# S3 Object Storage Migration Plan

## Goal

Move production object storage from MinIO to Amazon S3 while preserving the existing upload/download/delete/presigned-url architecture.

## Current Findings

- `backend/app/core/storage.py` imports and uses the MinIO Python SDK directly.
- `backend/pyproject.toml` already includes `boto3`, so the project can use the AWS S3 API without adding a new dependency.
- Generic file uploads call the storage helper but read the bucket from `settings.MINIO_BUCKET`.
- Evidence uploads and screenshot evidence hardcode `quicktrust-evidence`.
- Report rendering hardcodes `quicktrust-reports`.
- Report downloads bypass the storage helper and call the raw MinIO client.
- Local Docker Compose runs MinIO. Production Docker Compose also runs MinIO and must stop doing that.

## Implementation Steps

1. Add focused tests for S3-compatible upload, download, delete, bucket creation, and presigned URLs.
2. Replace the MinIO SDK in `app/core/storage.py` with a boto3 S3 client while keeping the same helper function names.
3. Add AWS S3 settings and move evidence/report buckets to configuration.
4. Update API and service call sites to use the configured buckets and the storage abstraction.
5. Keep MinIO in local Docker only as an S3-compatible emulator through `S3_ENDPOINT_URL`.
6. Remove MinIO from production Docker Compose.
7. Update env examples and docs for AWS S3 production setup.
8. Run targeted backend tests and grep for remaining MinIO-specific production code.

## Verification

- Targeted storage tests cover uploads, downloads, deletion, bucket creation, and presigned URLs using a fake boto3 client.
- Production hardening tests cover required S3 credentials in production.
- Static search confirms no MinIO SDK imports remain in backend application code.
