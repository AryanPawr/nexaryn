import uuid
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import utc_now
from app.models.device import Device
from app.models.user import User
from app.schemas.agent import (
    AgentHeartbeatRequest,
    AgentHeartbeatResponse,
    AgentRegisterRequest,
    AgentRegisterResponse,
)


AGENT_SYSTEM_USER_ID = uuid.uuid5(uuid.NAMESPACE_DNS, "nexaryn.local.agent-system-user")
AGENT_SYSTEM_USER_EMAIL = "agents@nexaryn.local"


def _as_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _get_or_create_agent_user(db: Session) -> User:
    user = db.get(User, AGENT_SYSTEM_USER_ID)
    if user is not None:
        return user

    user = User(
        id=AGENT_SYSTEM_USER_ID,
        email=AGENT_SYSTEM_USER_EMAIL,
        name="Nexaryn Agent System",
        created_at=utc_now(),
        updated_at=utc_now(),
    )
    db.add(user)
    db.flush()
    return user


def register_agent(db: Session, request: AgentRegisterRequest) -> AgentRegisterResponse:
    user = _get_or_create_agent_user(db)
    device = db.scalar(select(Device).where(Device.agent_id == request.agent_id))
    now = utc_now()

    if device is None:
        device = Device(
            id=uuid.uuid4(),
            user_id=user.id,
            agent_id=request.agent_id,
            hostname=request.hostname,
            os_name=request.os_name,
            os_version=request.os_version,
            agent_version=request.agent_version,
            last_seen_at=now,
            created_at=now,
            updated_at=now,
        )
        db.add(device)
    else:
        device.hostname = request.hostname
        device.os_name = request.os_name
        device.os_version = request.os_version
        device.agent_version = request.agent_version
        device.last_seen_at = now

    db.commit()
    db.refresh(device)
    return AgentRegisterResponse(device_id=device.id)


def heartbeat_agent(db: Session, request: AgentHeartbeatRequest) -> AgentHeartbeatResponse:
    device = db.get(Device, request.device_id)
    if device is None:
        raise HTTPException(
            status_code=404,
            detail={"message": "Device not found.", "device_id": str(request.device_id)},
        )
    if device.agent_id != request.agent_id:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "agent_id does not match device.",
                "device_id": str(request.device_id),
            },
        )

    device.last_seen_at = _as_utc(request.sent_at)
    db.commit()
    db.refresh(device)
    return AgentHeartbeatResponse(success=True, device_id=device.id, last_seen_at=device.last_seen_at)
