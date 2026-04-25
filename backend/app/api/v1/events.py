import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.redis import get_redis_client
from app.schemas.event import EventRead
from app.schemas.ingest import EventIngestRequest, EventIngestResponse
from app.services.events_service import list_events
from app.services.ingest_service import ingest_events


router = APIRouter(prefix="/events", tags=["events"])


@router.post("/ingest", response_model=EventIngestResponse)
async def ingest_event_batch(
    request: EventIngestRequest, db: Session = Depends(get_db)
) -> EventIngestResponse:
    return await ingest_events(db=db, redis=get_redis_client(), request=request)


@router.get("", response_model=list[EventRead])
def get_events(
    device_id: Optional[uuid.UUID] = None,
    category: Optional[str] = Query(default=None),
    severity: Optional[str] = Query(default=None),
    event_type: Optional[str] = Query(default=None),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> list[EventRead]:
    return list_events(
        db=db,
        device_id=device_id,
        category=category,
        severity=severity,
        event_type=event_type,
        limit=limit,
        offset=offset,
    )
