import asyncio
import json
import uuid
from datetime import datetime
from typing import Any, Optional

from app.core.database import SessionLocal
from app.core.redis import close_redis_client, get_redis_client
from app.models.finding import Finding
from app.services.ingest_service import INGEST_QUEUE_NAME


FINDING_RULES = {
    "malware_alert": ("malware_detected", "Malware alert observed"),
    "vulnerability_detected": ("vulnerability_detected", "Vulnerability detected"),
    "login_failure": ("authentication_anomaly", "Repeated login failure observed"),
}


def _parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value)


def build_finding_candidate(payload: dict[str, Any]) -> Optional[Finding]:
    finding_type, title = FINDING_RULES.get(payload["event_type"], (None, None))
    if finding_type is None and payload["severity"] not in {"high", "critical"}:
        return None

    event_time = _parse_datetime(payload["occurred_at"])
    return Finding(
        id=uuid.uuid4(),
        device_id=uuid.UUID(payload["device_id"]),
        event_id=uuid.UUID(payload["event_id"]),
        finding_type=finding_type or "high_severity_event",
        title=title or "High severity event observed",
        description=f"Rule-based finding generated from {payload['event_type']}.",
        severity=payload["severity"],
        status="open",
        first_seen_at=event_time,
        last_seen_at=event_time,
        metadata_json={
            "source": "ingest_worker",
            "rule": finding_type or "high_severity_event",
            "event_type": payload["event_type"],
            "category": payload["category"],
        },
    )


async def process_one_queued_event() -> bool:
    redis = get_redis_client()
    raw_payload = await redis.lpop(INGEST_QUEUE_NAME)
    if raw_payload is None:
        return False

    payload = json.loads(raw_payload)
    finding = build_finding_candidate(payload)
    if finding is None:
        return True

    with SessionLocal() as db:
        db.add(finding)
        db.commit()
    return True


async def run_worker() -> None:
    try:
        while True:
            processed = await process_one_queued_event()
            if not processed:
                await asyncio.sleep(2)
    finally:
        await close_redis_client()


def main() -> None:
    asyncio.run(run_worker())


if __name__ == "__main__":
    main()
