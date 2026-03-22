"""Control test execution engine — runs automated checks on controls."""
from __future__ import annotations

import logging
import time
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.collectors.base import COLLECTOR_REGISTRY
from app.core.exceptions import NotFoundError
from app.models.control import Control
from app.models.control_test import ControlTestDefinition, ControlTestResult
from app.models.evidence import Evidence
from app.models.integration import Integration
from app.core.hashing import compute_sha256

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Assertion helpers
# ---------------------------------------------------------------------------

def _resolve_field(data: dict, path: str):
    """Resolve a dot-separated JSON path (e.g. 'data.compliant') on a dict."""
    parts = path.split(".")
    current = data
    for part in parts:
        if isinstance(current, dict):
            current = current.get(part)
        else:
            return None
    return current


def _evaluate_assertion(actual, operator: str, expected_str: str) -> bool:
    """Evaluate an assertion like actual == expected, actual > expected, etc."""
    # Try to match types
    if actual is None:
        return operator == "exists" and expected_str.lower() == "false"

    actual_str = str(actual).lower()
    expected_lower = expected_str.lower()

    if operator == "eq":
        return actual_str == expected_lower
    elif operator == "neq":
        return actual_str != expected_lower
    elif operator == "gt":
        try:
            return float(actual) > float(expected_str)
        except (ValueError, TypeError):
            return False
    elif operator == "gte":
        try:
            return float(actual) >= float(expected_str)
        except (ValueError, TypeError):
            return False
    elif operator == "lt":
        try:
            return float(actual) < float(expected_str)
        except (ValueError, TypeError):
            return False
    elif operator == "lte":
        try:
            return float(actual) <= float(expected_str)
        except (ValueError, TypeError):
            return False
    elif operator == "contains":
        return expected_lower in actual_str
    elif operator == "not_contains":
        return expected_lower not in actual_str
    elif operator == "exists":
        return (actual is not None) == (expected_lower == "true")
    return False


# ---------------------------------------------------------------------------
# CRUD for test definitions
# ---------------------------------------------------------------------------

async def list_test_definitions(
    db: AsyncSession, org_id: UUID, control_id: UUID | None = None,
    page: int = 1, page_size: int = 50,
) -> tuple[list[ControlTestDefinition], int]:
    base_q = select(ControlTestDefinition).where(ControlTestDefinition.org_id == org_id)
    count_q = select(func.count()).select_from(ControlTestDefinition).where(
        ControlTestDefinition.org_id == org_id
    )
    if control_id:
        base_q = base_q.where(ControlTestDefinition.control_id == control_id)
        count_q = count_q.where(ControlTestDefinition.control_id == control_id)

    total = (await db.execute(count_q)).scalar() or 0
    q = base_q.offset((page - 1) * page_size).limit(page_size).order_by(
        ControlTestDefinition.created_at.desc()
    )
    result = await db.execute(q)
    return list(result.scalars().all()), total


async def create_test_definition(
    db: AsyncSession, org_id: UUID, data: dict,
) -> ControlTestDefinition:
    defn = ControlTestDefinition(org_id=org_id, **data)
    db.add(defn)
    await db.commit()
    await db.refresh(defn)
    return defn


async def get_test_definition(
    db: AsyncSession, org_id: UUID, defn_id: UUID,
) -> ControlTestDefinition:
    result = await db.execute(
        select(ControlTestDefinition).where(
            ControlTestDefinition.id == defn_id,
            ControlTestDefinition.org_id == org_id,
        )
    )
    defn = result.scalar_one_or_none()
    if not defn:
        raise NotFoundError(f"Test definition {defn_id} not found")
    return defn


async def delete_test_definition(
    db: AsyncSession, org_id: UUID, defn_id: UUID,
) -> None:
    defn = await get_test_definition(db, org_id, defn_id)
    await db.delete(defn)
    await db.commit()


# ---------------------------------------------------------------------------
# Test execution
# ---------------------------------------------------------------------------

