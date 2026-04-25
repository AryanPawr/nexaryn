import uuid
from datetime import datetime

from app.schemas.common import NexarynSchema


class AgentRegisterRequest(NexarynSchema):
    agent_id: str
    hostname: str
    os_name: str
    os_version: str
    agent_version: str


class AgentRegisterResponse(NexarynSchema):
    device_id: uuid.UUID


class AgentHeartbeatRequest(NexarynSchema):
    agent_id: str
    device_id: uuid.UUID
    sent_at: datetime


class AgentHeartbeatResponse(NexarynSchema):
    success: bool
    device_id: uuid.UUID
    last_seen_at: datetime
