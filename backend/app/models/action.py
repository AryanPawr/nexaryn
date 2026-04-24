import uuid
from datetime import datetime
from typing import Any, Optional

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.common import (
    ACTION_APPROVAL_STATUS_VALUES,
    ACTION_EXECUTION_STATUS_VALUES,
    UUIDPrimaryKeyMixin,
)


class Action(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "actions"
    __table_args__ = (
        CheckConstraint(
            f"approval_status IN {ACTION_APPROVAL_STATUS_VALUES}",
            name="ck_actions_approval_status",
        ),
        CheckConstraint(
            f"execution_status IN {ACTION_EXECUTION_STATUS_VALUES}",
            name="ck_actions_execution_status",
        ),
    )

    case_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("cases.id"), nullable=False, index=True
    )
    device_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("devices.id"), nullable=False, index=True
    )
    action_type: Mapped[str] = mapped_column(String(128), nullable=False)
    requested_by: Mapped[str] = mapped_column(String(255), nullable=False)
    approval_status: Mapped[str] = mapped_column(String(32), nullable=False)
    execution_status: Mapped[str] = mapped_column(String(32), nullable=False)
    requested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    executed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    result_json: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)

    case = relationship("Case", back_populates="actions")
    device = relationship("Device", back_populates="actions")