async def execute_test(
    db: AsyncSession, org_id: UUID, defn: ControlTestDefinition,
) -> ControlTestResult:
    """Run a single control test and record the result."""
    start = time.monotonic()

    # Get the collector
    collector = COLLECTOR_REGISTRY.get(defn.collector_type)
    if not collector:
        result = ControlTestResult(
            org_id=org_id,
            test_definition_id=defn.id,
            control_id=defn.control_id,
            result="error",
            actual_value=None,
            expected_value=defn.assertion_value,
            error_message=f"Collector '{defn.collector_type}' not found in registry",
            duration_ms=int((time.monotonic() - start) * 1000),
            executed_at=datetime.now(timezone.utc),
        )
        db.add(result)
        await db.commit()
        await db.refresh(result)
        return result

    # Get integration credentials if linked
    config = {}
    credentials = None
    if defn.integration_id:
        int_result = await db.execute(
            select(Integration).where(Integration.id == defn.integration_id)
        )
        integration = int_result.scalar_one_or_none()
        if integration:
            config = integration.config or {}
            if integration.credentials_ref:
                import json
                try:
                    credentials = json.loads(integration.credentials_ref)
                except (json.JSONDecodeError, TypeError):
                    credentials = {"ref": integration.credentials_ref}

    # Run the collector
    try:
        collect_result = await collector.collect(config=config, credentials=credentials)
    except Exception as exc:
        result = ControlTestResult(
            org_id=org_id,
            test_definition_id=defn.id,
            control_id=defn.control_id,
            result="error",
            actual_value=None,
            expected_value=defn.assertion_value,
            error_message=str(exc),
            duration_ms=int((time.monotonic() - start) * 1000),
            executed_at=datetime.now(timezone.utc),
        )
        db.add(result)
        await db.commit()
        await db.refresh(result)
        return result

    # Evaluate assertion
    actual_value = _resolve_field(collect_result, defn.assertion_field)
    passed = _evaluate_assertion(actual_value, defn.assertion_operator, defn.assertion_value)
    duration_ms = int((time.monotonic() - start) * 1000)

    # Create evidence record from the test
    import json as _json
    data_bytes = _json.dumps(collect_result.get("data", {}), sort_keys=True, default=str).encode()
    artifact_hash = compute_sha256(data_bytes)

    evidence = Evidence(
        org_id=org_id,
        control_id=defn.control_id,
        title=f"Control test: {defn.name} — {'PASS' if passed else 'FAIL'}",
        status="collected",
        collected_at=datetime.now(timezone.utc),
        data=collect_result.get("data", {}),
        collection_method="automated",
        collector=defn.collector_type,
        data_source="control_test",
        artifact_hash=artifact_hash,
    )
    db.add(evidence)
    await db.flush()

    # Create test result
    test_result = ControlTestResult(
        org_id=org_id,
        test_definition_id=defn.id,
        control_id=defn.control_id,
        result="pass" if passed else "fail",
        actual_value=str(actual_value) if actual_value is not None else None,
        expected_value=defn.assertion_value,
        evidence_id=evidence.id,
        duration_ms=duration_ms,
        details=collect_result.get("data", {}),
        executed_at=datetime.now(timezone.utc),
    )
    db.add(test_result)

    # Update the control's last test info
    control_result = await db.execute(
        select(Control).where(Control.id == defn.control_id, Control.org_id == org_id)
    )
    control = control_result.scalar_one_or_none()
    if control:
        control.last_test_date = datetime.now(timezone.utc)
        control.last_test_result = "pass" if passed else "fail"

    await db.commit()
    await db.refresh(test_result)

    logger.info(
        "Control test '%s' for control %s: %s (actual=%s, expected=%s)",
        defn.name, defn.control_id, test_result.result, actual_value, defn.assertion_value,
    )
    return test_result


async def run_all_due_tests(db: AsyncSession) -> int:
    """Run all active test definitions. Called by the scheduler."""
    result = await db.execute(
        select(ControlTestDefinition).where(ControlTestDefinition.is_active.is_(True))
    )
    definitions = list(result.scalars().all())
    executed = 0

    for defn in definitions:
        try:
            await execute_test(db, defn.org_id, defn)
            executed += 1
        except Exception as exc:
            logger.error("Failed to execute test %s: %s", defn.id, exc)

    return executed


# ---------------------------------------------------------------------------
# Query test results
# ---------------------------------------------------------------------------

async def list_test_results(
    db: AsyncSession, org_id: UUID, control_id: UUID | None = None,
    test_definition_id: UUID | None = None,
    page: int = 1, page_size: int = 50,
) -> tuple[list[ControlTestResult], int]:
    base_q = select(ControlTestResult).where(ControlTestResult.org_id == org_id)
    count_q = select(func.count()).select_from(ControlTestResult).where(
        ControlTestResult.org_id == org_id
    )
    if control_id:
        base_q = base_q.where(ControlTestResult.control_id == control_id)
        count_q = count_q.where(ControlTestResult.control_id == control_id)
    if test_definition_id:
        base_q = base_q.where(ControlTestResult.test_definition_id == test_definition_id)
        count_q = count_q.where(ControlTestResult.test_definition_id == test_definition_id)

    total = (await db.execute(count_q)).scalar() or 0
    q = base_q.offset((page - 1) * page_size).limit(page_size).order_by(
        ControlTestResult.created_at.desc()
    )
    result = await db.execute(q)
    return list(result.scalars().all()), total


async def get_control_test_summary(
    db: AsyncSession, org_id: UUID, control_id: UUID,
) -> dict:
    """Get test summary for a specific control."""
    total_q = select(func.count()).select_from(ControlTestResult).where(
        ControlTestResult.org_id == org_id,
        ControlTestResult.control_id == control_id,
    )
    pass_q = total_q.where(ControlTestResult.result == "pass")
    fail_q = total_q.where(ControlTestResult.result == "fail")

    total = (await db.execute(total_q)).scalar() or 0
    passed = (await db.execute(pass_q)).scalar() or 0
    failed = (await db.execute(fail_q)).scalar() or 0

    # Last test result
    last_q = select(ControlTestResult).where(
        ControlTestResult.org_id == org_id,
        ControlTestResult.control_id == control_id,
    ).order_by(ControlTestResult.created_at.desc()).limit(1)
    last_result = (await db.execute(last_q)).scalar_one_or_none()

    return {
        "total_runs": total,
        "passed": passed,
        "failed": failed,
        "pass_rate": round(passed / total * 100, 1) if total > 0 else 0,
        "last_result": last_result.result if last_result else None,
        "last_tested_at": last_result.executed_at.isoformat() if last_result else None,
    }
