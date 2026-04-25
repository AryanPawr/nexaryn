import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.event import Event
from app.models.finding import Finding


def list_findings(
    db: Session,
    device_id: Optional[uuid.UUID] = None,
    severity: Optional[str] = None,
    status: Optional[str] = None,
    category: Optional[str] = None,
) -> list[Finding]:
    statement = select(Finding)
    if category is not None:
        statement = statement.join(Event, Finding.event_id == Event.id)
        statement = statement.where(Event.category == category)
    if device_id is not None:
        statement = statement.where(Finding.device_id == device_id)
    if severity is not None:
        statement = statement.where(Finding.severity == severity)
    if status is not None:
        statement = statement.where(Finding.status == status)
    return list(db.scalars(statement.order_by(Finding.last_seen_at.desc())).all())
