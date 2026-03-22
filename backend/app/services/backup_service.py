"""Database backup service.

Manages automated and manual backups with status tracking via Redis.
"""

import asyncio
import logging
import os
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

BACKUP_DIR = os.environ.get("BACKUP_DIR", "/tmp/backups")


async def _run_backup_command() -> dict:
    """Execute pg_dump and return backup metadata."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename = f"quicktrust_{timestamp}.sql.gz"
    filepath = f"{BACKUP_DIR}/{filename}"

    os.makedirs(BACKUP_DIR, exist_ok=True)

    db_url = os.environ.get("DATABASE_URL", "")
    # Parse connection info from DATABASE_URL
    # Format: postgresql+asyncpg://user:pass@host:port/dbname
    import re
    match = re.match(r"postgresql\+?\w*://(\w+):([^@]+)@([^:]+):?(\d+)?/(\w+)", db_url)
    if not match:
        raise ValueError("Cannot parse DATABASE_URL for backup")

    user, password, host, port, dbname = match.groups()
    port = port or "5432"

    env = os.environ.copy()
    env["PGPASSWORD"] = password

    cmd = f'pg_dump -h {host} -p {port} -U {user} -d {dbname} --format=custom | gzip > "{filepath}"'

    proc = await asyncio.create_subprocess_shell(
        cmd,
        env=env,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    _, stderr = await proc.communicate()

    if proc.returncode != 0:
        error = stderr.decode()[:500]
        raise RuntimeError(f"pg_dump failed: {error}")

    # Get file size
    size = os.path.getsize(filepath) if os.path.exists(filepath) else 0

    return {
        "filename": filename,
        "filepath": filepath,
        "size_bytes": size,
        "size_human": _human_size(size),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "completed",
    }


def _human_size(size_bytes: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


async def create_backup() -> dict:
    """Create a database backup and record it in Redis."""
    try:
        from app.core.token_blacklist import get_redis

        # Record start
        r = await get_redis()
        await r.hset("backup:latest", mapping={
            "status": "running",
            "started_at": datetime.now(timezone.utc).isoformat(),
        })

        result = await _run_backup_command()

        # Record success
        await r.hset("backup:latest", mapping={
            "status": "completed",
            "filename": result["filename"],
            "size_bytes": str(result["size_bytes"]),
            "size_human": result["size_human"],
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "error": "",
        })

        # Add to history (keep last 30)
        history_entry = f'{result["timestamp"]}|{result["filename"]}|{result["size_human"]}|completed'
        await r.lpush("backup:history", history_entry)
        await r.ltrim("backup:history", 0, 29)

        logger.info("Backup completed: %s (%s)", result["filename"], result["size_human"])
        return result

    except Exception as exc:
        logger.error("Backup failed: %s", exc)
        try:
            from app.core.token_blacklist import get_redis
            r = await get_redis()
            await r.hset("backup:latest", mapping={
                "status": "failed",
                "error": str(exc)[:500],
                "completed_at": datetime.now(timezone.utc).isoformat(),
            })
        except Exception:
            pass
        raise


async def get_backup_status() -> dict:
    """Get the latest backup status and history."""
    try:
        from app.core.token_blacklist import get_redis
        r = await get_redis()

        latest = await r.hgetall("backup:latest")
        history_raw = await r.lrange("backup:history", 0, 9)

        history = []
        for entry in history_raw:
            parts = entry.split("|")
            if len(parts) >= 4:
                history.append({
                    "timestamp": parts[0],
                    "filename": parts[1],
                    "size": parts[2],
                    "status": parts[3],
                })

        # List local backup files
        local_files = []
        if os.path.isdir(BACKUP_DIR):
            for f in sorted(os.listdir(BACKUP_DIR), reverse=True)[:10]:
                fpath = os.path.join(BACKUP_DIR, f)
                if os.path.isfile(fpath):
                    local_files.append({
                        "filename": f,
                        "size": _human_size(os.path.getsize(fpath)),
                        "modified": datetime.fromtimestamp(
                            os.path.getmtime(fpath), tz=timezone.utc
                        ).isoformat(),
                    })

        return {
            "latest": {
                "status": latest.get("status", "never"),
                "filename": latest.get("filename", ""),
                "size": latest.get("size_human", ""),
                "completed_at": latest.get("completed_at", ""),
                "error": latest.get("error", ""),
            },
            "history": history,
            "local_files": local_files,
            "backup_dir": BACKUP_DIR,
        }
    except Exception as exc:
        logger.warning("Failed to get backup status: %s", exc)
        return {
            "latest": {"status": "unknown", "error": str(exc)[:200]},
            "history": [],
            "local_files": [],
            "backup_dir": BACKUP_DIR,
        }
