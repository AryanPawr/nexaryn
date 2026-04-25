import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.case import CaseDetailRead, CaseRead
from app.services.cases_service import get_case_detail, list_cases


router = APIRouter(prefix="/cases", tags=["cases"])


@router.get("", response_model=list[CaseRead])
def get_cases(
    device_id: Optional[uuid.UUID] = None,
    severity: Optional[str] = Query(default=None),
    status: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
) -> list[CaseRead]:
    return list_cases(db=db, device_id=device_id, severity=severity, status=status)


@router.get("/{case_id}", response_model=CaseDetailRead)
def get_case(case_id: uuid.UUID, db: Session = Depends(get_db)) -> CaseDetailRead:
    return get_case_detail(db=db, case_id=case_id)
