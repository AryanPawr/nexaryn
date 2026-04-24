import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.common import CASE_STATUS_VALUES, SEVERITY_VALUES, UUIDPrimaryKeyMixin


class Case(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "cases"
    __table_args__ = (
        CheckConstraint(f"severity IN {SEVERITY_VALUES}", name="ck_cases_severity"),
        CheckConstraint(f"status IN {CASE_STATUS_VALUES}", name="ck_cases_status"),
    )

    device_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("devices.id"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(16), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    opened_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)

    device = relationship("Device", back_populates="cases")
    actions = relationship("Action", back_populates="case")
