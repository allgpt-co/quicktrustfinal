"""QT-009: isolated accounting tests; no external AI/payment calls."""
from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4
from unittest.mock import AsyncMock

import pytest
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError

from app.agents.common import llm
from app.config import get_settings
from app.core.dependencies import get_current_user
from app.main import app
from app.models.ai_usage import AiUsageEvent
from app.models.billing import Subscription
from app.models.questionnaire import QuestionnaireResponse
from app.models.usage import UsageCounter, UsageEvent
from app.services import ai_usage_service as ai, questionnaire_jobs as jobs, usage_service as meter
from tests.conftest import make_test_user_with_role, test_session as sessions
from tests.test_ai_usage import MODEL, execute, response
from tests.test_billing import assignment, plan, subscription_url

AT = datetime(2030, 1, 15, 12, tzinfo=timezone.utc)


@pytest.fixture(autouse=True)
def isolated(monkeypatch):
    original = app.dependency_overrides[get_current_user]
    monkeypatch.setattr(jobs, "bg_async_session", sessions)
    settings = get_settings()
    monkeypatch.setattr(settings, "BEDROCK_ENABLED", True)
    monkeypatch.setattr(settings, "BEDROCK_MODEL_ID", MODEL)
    monkeypatch.setattr(settings, "BEDROCK_INPUT_COST_PER_MILLION", 2.0)
    monkeypatch.setattr(settings, "BEDROCK_OUTPUT_COST_PER_MILLION", 10.0)
    yield
    app.dependency_overrides[get_current_user] = original


def receipt(org_id, key="test", **overrides):
    return dict(org_id=UUID(str(org_id)), kind="LLM_COMPLETION", idempotency_key=key,
                source_type="test_call", source_id=key, occurred_at=AT,
                prompt_tokens=12, completion_tokens=3, cost_micros=54) | overrides


async def rows(model):
    async with sessions() as db:
        return list((await db.scalars(select(model))).all())


@pytest.mark.asyncio
async def test_retry_once_conflicting_payload_and_organization_separation(client, org_id):
    other = (await client.post("/api/v1/organizations", json={"name": "Other", "slug": "usage-other"})).json()["id"]
    async with sessions() as db:
        assert await meter.append_event(db, **receipt(org_id))
        await db.commit()
        assert not await meter.append_event(db, **receipt(org_id, occurred_at=AT + timedelta(days=40)))
        await db.commit()
        with pytest.raises(meter.UsageConflictError):
            await meter.append_event(db, **receipt(org_id, cost_micros=900))
        await db.rollback()
        assert await meter.append_event(db, **receipt(other))
        await db.commit()
    counters = await rows(UsageCounter)
    assert len(counters) == 2
    assert all(c.quantity == c.event_count == 1 and c.known_cost_micros == 54 for c in counters)
    assert all(c.period_start.month == 1 for c in counters)


@pytest.mark.asyncio
async def test_unknown_tokens_cost_and_mocks_are_not_misreported_as_free(client, org_id):
    async with sessions() as db:
        await meter.append_event(db, **receipt(org_id))
        await meter.append_event(db, **receipt(org_id, "unknown", prompt_tokens=None, completion_tokens=None, cost_micros=None))
        await meter.append_event(db, **receipt(org_id, "unpriced", cost_micros=None))
        await meter.append_event(db, **receipt(org_id, "mock", is_mock=True))
        await db.commit()
    counter, = await rows(UsageCounter)
    assert counter.quantity == counter.event_count == 3
    assert (counter.known_prompt_tokens, counter.known_completion_tokens, counter.known_cost_micros) == (24, 6, 54)
    assert (counter.unknown_token_events, counter.unpriced_events) == (1, 2)
    assert len(await rows(UsageEvent)) == 4


