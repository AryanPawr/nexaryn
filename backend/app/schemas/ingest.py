import uuid
from datetime import datetime
from typing import Any, Optional

from app.schemas.common import NexarynSchema, Severity


class IngestEvent(NexarynSchema):
    event_id: uuid.UUID
    event_type: str
    category: str
    severity: str
    occurred_at: datetime
    source: str
    payload: dict[str, Any]


class EventIngestRequest(NexarynSchema):
    device_id: uuid.UUID
    batch_id: str
    events: list[IngestEvent]


class EventValidationError(NexarynSchema):
    event_id: Optional[uuid.UUID] = None
    index: int
    field: str
    message: str


class EventIngestResponse(NexarynSchema):
    accepted_count: int
    rejected_count: int
    validation_errors: list[EventValidationError]


class QueuedEventPayload(NexarynSchema):
    event_id: uuid.UUID
    device_id: uuid.UUID
    event_type: str
    category: str
    severity: Severity
    occurred_at: datetime
    source: str
    payload_json: dict[str, Any]
