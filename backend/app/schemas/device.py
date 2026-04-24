import uuid
from datetime import datetime

from app.schemas.common import NexarynSchema


class DeviceBase(NexarynSchema):
    user_id: uuid.UUID
    agent_id: str
    hostname: str
    os_name: str
    os_version: str
    agent_version: str
    last_seen_at: datetime


class DeviceCreate(DeviceBase):
    pass


class DeviceRead(DeviceBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
