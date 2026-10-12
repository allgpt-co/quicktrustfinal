"""QT-004: queue lifecycle, authorization, progress, retries, and saved answers."""
import asyncio
from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4
from unittest.mock import AsyncMock

import pytest
from sqlalchemy import select

from app.main import app
from app.core.dependencies import get_current_user
from app.models.workflow import WorkflowExecution
from app.models.questionnaire import QuestionnaireResponse
from app.services import questionnaire_jobs as jobs
from app.agents.common import llm
from tests.conftest import test_session as session_factory, make_test_user_with_role, override_get_current_user


async def create(client, org, count=41):
    response = await client.post(f"/api/v1/organizations/{org}/questionnaires", json={
        "title": "Audit test", "questions": [
            {"question_id": f"q{i}", "question_text": f"Security question {i}"} for i in range(count)
        ],
    })
    assert response.status_code == 201, response.text
    return response.json()["id"]


@pytest.mark.asyncio
async def test_enqueue_returns_before_llm_and_reuses_active_job(client, org_id, monkeypatch):
    questionnaire = await create(client, org_id)
    ai = AsyncMock(side_effect=AssertionError("AI must not run in the HTTP request"))
    monkeypatch.setattr(llm, "call_llm_json", ai)
    url = f"/api/v1/organizations/{org_id}/questionnaires/{questionnaire}/auto-fill"
    first = await client.post(url)
    second = await client.post(url)
    assert first.status_code == second.status_code == 202
    assert first.json()["id"] == second.json()["id"]
    assert first.json()["status"] == "pending"
    ai.assert_not_called()
    assert (await client.get(url)).json()["id"] == first.json()["id"]
    base = url.removesuffix("/auto-fill")
    assert (await client.patch(base, json={"questions": []})).status_code == 409
    assert (await client.delete(base)).status_code == 409
    async def outsider():
        return make_test_user_with_role("compliance_manager", uuid4())
    app.dependency_overrides[get_current_user] = outsider
    try:
        assert (await client.get(url)).status_code == 403
        assert (await client.post(url)).status_code == 403
    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user


@pytest.mark.asyncio
async def test_worker_saves_answers_and_progress_and_retry_skips_existing(client, org_id, monkeypatch):
    monkeypatch.setattr(jobs, "bg_async_session", session_factory)
    questionnaire = await create(client, org_id)
    url = f"/api/v1/organizations/{org_id}/questionnaires/{questionnaire}/auto-fill"
    await client.post(url)
    claimed = await jobs.claim_next()
    assert claimed is not None
    assert await jobs.claim_next() is None
    seen = []
    async def answer(*, messages, **kwargs):
        async with session_factory() as db:
            wf = await db.get(WorkflowExecution, claimed[0])
            seen.append(wf.current_step)
        import re
        ids = re.findall(r"- ID: (\S+) \|", messages[-1]["content"])
        return {"answers": [{"question_id": q, "answer": "Test answer", "confidence": .9} for q in ids]}, {}
    monkeypatch.setattr(llm, "call_llm_json", answer)
    await jobs.execute_job(*claimed)
    result = (await client.get(url)).json()
    assert result["status"] == "completed"
    assert result["current_step"] == 41
    assert result["output_data"] == {"filled_count": 41}
    assert seen == [0, 20, 40]
    detail = (await client.get(url.removesuffix("/auto-fill"))).json()
    assert len(detail["responses"]) == detail["answered_count"] == 41
    await client.post(url)
    claimed = await jobs.claim_next()
    await jobs.execute_job(*claimed)
    assert (await client.get(url)).json()["output_data"] == {"filled_count": 0}
    assert len(seen) == 3
    updated = await client.patch(url.removesuffix("/auto-fill"), json={"title": "Reviewed"})
    assert updated.status_code == 200, updated.text
    assert len(updated.json()["responses"]) == 41


@pytest.mark.asyncio
async def test_failed_batch_retains_answers_and_can_retry(client, org_id, monkeypatch):
    monkeypatch.setattr(jobs, "bg_async_session", session_factory)
    questionnaire = await create(client, org_id, 21)
    url = f"/api/v1/organizations/{org_id}/questionnaires/{questionnaire}/auto-fill"
    await client.post(url)
    ai = AsyncMock(side_effect=[({"answers": [{"question_id": "q0", "answer": "Saved", "confidence": .9}]}, {}), RuntimeError("private provider error")])
    monkeypatch.setattr(llm, "call_llm_json", ai)
    await jobs.execute_job(*(await jobs.claim_next()))
    result = (await client.get(url)).json()
    assert result["status"] == "failed"
    assert "private provider" not in result["error_message"]
    async with session_factory() as db:
        answers = (await db.execute(select(QuestionnaireResponse))).scalars().all()
        assert len(answers) == 1
    retry = await client.post(url)
    assert retry.status_code == 202
    assert retry.json()["id"] != result["id"]


@pytest.mark.asyncio
async def test_timeout_and_stale_recovery(client, org_id, monkeypatch):
    monkeypatch.setattr(jobs, "bg_async_session", session_factory)
    questionnaire = await create(client, org_id, 1)
    url = f"/api/v1/organizations/{org_id}/questionnaires/{questionnaire}/auto-fill"
    await client.post(url)
    monkeypatch.setattr(jobs, "JOB_TIMEOUT_SECONDS", .02)
    async def slow(*args, **kwargs):
        await asyncio.sleep(10)
    monkeypatch.setattr(llm, "call_llm_json", slow)
    await jobs.execute_job(*(await jobs.claim_next()))
    assert (await client.get(url)).json()["status"] == "failed"
    await client.post(url)
    claimed = await jobs.claim_next()
    async with session_factory() as db:
        wf = await db.get(WorkflowExecution, claimed[0])
        wf.started_at = datetime.now(timezone.utc) - timedelta(hours=1)
        await db.commit()
    assert await jobs.claim_next() is None
    assert (await client.get(url)).json()["status"] == "failed"


@pytest.mark.asyncio
async def test_worker_cancellation_marks_job_failed(client, org_id, monkeypatch):
    monkeypatch.setattr(jobs, "bg_async_session", session_factory)
    questionnaire = await create(client, org_id, 1)
    url = f"/api/v1/organizations/{org_id}/questionnaires/{questionnaire}/auto-fill"
    await client.post(url)
    entered = asyncio.Event()
    async def blocked(*args, **kwargs):
        entered.set()
        await asyncio.Event().wait()
    monkeypatch.setattr(llm, "call_llm_json", blocked)
    task = asyncio.create_task(jobs.execute_job(*(await jobs.claim_next())))
    await asyncio.wait_for(entered.wait(), timeout=5)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert (await client.get(url)).json()["status"] == "failed"


@pytest.mark.asyncio
async def test_job_status_cannot_be_read_using_another_org_url(client, org_id):
    questionnaire = await create(client, org_id, 1)
    job = (await client.post(f"/api/v1/organizations/{org_id}/questionnaires/{questionnaire}/auto-fill")).json()
    # Platform admin passes the organization guard, but entity lookup must still be scoped.
    wrong_org = uuid4()
    response = await client.get(f"/api/v1/organizations/{wrong_org}/questionnaires/{questionnaire}/auto-fill")
    assert response.status_code == 404
    response = await client.get(f"/api/v1/organizations/{wrong_org}/workflows/{job['id']}")
    assert response.status_code == 404
