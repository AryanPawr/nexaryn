from __future__ import annotations

import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Optional


APPROVED_EVENT_TYPES = {
    "process_snapshot",
    "open_port_snapshot",
    "package_inventory_snapshot",
    "docker_metadata_snapshot",
    "secret_exposure_detected",
    "config_risk_detected",
    "heartbeat_status",
}
APPROVED_CATEGORIES = {"process", "network", "package", "container", "secret", "config", "system"}
APPROVED_SEVERITIES = {"info", "low", "medium", "high", "critical"}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class AgentEvent:
    event_id: str
    device_id: str
    event_type: str
    category: str
    severity: str
    occurred_at: str
    source: str
    payload: dict[str, Any]

    @classmethod
    def create(
        cls,
        device_id: str,
        event_type: str,
        category: str,
        severity: str,
        payload: dict[str, Any],
        occurred_at: Optional[str] = None,
    ) -> "AgentEvent":
        event = cls(
            event_id=str(uuid.uuid4()),
            device_id=device_id,
            event_type=event_type,
            category=category,
            severity=severity,
            occurred_at=occurred_at or utc_now_iso(),
            source="agent",
            payload=payload,
        )
        event.validate()
        return event

    def validate(self) -> None:
        if self.event_type not in APPROVED_EVENT_TYPES:
            raise ValueError(f"Unsupported event_type: {self.event_type}")
        if self.category not in APPROVED_CATEGORIES:
            raise ValueError(f"Unsupported category: {self.category}")
        if self.severity not in APPROVED_SEVERITIES:
            raise ValueError(f"Unsupported severity: {self.severity}")
        if self.source != "agent":
            raise ValueError("source must be 'agent'")
        uuid.UUID(self.event_id)
        uuid.UUID(self.device_id)
        datetime.fromisoformat(self.occurred_at)

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        return asdict(self)
