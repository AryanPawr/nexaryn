from __future__ import annotations

import platform
import socket

from agent.config import AgentConfig
from agent.http_client import post_json


def register_agent(config: AgentConfig) -> str:
    payload = {
        "agent_id": config.agent_id,
        "hostname": socket.gethostname(),
        "os_name": platform.system() or "unknown",
        "os_version": platform.version() or "unknown",
        "agent_version": config.agent_version,
    }
    response = post_json(f"{config.backend_url}/api/v1/agents/register", payload)
    device_id = response["device_id"]
    config.device_id = device_id
    config.save()
    return device_id
