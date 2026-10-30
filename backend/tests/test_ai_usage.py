"""QT-007: credential-free tests using known provider usage and synthetic prices."""
from decimal import Decimal
from types import SimpleNamespace
from uuid import UUID, uuid4
from unittest.mock import AsyncMock

import pytest
from sqlalchemy import select
from app.agents.common import llm
from app.config import get_settings
from app.models.ai_usage import AiUsageEvent
from app.models.questionnaire import QuestionnaireResponse
from app.services import questionnaire_jobs as jobs, ai_usage_service as meter
from tests.conftest import test_session as sessions, TEST_USER_ID
from tests.test_questionnaire_jobs import create

MODEL = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"


@pytest.fixture(autouse=True)
def pricing(monkeypatch):
    settings = get_settings()
    monkeypatch.setattr(settings, "BEDROCK_ENABLED", True)
    monkeypatch.setattr(settings, "BEDROCK_MODEL_ID", MODEL)
    # Artificial rates for arithmetic tests, not a claim about current AWS prices.
    monkeypatch.setattr(settings, "BEDROCK_INPUT_COST_PER_MILLION", 2.0)
    monkeypatch.setattr(settings, "BEDROCK_OUTPUT_COST_PER_MILLION", 10.0)
    monkeypatch.setattr(jobs, "bg_async_session", sessions)


def response(content='{"answers":[{"question_id":"q0","answer":"Test answer","confidence":0.9}]}', usage=True):
    return SimpleNamespace(usage=SimpleNamespace(prompt_tokens=1200, completion_tokens=300, total_tokens=1500) if usage else None,
                          choices=[SimpleNamespace(message=SimpleNamespace(content=content))])


async def execute(client, org_id, count=1):
    questionnaire = await create(client, org_id, count)
    url = f"/api/v1/organizations/{org_id}/questionnaires/{questionnaire}/auto-fill"
    job = (await client.post(url)).json()
    await jobs.execute_job(*(await jobs.claim_next()))
    return questionnaire, job, (await client.get(url)).json(), url


async def events():
    async with sessions() as db:
        return list((await db.execute(select(AiUsageEvent).order_by(AiUsageEvent.created_at))).scalars())


@pytest.mark.asyncio
async def test_autofill_persists_exact_usage_and_retry_skips_saved_answers(client, org_id, monkeypatch):
    provider = AsyncMock(return_value=response())
    monkeypatch.setattr(llm.litellm, "acompletion", provider)
    questionnaire, job, result, url = await execute(client, org_id)
    assert result["status"] == "completed"
    rows = await events()
    assert len(rows) == 1
    row = rows[0]
    assert (row.prompt_tokens, row.completion_tokens, row.cost_micros) == (1200, 300, 5400)
    assert row.model == MODEL and row.status == "reported"
    assert row.org_id == UUID(org_id) and row.questionnaire_id == UUID(questionnaire)
    assert row.job_id == UUID(job["id"]) and row.user_id == TEST_USER_ID
    assert row.input_rate_per_million == Decimal("2") and row.output_rate_per_million == Decimal("10")
    async with sessions() as db:
        # A duplicate finalization must not alter the original consumption or pricing.
        await meter.finish_call(db, row, {"model": MODEL, "prompt_tokens": 9999, "completion_tokens": 9999})
    assert (await events())[0].cost_micros == 5400
    await client.post(url)
    await jobs.execute_job(*(await jobs.claim_next()))
    assert provider.await_count == 1
    assert len(await events()) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("content", ['not valid JSON', '{"answers":[]}'])
async def test_paid_usage_survives_invalid_or_unanswerable_output(client, org_id, monkeypatch, content):
    monkeypatch.setattr(llm.litellm, "acompletion", AsyncMock(return_value=response(content)))
    _, _, result, _ = await execute(client, org_id)
    assert result["status"] == ("failed" if content == 'not valid JSON' else "completed")
    row, = await events()
    assert row.status == "reported" and row.cost_micros == 5400
    async with sessions() as db:
        assert list((await db.execute(select(QuestionnaireResponse))).scalars()) == []


@pytest.mark.asyncio
async def test_missing_usage_and_provider_failure_are_unknown_not_free(client, org_id, monkeypatch):
    provider = AsyncMock(side_effect=[response(usage=False), RuntimeError("provider unavailable")])
    monkeypatch.setattr(llm.litellm, "acompletion", provider)
    await execute(client, org_id)
    await execute(client, org_id)
    rows = await events()
    assert len(rows) == 2
    assert all(r.status == "unknown" and r.cost_micros is None and r.prompt_tokens is None for r in rows)


@pytest.mark.asyncio
async def test_mock_usage_is_identified_and_has_no_paid_cost(client, org_id, monkeypatch):
    monkeypatch.setattr(get_settings(), "BEDROCK_ENABLED", False)
    provider = AsyncMock(side_effect=AssertionError("No network call allowed"))
    monkeypatch.setattr(llm.litellm, "acompletion", provider)
    await execute(client, org_id)
    row, = await events()
    assert (row.status, row.prompt_tokens, row.completion_tokens, row.cost_micros) == ("mock", 0, 0, 0)
    provider.assert_not_awaited()


