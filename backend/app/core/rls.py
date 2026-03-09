"""Row-Level Security session variable hook.

Before each SQL statement on PostgreSQL, this sets the ``app.current_org``
session variable so that RLS policies can filter rows by tenant.  On SQLite
(dev) it is a no-op.
"""

from __future__ import annotations

from sqlalchemy import event, text
from sqlalchemy.orm import Session

from app.core.request_context import current_org_var


def _set_rls_var(session, _transaction, connection):
    """SQLAlchemy ``after_begin`` event: set the RLS session variable."""
    if connection.dialect.name != "postgresql":
        return
    org_id = current_org_var.get("")
    if org_id:
        connection.execute(text(f"SET LOCAL app.current_org = '{org_id}'"))


def register_rls_hook() -> None:
    """Register the RLS session variable hook on the sync Session class.

    SQLAlchemy's AsyncSession delegates to a sync Session internally,
    so events registered on Session propagate to async usage.
    """
    event.listen(Session, "after_begin", _set_rls_var)
