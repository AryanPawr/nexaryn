import uuid
from datetime import datetime
from typing import Any

from app.schemas.common import NexarynSchema, Severity


class EventBase(NexarynSchema):
    device_id: uuid.UUID
    event_type: str
    category: str
    severity: Severity
    occurred_at: datetime
    received_at: datetime
    source: str
    payload_json: dict[str, Any]


class EventCreate(EventBase):
    pass


class EventRead(EventBase):
    id: uuid.UUID