@pytest.mark.asyncio
async def test_calendar_boundaries_and_signed_storage_deltas(client, org_id):
    before = datetime(2029, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
    boundary = datetime(2030, 1, 1, tzinfo=timezone.utc)
    async with sessions() as db:
        await meter.append_event(db, **receipt(org_id, "old", occurred_at=before))
        await meter.append_event(db, **receipt(org_id, "new", occurred_at=boundary))
        await meter.append_event(db, **receipt(org_id, "upload", kind="STORAGE_BYTES", quantity=100, prompt_tokens=None, completion_tokens=None, cost_micros=0))
        await meter.append_event(db, **receipt(org_id, "delete", kind="STORAGE_BYTES", quantity=-40, prompt_tokens=None, completion_tokens=None, cost_micros=0))
        await db.commit()
    counters = await rows(UsageCounter)
    assert len(counters) == 3
    assert next(c for c in counters if c.kind == "STORAGE_BYTES").quantity == 60
    old = next(c for c in counters if c.period_start.year == 2029)
    assert old.period_end.year == 2030 and old.period_end.month == 1


@pytest.mark.asyncio
async def test_ai_period_snapshot_survives_renewal_during_call(client, org_id):
    p = await plan(client)
    data = assignment(p["id"])
    data["current_period_start"] = (datetime.now(timezone.utc) - timedelta(days=10)).isoformat()
    data["current_period_end"] = (datetime.now(timezone.utc) + timedelta(days=20)).isoformat()
    assert (await client.put(subscription_url(org_id), json=data)).status_code == 200
    async with sessions() as db:
        event = await ai.start_call(db, org_id=UUID(org_id), questionnaire_id=uuid4())
        original_start = event.usage_period_start
    data.update(expected_version=1, current_period_start=data["current_period_end"],
                current_period_end=(datetime.now(timezone.utc) + timedelta(days=50)).isoformat())
    assert (await client.put(subscription_url(org_id), json=data)).status_code == 200
    async with sessions() as db:
        await ai.finish_call(db, event, {"model": MODEL, "prompt_tokens": 12, "completion_tokens": 3})
        assert (await meter.resolve_period(db, UUID(org_id), event.created_at)).source == "calendar_month"
    counter, = await rows(UsageCounter)
    assert counter.period_source == "subscription"
    assert meter.utc(counter.period_start) == meter.utc(original_start)


@pytest.mark.asyncio
async def test_provider_finalization_and_counter_failure_roll_back_together(client, org_id, monkeypatch):
    async with sessions() as db:
        event = await ai.start_call(db, org_id=UUID(org_id), questionnaire_id=uuid4())
        original = meter._insert
        def fail_counter(db, table):
            if table is UsageCounter:
                raise SQLAlchemyError("simulated counter failure")
            return original(db, table)
        with monkeypatch.context() as patch:
            patch.setattr(meter, "_insert", fail_counter)
            with pytest.raises(ai.UsageRecordingError):
                await ai.finish_call(db, event, {"prompt_tokens": 12, "completion_tokens": 3})
        await db.refresh(event)
        assert event.status == "started"
        assert await db.scalar(select(func.count()).select_from(UsageEvent)) == 0
        assert await db.scalar(select(func.count()).select_from(UsageCounter)) == 0
        await ai.finish_call(db, event, {"model": MODEL, "prompt_tokens": 12, "completion_tokens": 3})
    assert len(await rows(UsageCounter)) == 1


@pytest.mark.asyncio
async def test_autofill_counts_calls_saved_answers_and_questionnaire_once(client, org_id, monkeypatch):
    provider = AsyncMock(return_value=response())
    monkeypatch.setattr(llm.litellm, "acompletion", provider)
    _, job, result, url = await execute(client, org_id)
    assert result["status"] == "completed"
    await jobs.finish(UUID(job["id"]), count=1)
    await client.post(url)
    await jobs.execute_job(*(await jobs.claim_next()))
    totals = {c.kind: c for c in await rows(UsageCounter)}
    assert set(totals) == {"LLM_COMPLETION", "QUESTION_ANSWERED", "QUESTIONNAIRE_PROCESSED"}
    assert all(c.quantity == 1 for c in totals.values())
    assert sum(c.known_cost_micros for c in totals.values()) == 5400
    assert totals["QUESTION_ANSWERED"].known_cost_micros == 0
    assert provider.await_count == 1


@pytest.mark.asyncio
async def test_unsaved_answers_have_no_answer_or_questionnaire_charge(client, org_id, monkeypatch):
    monkeypatch.setattr(llm.litellm, "acompletion", AsyncMock(return_value=response()))
    original = meter.append_event
    async def fail_after_receipt(db, **kwargs):
        result = await original(db, **kwargs)
        if kwargs["kind"] == "QUESTION_ANSWERED":
            raise SQLAlchemyError("simulated answer transaction failure")
        return result
    monkeypatch.setattr(meter, "append_event", fail_after_receipt)
    _, _, result, _ = await execute(client, org_id)
    assert result["status"] == "failed"
    assert await rows(QuestionnaireResponse) == []
    counter, = await rows(UsageCounter)
    assert counter.kind == "LLM_COMPLETION" and counter.quantity == 1
    assert len(await rows(UsageEvent)) == 1


@pytest.mark.asyncio
async def test_failed_job_completion_retries_without_double_charging_answers(client, org_id, monkeypatch):
    provider = AsyncMock(return_value=response())
    monkeypatch.setattr(llm.litellm, "acompletion", provider)
    original = meter.append_event
    async def fail_completion(db, **kwargs):
        result = await original(db, **kwargs)
        if kwargs["kind"] == "QUESTIONNAIRE_PROCESSED":
            raise SQLAlchemyError("simulated completion transaction failure")
        return result
    with monkeypatch.context() as patch:
        patch.setattr(meter, "append_event", fail_completion)
        _, _, result, url = await execute(client, org_id)
    assert result["status"] == "failed"
    assert len(await rows(QuestionnaireResponse)) == 1
    assert len(await rows(UsageCounter)) == 2
    await client.post(url)
    await jobs.execute_job(*(await jobs.claim_next()))
    assert (await client.get(url)).json()["status"] == "completed"
    assert len(await rows(UsageCounter)) == 3
    assert provider.await_count == 1


@pytest.mark.asyncio
async def test_mock_autofill_never_creates_consumption_counters(client, org_id, monkeypatch):
    monkeypatch.setattr(get_settings(), "BEDROCK_ENABLED", False)
    _, _, result, _ = await execute(client, org_id)
    assert result["status"] == "completed"
    assert await rows(UsageCounter) == []
    events = await rows(UsageEvent)
    assert len(events) == 1 and events[0].is_mock


@pytest.mark.asyncio
async def test_legacy_backfill_is_bounded_idempotent_and_not_assigned_to_current_contract(client, org_id):
    p = await plan(client)
    assert (await client.put(subscription_url(org_id), json=assignment(p["id"]))).status_code == 200
    async with sessions() as db:
        for status in ("reported", "unknown", "mock", "started"):
            db.add(AiUsageEvent(org_id=UUID(org_id), questionnaire_id=uuid4(), batch_index=0,
                status=status, model="mock" if status == "mock" else MODEL,
                prompt_tokens=12 if status in ("reported", "mock") else None,
                completion_tokens=3 if status in ("reported", "mock") else None,
                cost_micros=54 if status == "reported" else 0 if status == "mock" else None,
                created_at=AT))
        await db.commit()
        assert (await meter.get_usage(db, UUID(org_id)))["unprojected_ai_calls"] == 3
        assert await meter.backfill_ai_calls(db, UUID(org_id), limit=1) == 1
        await db.commit()
        assert await meter.backfill_ai_calls(db, UUID(org_id), limit=100) == 2
        await db.commit()
        assert await meter.backfill_ai_calls(db, UUID(org_id)) == 0
        report = await meter.get_usage(db, UUID(org_id))
        assert report["unprojected_ai_calls"] == 0 and report["pending_ai_calls"] == 1
    counter, = await rows(UsageCounter)
    assert counter.period_source == "legacy_calendar_month" and counter.quantity == 2
    assert counter.unpriced_events == counter.unknown_token_events == 1


@pytest.mark.asyncio
async def test_usage_api_is_scoped_and_paginates_stored_periods(client, org_id):
    async with sessions() as db:
        await meter.append_event(db, **receipt(org_id))
        await meter.append_event(db, **receipt(org_id, "feb", occurred_at=AT + timedelta(days=35)))
        await db.commit()
    url = f"/api/v1/organizations/{org_id}/billing/usage"
    result = await client.get(url + "?limit=1")
    assert result.status_code == 200
    report = result.json()
    assert len(report["counters"]) == 1 and report["next_offset"] == 1
    assert report["enforcement_enabled"] is False
    assert "Auto-fill" in report["coverage"]
    assert (await client.get(url + "?limit=1&offset=1")).json()["next_offset"] is None
    async def employee():
        return make_test_user_with_role("employee", UUID(org_id))
    app.dependency_overrides[get_current_user] = employee
    assert (await client.get(url)).status_code == 403
    async def foreign_admin():
        return make_test_user_with_role("super_admin", uuid4())
    app.dependency_overrides[get_current_user] = foreign_admin
    assert (await client.get(url)).status_code == 403
    async def own_admin():
        return make_test_user_with_role("super_admin", UUID(org_id))
    app.dependency_overrides[get_current_user] = own_admin
    assert (await client.get(url)).status_code == 200
    assert (await client.get(url + "?limit=1001")).status_code == 422
    app.dependency_overrides.pop(get_current_user)
    assert (await client.get(url)).status_code == 401


@pytest.mark.asyncio
@pytest.mark.parametrize("changes", [{"quantity": -1}, {"quantity": True}, {"quantity": 2**63},
    {"kind": "invented"}, {"cost_micros": -1}, {"prompt_tokens": -1}, {"idempotency_key": ""},
    {"is_mock": "false"}])
async def test_invalid_receipts_are_rejected_without_partial_writes(client, org_id, changes):
    async with sessions() as db:
        with pytest.raises(ValueError):
            await meter.append_event(db, **receipt(org_id, **changes))
        assert await db.scalar(select(func.count()).select_from(UsageEvent)) == 0


@pytest.mark.asyncio
async def test_keyword_matches_are_separate_from_ai_answers(client, org_id, monkeypatch):
    from app.models.control import Control
    async with sessions() as db:
        db.add(Control(org_id=UUID(org_id), title="Security question", status="implemented"))
        await db.commit()
    provider = AsyncMock(side_effect=AssertionError("Keyword matching must not call AI"))
    monkeypatch.setattr(llm.litellm, "acompletion", provider)
    _, _, result, _ = await execute(client, org_id)
    assert result["status"] == "completed"
    counters = {c.kind: c.quantity for c in await rows(UsageCounter)}
    assert counters == {"QUESTION_MATCHED": 1, "QUESTIONNAIRE_PROCESSED": 1}
    provider.assert_not_awaited()


@pytest.mark.asyncio
async def test_client_style_answer_row_does_not_create_processing_usage(client, org_id):
    from tests.test_questionnaire_jobs import create
    questionnaire = await create(client, org_id, 1)
    async with sessions() as db:
        # Legacy/manual routes may accept source_type. It is not proof of billable processing.
        db.add(QuestionnaireResponse(org_id=UUID(org_id), questionnaire_id=UUID(questionnaire),
            question_id="q0", question_text="Security question 0", answer="User supplied", source_type="control"))
        await db.commit()
    url = f"/api/v1/organizations/{org_id}/questionnaires/{questionnaire}/auto-fill"
    await client.post(url)
    await jobs.execute_job(*(await jobs.claim_next()))
    assert (await client.get(url)).json()["status"] == "completed"
    assert await rows(UsageEvent) == []
    assert await rows(UsageCounter) == []


@pytest.mark.asyncio
async def test_questionnaire_deletion_preserves_accounting_history(client, org_id, monkeypatch):
    monkeypatch.setattr(llm.litellm, "acompletion", AsyncMock(return_value=response()))
    questionnaire, _, _, _ = await execute(client, org_id)
    assert (await client.delete(f"/api/v1/organizations/{org_id}/questionnaires/{questionnaire}")).status_code == 204
    assert await rows(QuestionnaireResponse) == []
    assert len(await rows(UsageEvent)) == 3
    assert len(await rows(UsageCounter)) == 3
