from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.core.redis import get_redis_client


router = APIRouter(tags=["health"])


@router.get("/health")
async def health(db: Session = Depends(get_db)) -> dict[str, Any]:
    settings = get_settings()
    database = {"status": "ok"}
    redis = {"status": "ok"}

    try:
        db.execute(text("SELECT 1")).scalar_one()
    except Exception as exc:  # pragma: no cover - exercised by integration checks
        database = {"status": "error", "error": exc.__class__.__name__}

    try:
        await get_redis_client().ping()
    except Exception as exc:  # pragma: no cover - exercised by integration checks
        redis = {"status": "error", "error": exc.__class__.__name__}

    service_status = "ok" if database["status"] == "ok" and redis["status"] == "ok" else "degraded"
    return {
        "service": settings.service_name,
        "status": service_status,
        "database": database,
        "redis": redis,
    }
