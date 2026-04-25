import uuid
from collections import Counter
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.case import Case
from app.models.finding import Finding
from app.models.common import SEVERITY_VALUES
from app.schemas.posture import PostureScoreResponse


SEVERITY_WEIGHTS = {
    "info": 1,
    "low": 3,
    "medium": 8,
    "high": 18,
    "critical": 30,
}
ACTIVE_CASE_STATUSES = {"open", "investigating", "contained"}


def calculate_posture_score(db: Session, device_id: Optional[uuid.UUID] = None) -> PostureScoreResponse:
    """
    Posture score v1 is intentionally rule-based:
    - Inputs: open findings and active cases, optionally filtered by device_id.
    - Weights: info=1, low=3, medium=8, high=18, critical=30.
    - Active findings are status='open'; active cases are open/investigating/contained.
    - Risk points are the weighted sum of finding counts plus case counts.
    - Output range is 0-100, computed as max(0, 100 - risk_points).
    - Trend is stable in Week 1 because no historical score snapshots exist yet.
    """
    findings_statement = select(Finding).where(Finding.status == "open")
    cases_statement = select(Case).where(Case.status.in_(ACTIVE_CASE_STATUSES))
    if device_id is not None:
        findings_statement = findings_statement.where(Finding.device_id == device_id)
        cases_statement = cases_statement.where(Case.device_id == device_id)

    findings = list(db.scalars(findings_statement).all())
    cases = list(db.scalars(cases_statement).all())
    finding_counts = Counter(finding.severity for finding in findings)
    case_counts = Counter(case.severity for case in cases)
    risk_points = sum(
        SEVERITY_WEIGHTS[severity] * (finding_counts[severity] + case_counts[severity])
        for severity in SEVERITY_VALUES
    )
    overall_score = max(0, min(100, 100 - risk_points))

    drivers = []
    for severity in reversed(SEVERITY_VALUES):
        total = finding_counts[severity] + case_counts[severity]
        if total:
            drivers.append(f"{total} active {severity} item(s)")
    if not drivers:
        drivers.append("No active findings or cases")

    return PostureScoreResponse(
        overall_score=overall_score,
        trend="stable",
        summary_counts={
            "findings": {severity: finding_counts[severity] for severity in SEVERITY_VALUES},
            "cases": {severity: case_counts[severity] for severity in SEVERITY_VALUES},
            "risk_points": risk_points,
        },
        drivers=drivers,
    )
