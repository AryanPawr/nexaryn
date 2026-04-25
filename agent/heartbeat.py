from __future__ import annotations

from agent.config import AgentConfig
from agent.http_client import post_json
from agent.models import AgentEvent, utc_now_iso


def send_heartbeat(config: AgentConfig) -> dict:
    sent_at = utc_now_iso()
    payload = {
        "agent_id": config.agent_id,
        "device_id": config.require_device_id(),
        "sent_at": sent_at,
    }
    return post_json(f"{config.backend_url}/api/v1/agents/heartbeat", payload)


def heartbeat_event(config: AgentConfig) -> AgentEvent:
    return AgentEvent.create(
        device_id=config.require_device_id(),
        event_type="heartbeat_status",
        category="system",
        severity="info",
        payload={"agent_id": config.agent_id, "status": "ok"},
    )
