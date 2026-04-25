from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.device import Device


def list_devices(
    db: Session,
    agent_id: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> list[Device]:
    statement = select(Device)
    if agent_id is not None:
        statement = statement.where(Device.agent_id == agent_id)
    statement = statement.order_by(Device.last_seen_at.desc()).offset(offset).limit(limit)
    return list(db.scalars(statement).all())
