"""Project existing AI ledgers in bounded transactions; repeat safely after interruption.

Example: python -m app.scripts.backfill_ai_usage --org-id UUID --max-batches 10
Requires migration 0020. Uses the configured database; run only for an authorized org.
"""
import argparse
import asyncio
from uuid import UUID

from sqlalchemy import func, select
from app.core.database import async_session, engine
from app.models.organization import Organization
from app.services.usage_service import backfill_ai_calls, unprojected_ai_query


async def run(args):
    total = 0
    try:
        async with async_session() as db:
            if await db.get(Organization, args.org_id) is None:
                raise ValueError("Organization not found")
            for _ in range(args.max_batches):
                count = await backfill_ai_calls(db, args.org_id, limit=args.batch_size)
                await db.commit()
                total += count
                if count < args.batch_size:
                    break
            remaining = await db.scalar(select(func.count()).select_from(unprojected_ai_query(args.org_id).subquery()))
            print(f"Projected {total} AI ledger rows; {remaining} finalized rows remain. Started calls are not inferred.")
    finally:
        await engine.dispose()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--org-id", type=UUID, required=True)
    parser.add_argument("--batch-size", type=int, choices=range(1, 1001), default=100, metavar="1..1000")
    parser.add_argument("--max-batches", type=int, choices=range(1, 101), default=10, metavar="1..100")
    asyncio.run(run(parser.parse_args()))
