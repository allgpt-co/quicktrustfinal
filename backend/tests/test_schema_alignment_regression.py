"""Real PostgreSQL checks; each test owns a temporary schema, never public.

Run from backend/ with the database dependencies installed:
QT_SCHEMA_TEST_DATABASE_URL=postgresql+asyncpg://... python tests/test_schema_alignment_regression.py

The URL must point to a disposable test database with schema creation privileges.
"""

import asyncio
import contextlib
import io
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from alembic import command
from alembic.config import Config

import app.models
from app.core import database

ROOT = Path(__file__).resolve().parents[1]
TEST_URL = os.environ.get("QT_SCHEMA_TEST_DATABASE_URL")


@unittest.skipUnless(TEST_URL, "Set QT_SCHEMA_TEST_DATABASE_URL to an isolated PostgreSQL database")
class SchemaAlignmentTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.schema = "qt_migration_test_" + uuid.uuid4().hex
        self.admin = create_async_engine(TEST_URL)
        async with self.admin.begin() as conn:
            await conn.execute(sa.text(f'CREATE SCHEMA "{self.schema}"'))
        self.engine = create_async_engine(
            TEST_URL, connect_args={"server_settings": {"search_path": self.schema}}
        )
        await self.migrate("0012")

    async def asyncTearDown(self):
        await self.engine.dispose()
        async with self.admin.begin() as conn:
            await conn.execute(sa.text(f'DROP SCHEMA "{self.schema}" CASCADE'))
        await self.admin.dispose()

    async def migrate(self, revision):
        def run(connection):
            cfg = Config(str(ROOT / "alembic.ini"))
            cfg.set_main_option("script_location", str(ROOT / "alembic"))
            cfg.attributes["connection"] = connection
            command.upgrade(cfg, revision)
        async with self.engine.begin() as conn:
            await conn.run_sync(run)

    async def assert_no_missing_columns(self):
        def check(connection):
            inspector = sa.inspect(connection)
            missing = []
            for table in database.Base.metadata.tables.values():
                if not inspector.has_table(table.name):
                    missing.append(table.name)
                    continue
                actual = {c["name"] for c in inspector.get_columns(table.name)}
                missing.extend(f"{table.name}.{name}" for name in set(table.c.keys()) - actual)
            self.assertEqual(missing, [])
        async with self.engine.connect() as conn:
            await conn.run_sync(check)

    async def seed(self):
        from seeds.run_seeds import main
        sessions = async_sessionmaker(self.engine, expire_on_commit=False)
        with patch.multiple(database, engine=self.engine, async_session=sessions):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                await main()
        self.assertIn("Seeding complete!", output.getvalue())

    async def counts(self):
        async with self.engine.connect() as conn:
            return {
                name: await conn.scalar(sa.text(f'SELECT count(*) FROM "{name}"'))
                for name in ("frameworks", "framework_domains", "framework_requirements",
                             "control_objectives", "control_templates", "evidence_templates",
                             "policy_templates", "control_template_framework_mappings")
            }

    async def test_clean_migration_and_repeated_seed(self):
        await self.migrate("0013")
        await self.assert_no_missing_columns()
        await self.seed()
        counts = await self.counts()
        self.assertGreater(counts["frameworks"], 10)
        await self.seed()
        self.assertEqual(await self.counts(), counts)
        await self.migrate("head")  # no-op after successful upgrade

    async def test_partial_seed_schema_preserves_legacy_data(self):
        ids = {name: str(uuid.uuid4()) for name in ("org", "framework", "domain", "req", "objective",
                "template", "evidence", "policy", "mapping", "control", "audit")}
        async with self.engine.begin() as conn:
            # Reproduce the user's seed attempt: create missing tables, leave old columns untouched.
            await conn.run_sync(database.Base.metadata.create_all)
            await conn.execute(sa.text("INSERT INTO organizations (id,name,slug,cloud_providers) "
                                       "VALUES (:org,'Legacy org','legacy-org','[\"aws\"]')"), ids)
            await conn.execute(sa.text("INSERT INTO frameworks (id,name,version) "
                                       "VALUES (:framework,'Legacy framework','1')"), ids)
            await conn.execute(sa.text("INSERT INTO framework_domains (id,framework_id,name,domain_order) "
                                       "VALUES (:domain,:framework,'Legacy domain',7)"), ids)
            await conn.execute(sa.text("INSERT INTO framework_requirements (id,domain_id,ref_code,title) "
                                       "VALUES (:req,:domain,'SEC.1','Legacy requirement')"), ids)
            await conn.execute(sa.text("INSERT INTO control_objectives (id,requirement_id,ref_code,title) "
                                       "VALUES (:objective,:req,'SEC.1.1','Legacy objective')"), ids)
            await conn.execute(sa.text("INSERT INTO control_templates (id,title,domain) "
                                       "VALUES (:template,'Legacy control','Security')"), ids)
            await conn.execute(sa.text("INSERT INTO evidence_templates (id,title,evidence_type) "
                                       "VALUES (:evidence,'Legacy evidence','document')"), ids)
            await conn.execute(sa.text("INSERT INTO policy_templates (id,title,category,content) "
                                       "VALUES (:policy,'Legacy policy','Security','Keep this policy')"), ids)
            await conn.execute(sa.text("INSERT INTO control_template_framework_mappings "
                "(id,control_template_id,framework_id,requirement_id) "
                "VALUES (:mapping,:template,:framework,:req)"), ids)
            await conn.execute(sa.text("INSERT INTO controls (id,org_id,title,implementation_notes) "
                                       "VALUES (:control,:org,'Legacy control','Keep these notes')"), ids)
            await conn.execute(sa.text("INSERT INTO audit_logs (id,org_id,action,created_at,ip_address) "
                "VALUES (:audit,:org,'legacy-event','2020-01-01T00:00:00Z','127.0.0.1')"), ids)
        await self.migrate("0013")
        await self.assert_no_missing_columns()
        async with self.engine.connect() as conn:
            async def scalar(sql):
                return await conn.scalar(sa.text(sql), ids)
            self.assertTrue(await scalar("SELECT is_active FROM frameworks WHERE id=:framework"))
            self.assertEqual(await scalar("SELECT sort_order FROM framework_domains WHERE id=:domain"), 7)
            self.assertEqual(await scalar("SELECT code FROM framework_requirements WHERE id=:req"), "SEC.1")
            self.assertEqual(await scalar("SELECT code FROM control_objectives WHERE id=:objective"), "SEC.1.1")
            self.assertEqual(await scalar("SELECT requirement_code FROM control_template_framework_mappings "
                                          "WHERE id=:mapping"), "SEC.1")
            self.assertEqual(await scalar("SELECT implementation_details FROM controls WHERE id=:control"),
                             "Keep these notes")
            self.assertEqual(await scalar("SELECT content_template FROM policy_templates WHERE id=:policy"),
                             "Keep this policy")
            self.assertEqual(await scalar("SELECT template_code FROM control_templates WHERE id=:template"),
                             "legacy-" + ids["template"])
            self.assertEqual(await scalar("SELECT cloud_providers FROM organizations WHERE id=:org"), ["aws"])
            self.assertEqual(await scalar("SELECT outcome FROM audit_logs WHERE id=:audit"), "unknown")
            self.assertEqual(await scalar('SELECT extract(year FROM "timestamp") FROM audit_logs WHERE id=:audit'), 2020)
            self.assertEqual(await scalar("SELECT actor_ip FROM audit_logs WHERE id=:audit"), "127.0.0.1")
            self.assertEqual(await scalar("SELECT ref_code FROM framework_requirements WHERE id=:req"), "SEC.1")
        await self.seed()

    async def test_user_timestamps_allow_admin_member_listing(self):
        await self.migrate("0014")
        org_id = uuid.uuid4()
        missing_id, existing_id, new_id = (uuid.uuid4() for _ in range(3))
        async with self.engine.begin() as conn:
            await conn.execute(sa.text(
                "INSERT INTO organizations (id,name,slug) VALUES (:id,'Timestamp test',:id)"
            ), {"id": str(org_id)})
            for user_id, timestamp in ((missing_id, None), (existing_id, "2021-02-03T00:00:00Z")):
                await conn.execute(sa.text(
                    "INSERT INTO users (id,org_id,email,full_name,role,created_at,updated_at) "
                    "VALUES (:id,:org,:email,'Test member','employee',"
                    "'2020-01-01T00:00:00Z',CAST(CAST(:updated AS text) AS timestamptz))"
                ), {"id": str(user_id), "org": str(org_id),
                    "email": f"{user_id}@example.com", "updated": timestamp})
        await self.migrate("head")
        async with self.engine.begin() as conn:
            self.assertEqual(await conn.scalar(sa.text(
                "SELECT updated_at = created_at FROM users WHERE id=:id"
            ), {"id": str(missing_id)}), True)
            self.assertEqual(await conn.scalar(sa.text(
                "SELECT extract(year FROM updated_at) FROM users WHERE id=:id"
            ), {"id": str(existing_id)}), 2021)
            await conn.execute(sa.text(
                "INSERT INTO users (id,org_id,email,full_name,role) "
                "VALUES (:id,:org,:email,'New member','employee')"
            ), {"id": str(new_id), "org": str(org_id), "email": f"{new_id}@example.com"})
            def check_column(connection):
                column = next(c for c in sa.inspect(connection).get_columns("users")
                              if c["name"] == "updated_at")
                self.assertFalse(column["nullable"])
                self.assertIsNotNone(column["default"])
            await conn.run_sync(check_column)
        from app.api.v1.users import list_users
        from app.models.user import User
        sessions = async_sessionmaker(self.engine, expire_on_commit=False)
        async with sessions() as db:
            response = await list_users(
                org_id=org_id, db=db,
                current_user=User(role="super_admin"), page=1, page_size=100,
            )
            self.assertEqual(response.total, 3)
            self.assertTrue(all(user.updated_at is not None for user in response.items))

    async def test_postgres_queue_concurrency_and_saved_answers(self):
        await self.migrate("head")
        from unittest.mock import AsyncMock
        from app.models.organization import Organization
        from app.models.questionnaire import Questionnaire, QuestionnaireResponse
        from app.models.workflow import WorkflowExecution
        from app.services import questionnaire_jobs as jobs
        from app.schemas.questionnaire import QuestionnaireDetailResponse

        sessions = async_sessionmaker(self.engine, expire_on_commit=False)
        org_id = uuid.uuid4()
        async with sessions() as db:
            db.add(Organization(id=org_id, name="Queue test", slug=str(org_id)))
            await db.flush()
            questionnaire = Questionnaire(org_id=org_id, title="Queue test", questions=[
                {"question_id": "q1", "question_text": "Describe security"}
            ], total_questions=1)
            db.add(questionnaire)
            await db.commit()
            questionnaire_id = questionnaire.id

        async def submit():
            async with sessions() as db:
                return (await jobs.enqueue(db, org_id, questionnaire_id, None)).id

        ids = await asyncio.gather(submit(), submit(), submit())
        self.assertEqual(len(set(ids)), 1)
        with patch.object(jobs, "bg_async_session", sessions):
            claims = await asyncio.gather(jobs.claim_next(), jobs.claim_next())
            claimed = [claim for claim in claims if claim]
            self.assertEqual(len(claimed), 1)
            with patch("app.agents.common.llm.call_llm_json", new=AsyncMock(return_value=(
                {"answers": [{"question_id": "q1", "answer": "Saved answer", "confidence": .9}]}, {}
            ))):
                await jobs.execute_job(*claimed[0])
            async with sessions() as db:
                wf = await db.get(WorkflowExecution, ids[0])
                self.assertEqual(wf.status, "completed", wf.error_message)
                questionnaire = await db.get(Questionnaire, questionnaire_id)
                serialized = QuestionnaireDetailResponse.model_validate(questionnaire)
                self.assertEqual(serialized.responses[0].answer, "Saved answer")
                self.assertIsNotNone(serialized.updated_at)
                self.assertIsNotNone(serialized.responses[0].updated_at)



if __name__ == "__main__":
    unittest.main(verbosity=2)
