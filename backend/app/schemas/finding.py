import uuid
from datetime import datetime
from typing import Any, Optional

from app.schemas.common import FindingStatus, NexarynSchema, Severity


class FindingBase(NexarynSchema):
    device_id: uuid.UUID
    event_id: Optional[uuid.UUID] = None
    finding_type: str
    title: str
    description: str
    severity: Severity
    status: FindingStatus
    first_seen_at: datetime
    last_seen_at: datetime
    metadata_json: dict[str, Any]


class FindingCreate(FindingBase):
    pass


class FindingRead(FindingBase):
    id: uuid.UUID
