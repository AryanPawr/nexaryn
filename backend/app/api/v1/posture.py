import uuid
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.posture import PostureScoreResponse
from app.services.posture_service import calculate_posture_score


router = APIRouter(tags=["posture"])


@router.get("/posture-score", response_model=PostureScoreResponse)
def get_posture_score(
    device_id: Optional[uuid.UUID] = None, db: Session = Depends(get_db)
) -> PostureScoreResponse:
    return calculate_posture_score(db=db, device_id=device_id)
