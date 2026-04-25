import uuid
from datetime import datetime
from typing import Any, Optional

from app.schemas.common import ActionExecutionStatus, NexarynSchema


class ActionResponse(NexarynSchema):
    id: uuid.UUID
    case_id: uuid.UUID
    device_id: uuid.UUID
    action_type: str
    requested_by: str
    approval_status: str
    execution_status: ActionExecutionStatus
    requested_at: datetime
    executed_at: Optional[datetime] = None
    result_json: dict[str, Any]


class ActionResultRequest(NexarynSchema):
    action_id: uuid.UUID
    device_id: uuid.UUID
    execution_status: ActionExecutionStatus
    result_json: dict[str, Any]
    executed_at: datetime
