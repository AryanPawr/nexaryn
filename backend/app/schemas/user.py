import uuid
from datetime import datetime

from app.schemas.common import NexarynSchema


class UserBase(NexarynSchema):
    email: str
    name: str


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
