import uuid
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import utc_now


class UUIDPrimaryKeyMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, sort_order=-100
    )


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False, sort_order=1000
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
        sort_order=1001,
    )


SEVERITY_VALUES = ("info", "low", "medium", "high", "critical")
FINDING_STATUS_VALUES = ("open", "triaged", "resolved", "ignored")
CASE_STATUS_VALUES = ("open", "investigating", "contained", "resolved", "closed")
ACTION_APPROVAL_STATUS_VALUES = ("pending", "approved", "rejected")
ACTION_EXECUTION_STATUS_VALUES = ("pending", "running", "succeeded", "failed", "cancelled")
