import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.event import Event


def list_events(
    db: Session,
    device_id: Optional[uuid.UUID] = None,
    category: Optional[str] = None,
    severity: Optional[str] = None,
    event_type: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> list[Event]:
    statement = select(Event)
    if device_id is not None:
        statement = statement.where(Event.device_id == device_id)
    if category is not None:
        statement = statement.where(Event.category == category)
    if severity is not None:
        statement = statement.where(Event.severity == severity)
    if event_type is not None:
        statement = statement.where(Event.event_type == event_type)
    statement = statement.order_by(Event.received_at.desc()).offset(offset).limit(limit)
    return list(db.scalars(statement).all())
