import json
from datetime import timezone
from typing import Any

from redis.asyncio import Redis
from sqlalchemy.orm import Session

from app.core.database import utc_now
from app.models.device import Device
from app.models.event import Event
from app.models.common import SEVERITY_VALUES
from app.schemas.ingest import EventIngestRequest, EventIngestResponse, EventValidationError


INGEST_QUEUE_NAME = "nexaryn:ingest:events"
ALLOWED_EVENT_TYPES = {
    "process_snapshot",
    "open_port_snapshot",
    "package_inventory_snapshot",
    "docker_metadata_snapshot",
    "secret_exposure_detected",
    "config_risk_detected",
    "heartbeat_status",
    "process_start",
    "process_stop",
    "network_connection",
    "file_change",
    "login_success",
    "login_failure",
    "malware_alert",
    "vulnerability_detected",
    "configuration_change",
}
ALLOWED_CATEGORIES = {
    "process",
    "network",
    "package",
    "container",
    "secret",
    "config",
    "system",
    "file",
    "auth",
    "endpoint",
    "security",
}


def _utc(value):
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _validate_event(index: int, event) -> list[EventValidationError]:
    errors: list[EventValidationError] = []
    if event.event_type not in ALLOWED_EVENT_TYPES:
        errors.append(
            EventValidationError(
                event_id=event.event_id,
                index=index,
                field="event_type",
                message=f"Unknown event_type '{event.event_type}'.",
            )
        )
    if event.category not in ALLOWED_CATEGORIES:
        errors.append(
            EventValidationError(
                event_id=event.event_id,
                index=index,
                field="category",
                message=f"Unknown category '{event.category}'.",
            )
        )
    if event.severity not in SEVERITY_VALUES:
        errors.append(
            EventValidationError(
                event_id=event.event_id,
                index=index,
                field="severity",
                message=f"Unknown severity '{event.severity}'.",
            )
        )
    return errors


async def ingest_events(
    db: Session, redis: Redis, request: EventIngestRequest
) -> EventIngestResponse:
    device = db.get(Device, request.device_id)
    if device is None:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=404,
            detail={"message": "Device not found.", "device_id": str(request.device_id)},
        )

    validation_errors: list[EventValidationError] = []
    accepted_events: list[Event] = []
    queue_payloads: list[dict[str, Any]] = []
    seen_event_ids: set[str] = set()

    for index, ingest_event in enumerate(request.events):
        event_errors = _validate_event(index, ingest_event)
        event_id_key = str(ingest_event.event_id)
        if event_id_key in seen_event_ids or db.get(Event, ingest_event.event_id) is not None:
            event_errors.append(
                EventValidationError(
                    event_id=ingest_event.event_id,
                    index=index,
                    field="event_id",
                    message=f"Duplicate event_id '{ingest_event.event_id}'.",
                )
            )
        validation_errors.extend(event_errors)
        if event_errors:
            continue
        seen_event_ids.add(event_id_key)

        event = Event(
            id=ingest_event.event_id,
            device_id=request.device_id,
            event_type=ingest_event.event_type,
            category=ingest_event.category,
            severity=ingest_event.severity,
            occurred_at=_utc(ingest_event.occurred_at),
            received_at=utc_now(),
            source=ingest_event.source,
            payload_json={
                **ingest_event.payload,
                "_ingest": {"batch_id": request.batch_id},
            },
        )
        accepted_events.append(event)
        queue_payloads.append(
            {
                "event_id": str(event.id),
                "device_id": str(event.device_id),
                "event_type": event.event_type,
                "category": event.category,
                "severity": event.severity,
                "occurred_at": event.occurred_at.isoformat(),
                "source": event.source,
                "payload_json": event.payload_json,
            }
        )

    if accepted_events:
        db.add_all(accepted_events)
        db.commit()
        for payload in queue_payloads:
            await redis.rpush(INGEST_QUEUE_NAME, json.dumps(payload))

    return EventIngestResponse(
        accepted_count=len(accepted_events),
        rejected_count=len(request.events) - len(accepted_events),
        validation_errors=validation_errors,
    )
