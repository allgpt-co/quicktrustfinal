"""Backup management API endpoints."""

from fastapi import APIRouter, HTTPException

from app.core.dependencies import DB, AdminUser, VerifiedOrgId
from app.services import backup_service

router = APIRouter(
    prefix="/organizations/{org_id}/backups",
    tags=["backups"],
)


@router.get("/status")
async def get_backup_status(
    org_id: VerifiedOrgId, current_user: AdminUser,
):
    """Get latest backup status and history (admin only)."""
    return await backup_service.get_backup_status()


@router.post("/trigger")
async def trigger_backup(
    org_id: VerifiedOrgId, current_user: AdminUser,
):
    """Manually trigger a database backup (admin only)."""
    try:
        result = await backup_service.create_backup()
        return {"message": "Backup completed successfully", "backup": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Backup failed: {str(e)[:300]}")
