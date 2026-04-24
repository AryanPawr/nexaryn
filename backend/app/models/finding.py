import uuid
from datetime import datetime
from typing import Any, Optional

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.common import FINDING_STATUS_VALUES, SEVERITY_VALUES, UUIDPrimaryKeyMixin


class Finding(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "findings"
    __table_args__ = (
        CheckConstraint(f"severity IN {SEVERITY_VALUES}", name="ck_findings_severity"),
        CheckConstraint(f"status IN {FINDING_STATUS_VALUES}", name="ck_findings_status"),
    )

    device_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("devices.id"), nullable=False, index=True
    )
    event_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("events.id"), nullable=True, index=True
    )
    finding_type: Mapped[str] = mapped_column(String(128), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(16), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    first_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)

    device = relationship("Device", back_populates="findings")
    event = relationship("Event", back_populates="findings")
