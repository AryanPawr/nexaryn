from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.agent import (
    AgentHeartbeatRequest,
    AgentHeartbeatResponse,
    AgentRegisterRequest,
    AgentRegisterResponse,
)
from app.services.agent_service import heartbeat_agent, register_agent


router = APIRouter(prefix="/agents", tags=["agents"])


@router.post("/register", response_model=AgentRegisterResponse)
def register(
    request: AgentRegisterRequest, db: Session = Depends(get_db)
) -> AgentRegisterResponse:
    return register_agent(db=db, request=request)


@router.post("/heartbeat", response_model=AgentHeartbeatResponse)
def heartbeat(
    request: AgentHeartbeatRequest, db: Session = Depends(get_db)
) -> AgentHeartbeatResponse:
    return heartbeat_agent(db=db, request=request)
