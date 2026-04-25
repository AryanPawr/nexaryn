import uuid
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.case import Case
from app.models.finding import Finding
from app.schemas.case import CaseDetailRead


def list_cases(
    db: Session,
    device_id: Optional[uuid.UUID] = None,
    severity: Optional[str] = None,
    status: Optional[str] = None,
) -> list[Case]:
    statement = select(Case)
    if device_id is not None:
        statement = statement.where(Case.device_id == device_id)
    if severity is not None:
        statement = statement.where(Case.severity == severity)
    if status is not None:
        statement = statement.where(Case.status == status)
    return list(db.scalars(statement.order_by(Case.updated_at.desc())).all())


def get_case_detail(db: Session, case_id: uuid.UUID) -> CaseDetailRead:
    case = db.get(Case, case_id)
    if case is None:
        raise HTTPException(
            status_code=404,
            detail={"message": "Case not found.", "case_id": str(case_id)},
        )

    finding_ids = case.metadata_json.get("finding_ids", []) if case.metadata_json else []
    findings_statement = select(Finding).where(Finding.device_id == case.device_id)
    if finding_ids:
        findings_statement = findings_statement.where(Finding.id.in_(finding_ids))
    findings = list(db.scalars(findings_statement.order_by(Finding.last_seen_at.desc())).all())

    return CaseDetailRead(
        id=case.id,
        device_id=case.device_id,
        title=case.title,
        summary=case.summary,
        severity=case.severity,
        status=case.status,
        opened_at=case.opened_at,
        updated_at=case.updated_at,
        metadata_json=case.metadata_json,
        findings=findings,
    )
