import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.finding import FindingRead
from app.services.findings_service import list_findings


router = APIRouter(prefix="/findings", tags=["findings"])


@router.get("", response_model=list[FindingRead])
def get_findings(
    device_id: Optional[uuid.UUID] = None,
    severity: Optional[str] = Query(default=None),
    status: Optional[str] = Query(default=None),
    category: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
) -> list[FindingRead]:
    return list_findings(
        db=db, device_id=device_id, severity=severity, status=status, category=category
    )
