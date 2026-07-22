# QuickTrust Architecture

## Overview

QuickTrust is an open-source, agent-first GRC platform. It combines a Next.js application, an async FastAPI API, organization-scoped PostgreSQL data, AWS-compatible object storage, and Bedrock-backed AI workflows.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 15, React 19, Tailwind CSS, Radix UI |
| Backend API | FastAPI, Python 3.12, SQLAlchemy 2.0 async |
| Database | PostgreSQL 16 + pgvector; SQLite for local development/tests |
| Authentication | Application email/password, Argon2id, signed JWT access tokens, rotating refresh sessions |
| Authorization | Database-backed RBAC and organization membership |
| Cache/revocation | Redis 7 |
| Object storage | Amazon S3 in production; MinIO as a local S3-compatible emulator |
| AI | LangGraph + LiteLLM + Anthropic Claude Sonnet on Amazon Bedrock |
| Reverse proxy | Traefik v3 |
| Containers | Docker Compose |

## Runtime Architecture

```text
Browser ── Next.js (3000 container / 3001 host) ── FastAPI (8000) ── PostgreSQL (5432)
                     │                                  ├── Redis (6379)
                     │                                  ├── S3 / local emulator
                     │                                  └── Bedrock Claude Sonnet
                     └── HttpOnly rotating refresh cookie + in-memory access JWT
```

## Authentication Flow

1. The browser submits an email/password to `POST /api/v1/auth/token`, or creates an account through `POST /api/v1/auth/register`.
2. Passwords are hashed with Argon2id; existing users without local password material use the one-time reset flow.
3. FastAPI returns a short-lived HS256 access JWT and sets a rotating opaque refresh token as an HttpOnly, SameSite cookie. Only the refresh-token SHA-256 digest is stored.
4. The frontend keeps the access token in memory, calls `/auth/me`, and attaches the token to protected API requests.
5. `/auth/refresh` rotates the database-backed session. Redis supports immediate access-token revocation on logout, password change, suspension, or sign-out-all.
6. Protected dependencies resolve the JWT subject to the current database user, then enforce the existing role and organization rules from the database.

## AI Controls-Generation Flow

```text
START
  → load_framework_requirements
  → match_templates_to_requirements
  → customize_controls (Claude Sonnet via Bedrock)
  → deduplicate_controls
  → suggest_owners (Claude Sonnet via Bedrock)
  → finalize_output (database drafts)
END
```

## Key Design Decisions

1. Async SQLAlchemy sessions are used throughout the API.
2. Authorization remains database-backed so role and organization changes take effect independently of access-token claims.
3. Access JWTs are deliberately short-lived; refresh secrets are opaque, rotating, HttpOnly, and stored only as hashes.
4. AI calls retain LiteLLM as the compatibility layer while routing only to Bedrock Claude Sonnet.
5. Evidence, generic uploads, screenshots, and rendered reports use boto3 against S3-compatible storage.
6. Production schema changes run through Alembic; local/test startup may use metadata creation.

## Authentication Tables

- `users` — application identity, Argon2id password hash, role, organization, lockout state, and preserved legacy identity identifier
- `auth_sessions` — hashed rotating refresh tokens, client metadata, expiry, and revocation
- `password_reset_tokens` — hashed, expiring, one-time password setup/reset tokens
- `api_keys` — existing scoped API-key authentication
- `invitations` — organization/role invitations

## Directory Structure

```text
backend/app/api/v1/       FastAPI routers
backend/app/core/         configuration, JWT/password security, dependencies
backend/app/models/       SQLAlchemy models
backend/app/services/     business and authentication services
backend/app/agents/       LangGraph workflows
backend/alembic/versions/ schema migrations
frontend/src/app/         Next.js App Router pages
frontend/src/providers/   auth/query/theme context
frontend/src/lib/         API and authentication clients
infra/                    PostgreSQL, Traefik, and operational scripts
```
