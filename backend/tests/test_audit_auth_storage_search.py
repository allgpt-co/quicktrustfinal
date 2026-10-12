"""QT-001/002/003: persistent regression coverage for the local audit checks."""
import time
from uuid import uuid4
from unittest.mock import AsyncMock, Mock

import pytest
from jose import jwt

from app.main import app
from app.core.dependencies import get_current_user
from app.core import security
from app.api.v1 import files
from app.models.embedding import Embedding
from app.services import embedding_service
from tests.conftest import make_test_user_with_role, override_get_current_user


@pytest.mark.asyncio
async def test_protected_endpoint_rejects_missing_malformed_forged_expired_tokens(client, monkeypatch):
    monkeypatch.setattr(security.settings, "SECRET_KEY", "local-test-signing-secret-at-least-32-characters")
    now = int(time.time())
    claims = dict(sub=str(uuid4()), iat=now-120, exp=now+300, type="access",
                  iss=security.settings.JWT_ISSUER, aud=security.settings.JWT_AUDIENCE)
    cases = [
        (None, "Missing or invalid authorization"),
        ("invalid", "Not enough segments"),
        (jwt.encode(claims, "wrong-secret", algorithm="HS256"), "Signature verification failed"),
        (jwt.encode({**claims, "exp": now-60}, security.settings.SECRET_KEY, algorithm="HS256"), "Signature has expired"),
    ]
    app.dependency_overrides.pop(get_current_user, None)
    try:
        for token, detail in cases:
            response = await client.get("/api/v1/frameworks", headers={"Authorization": f"Bearer {token}"} if token else {})
            assert response.status_code == 401
            assert detail in response.text
    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user


@pytest.mark.asyncio
async def test_file_access_tenant_bucket_and_prefix_boundaries(client, monkeypatch):
    org_a, org_b = uuid4(), uuid4()
    async def user():
        return make_test_user_with_role("employee", org_a)
    app.dependency_overrides[get_current_user] = user
    signer = Mock(return_value="https://example.invalid/file")
    deleter = Mock()
    uploader = Mock(return_value="mock/path")
    monkeypatch.setattr(files, "get_presigned_url", signer)
    monkeypatch.setattr(files, "delete_file", deleter)
    monkeypatch.setattr(files, "upload_file", uploader)
    bucket = files.get_settings().S3_BUCKET
    try:
        for org, path, expected in [
            (org_a, f"{bucket}/{org_a}/test.txt", 307),
            (org_b, f"{bucket}/{org_b}/test.txt", 403),
            (org_a, f"{bucket}/{org_b}/test.txt", 403),
            (org_a, f"other-bucket/{org_a}/test.txt", 403),
            (org_a, f"{bucket}/{org_a}-suffix/test.txt", 403),
            (org_a, "malformed", 400),
        ]:
            signer.reset_mock()
            response = await client.get(f"/api/v1/organizations/{org}/files/test/download", params={"object_path": path})
            assert response.status_code == expected
            assert signer.called == (expected == 307)
            deleter.reset_mock()
            response = await client.delete(f"/api/v1/organizations/{org}/files/test", params={"object_path": path})
            assert response.status_code == (200 if expected == 307 else expected)
            assert deleter.called == (expected == 307)
        for org, expected in [(org_a, 201), (org_b, 403)]:
            uploader.reset_mock()
            response = await client.post(f"/api/v1/organizations/{org}/files/upload", files={"file": ("test.txt", b"test", "text/plain")})
            assert response.status_code == expected
            assert uploader.called == (expected == 201)
    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user


@pytest.mark.asyncio
async def test_search_route_and_data_isolation(client, db, monkeypatch):
    org_a, org_b, empty = uuid4(), uuid4(), uuid4()
    ids = [uuid4(), uuid4()]
    for org, entity in zip([org_a, org_b], ids):
        db.add(Embedding(org_id=org, entity_id=entity, entity_type="policy", content_hash=entity.hex,
                         text_content="Private policy", vector=[1., 0.], dimensions=2))
    await db.commit()
    monkeypatch.setattr(embedding_service, "_compute_embedding", lambda text: [1., 0.])
    for org, expected in [(org_a, [str(ids[0])]), (org_b, [str(ids[1])]), (empty, [])]:
        results = await embedding_service.search_similar(db, org, "policy", min_score=0.)
        assert [row["entity_id"] for row in results] == expected
    async def user():
        return make_test_user_with_role("employee", org_a)
    app.dependency_overrides[get_current_user] = user
    search = AsyncMock(return_value=[])
    monkeypatch.setattr(embedding_service, "search_similar", search)
    try:
        for org, expected in [(org_a, 200), (org_b, 403)]:
            search.reset_mock()
            response = await client.post(f"/api/v1/organizations/{org}/embeddings/search", json={"query": "policy"})
            assert response.status_code == expected
            assert search.called == (expected == 200)
            if search.called:
                assert search.call_args.args[1] == org_a
    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user
