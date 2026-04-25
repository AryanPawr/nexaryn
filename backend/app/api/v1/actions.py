import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.action_flow import ActionResponse, ActionResultRequest
from app.services.action_service import approve_action, deny_action, list_actions, store_action_result


router = APIRouter(prefix="/actions", tags=["actions"])


@router.get("", response_model=list[ActionResponse])
def get_actions(
    device_id: Optional[uuid.UUID] = None,
    approval_status: Optional[str] = Query(default=None),
    execution_status: Optional[str] = Query(default=None),
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> list[ActionResponse]:
    return list_actions(
        db=db,
        device_id=device_id,
        approval_status=approval_status,
        execution_status=execution_status,
        limit=limit,
        offset=offset,
    )


@router.post("/{action_id}/approve", response_model=ActionResponse)
def approve(action_id: uuid.UUID, db: Session = Depends(get_db)) -> ActionResponse:
    return approve_action(db=db, action_id=action_id)


@router.post("/{action_id}/deny", response_model=ActionResponse)
def deny(action_id: uuid.UUID, db: Session = Depends(get_db)) -> ActionResponse:
    return deny_action(db=db, action_id=action_id)


@router.post("/result", response_model=ActionResponse)
def result(request: ActionResultRequest, db: Session = Depends(get_db)) -> ActionResponse:
    return store_action_result(db=db, request=request)
