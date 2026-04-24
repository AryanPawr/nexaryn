import uuid
from datetime import datetime
from typing import Any, Optional

from app.schemas.common import (
    ActionApprovalStatus,
    ActionExecutionStatus,
    NexarynSchema,
)


class ActionBase(NexarynSchema):
    case_id: uuid.UUID
    device_id: uuid.UUID
    action_type: str
    requested_by: str
    approval_status: ActionApprovalStatus
    execution_status: ActionExecutionStatus
    requested_at: datetime
    executed_at: Optional[datetime] = None
    result_json: dict[str, Any]


class ActionCreate(ActionBase):
    pass


class ActionRead(ActionBase):
    id: uuid.UUID