@pytest.mark.asyncio
async def test_missing_prices_preserve_tokens_without_inventing_zero_cost(client, org_id, monkeypatch):
    monkeypatch.setattr(get_settings(), "BEDROCK_INPUT_COST_PER_MILLION", 0)
    monkeypatch.setattr(llm.litellm, "acompletion", AsyncMock(return_value=response()))
    await execute(client, org_id)
    row, = await events()
    assert row.prompt_tokens == 1200 and row.completion_tokens == 300
    assert row.cost_micros is None


@pytest.mark.asyncio
async def test_ledger_failure_prevents_provider_call(client, org_id, monkeypatch):
    provider = AsyncMock(return_value=response())
    monkeypatch.setattr(llm.litellm, "acompletion", provider)
    monkeypatch.setattr(meter, "start_call", AsyncMock(side_effect=meter.UsageRecordingError("database unavailable")))
    _, _, result, _ = await execute(client, org_id)
    assert result["status"] == "failed"
    provider.assert_not_awaited()


@pytest.mark.asyncio
async def test_finalization_failure_stops_answer_save_and_retains_started_record(client, org_id, monkeypatch):
    monkeypatch.setattr(llm.litellm, "acompletion", AsyncMock(return_value=response()))
    monkeypatch.setattr(meter, "finish_call", AsyncMock(side_effect=meter.UsageRecordingError("database unavailable")))
    _, _, result, _ = await execute(client, org_id)
    assert result["status"] == "failed"
    row, = await events()
    assert row.status == "started" and row.cost_micros is None
    async with sessions() as db:
        assert list((await db.execute(select(QuestionnaireResponse))).scalars()) == []


@pytest.mark.asyncio
async def test_new_provider_invocations_are_distinct_and_org_scoped(client, org_id, monkeypatch):
    monkeypatch.setattr(llm.litellm, "acompletion", AsyncMock(return_value=response('{"answers":[]}')))
    _, _, _, url = await execute(client, org_id)
    # Retrying an unanswered questionnaire makes a new paid call, not a duplicate write.
    await client.post(url)
    await jobs.execute_job(*(await jobs.claim_next()))
    other_org = (await client.post("/api/v1/organizations", json={"name": "Other org", "slug": "qt007-other"})).json()["id"]
    await execute(client, other_org)
    rows = await events()
    assert len({r.id for r in rows}) == 3
    assert len({r.job_id for r in rows}) == 3
    assert sum(r.cost_micros for r in rows if r.org_id == UUID(org_id)) == 10800
    assert sum(r.cost_micros for r in rows if r.org_id == UUID(other_org)) == 5400


def test_fractional_rates_round_only_after_summing():
    assert meter.estimate_cost_micros(1, 1, Decimal("0.4"), Decimal("0.4")) == 1


@pytest.mark.asyncio
async def test_answer_database_failure_does_not_erase_paid_usage(client, org_id, monkeypatch):
    from sqlalchemy import event
    from sqlalchemy.orm import Session
    from sqlalchemy.exc import SQLAlchemyError
    monkeypatch.setattr(llm.litellm, "acompletion", AsyncMock(return_value=response()))

    def fail_answer(session, context, instances):
        if any(isinstance(row, QuestionnaireResponse) for row in session.new):
            raise SQLAlchemyError("Simulated answer storage failure")

    event.listen(Session, "before_flush", fail_answer)
    try:
        _, _, result, _ = await execute(client, org_id)
    finally:
        event.remove(Session, "before_flush", fail_answer)
    assert result["status"] == "failed"
    row, = await events()
    assert row.status == "reported" and row.cost_micros == 5400


def test_prices_match_persisted_precision_and_reject_nonfinite_values():
    assert meter._rate("0.123456789") == Decimal("0.12345679")
    assert meter._rate("NaN") is None
    assert meter._rate("Infinity") is None
    assert meter._rate(-1) is None
    assert meter._rate(0) is None


@pytest.mark.asyncio
async def test_rates_are_snapshotted_and_unrecognized_model_is_unpriced(client, org_id, monkeypatch):
    monkeypatch.setattr(llm.litellm, "acompletion", AsyncMock(return_value=response()))
    _, _, _, _ = await execute(client, org_id)
    row, = await events()
    monkeypatch.setattr(get_settings(), "BEDROCK_INPUT_COST_PER_MILLION", 100)
    async with sessions() as db:
        second = await meter.start_call(db, org_id=row.org_id, questionnaire_id=row.questionnaire_id)
        await meter.finish_call(db, second, {"model": "different-model", "prompt_tokens": 1200, "completion_tokens": 300})
    rows = await events()
    priced = next(r for r in rows if r.id == row.id)
    unpriced = next(r for r in rows if r.id != row.id)
    assert priced.cost_micros == 5400 and priced.input_rate_per_million == Decimal("2")
    assert unpriced.cost_micros is None and unpriced.prompt_tokens == 1200
