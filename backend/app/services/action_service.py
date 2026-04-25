import uuid
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.action import Action
from app.schemas.action_flow import ActionResponse, ActionResultRequest


def _to_response(action: Action) -> ActionResponse:
    approval_status = "denied" if action.approval_status == "rejected" else action.approval_status
    return ActionResponse(
        id=action.id,
        case_id=action.case_id,
        device_id=action.device_id,
        action_type=action.action_type,
        requested_by=action.requested_by,
        approval_status=approval_status,
        execution_status=action.execution_status,
        requested_at=action.requested_at,
        executed_at=action.executed_at,
        result_json=action.result_json,
    )


def get_action_or_404(db: Session, action_id: uuid.UUID) -> Action:
    action = db.get(Action, action_id)
    if action is None:
        raise HTTPException(
            status_code=404,
            detail={"message": "Action not found.", "action_id": str(action_id)},
        )
    return action


def list_actions(
    db: Session,
    device_id: Optional[uuid.UUID] = None,
    approval_status: Optional[str] = None,
    execution_status: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> list[ActionResponse]:
    statement = select(Action)
    if device_id is not None:
        statement = statement.where(Action.device_id == device_id)
    if approval_status is not None:
        storage_status = "rejected" if approval_status == "denied" else approval_status
        statement = statement.where(Action.approval_status == storage_status)
    if execution_status is not None:
        statement = statement.where(Action.execution_status == execution_status)
    statement = statement.order_by(Action.requested_at.desc()).offset(offset).limit(limit)
    return [_to_response(action) for action in db.scalars(statement).all()]


def approve_action(db: Session, action_id: uuid.UUID) -> ActionResponse:
    action = get_action_or_404(db, action_id)
    if action.approval_status != "pending":
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Action approval_status must be pending.",
                "current_status": action.approval_status,
            },
        )
    action.approval_status = "approved"
    db.commit()
    db.refresh(action)
    return _to_response(action)


def deny_action(db: Session, action_id: uuid.UUID) -> ActionResponse:
    action = get_action_or_404(db, action_id)
    if action.approval_status != "pending":
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Action approval_status must be pending.",
                "current_status": action.approval_status,
            },
        )
    action.approval_status = "rejected"
    db.commit()
    db.refresh(action)
    return _to_response(action)


def store_action_result(db: Session, request: ActionResultRequest) -> ActionResponse:
    action = get_action_or_404(db, request.action_id)
    if action.device_id != request.device_id:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Action does not belong to device.",
                "action_id": str(request.action_id),
                "device_id": str(request.device_id),
            },
        )
    action.execution_status = str(request.execution_status)
    action.result_json = request.result_json
    action.executed_at = request.executed_at
    db.commit()
    db.refresh(action)
    return _to_response(action)
