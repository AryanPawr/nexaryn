import uuid
from datetime import datetime
from typing import Any

from app.schemas.common import CaseStatus, NexarynSchema, Severity
from app.schemas.finding import FindingRead


class CaseBase(NexarynSchema):
    device_id: uuid.UUID
    title: str
    summary: str
    severity: Severity
    status: CaseStatus
    opened_at: datetime
    updated_at: datetime
    metadata_json: dict[str, Any]


class CaseCreate(CaseBase):
    pass


class CaseRead(CaseBase):
    id: uuid.UUID


class CaseDetailRead(CaseRead):
    findings: list[FindingRead]
