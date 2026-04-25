from __future__ import annotations

import json
import os
import socket
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional


DEFAULT_CONFIG_PATH = Path(os.environ.get("NEXARYN_AGENT_CONFIG", "agent_config.json"))


@dataclass
class AgentConfig:
    backend_url: str
    agent_id: str
    device_id: Optional[str]
    heartbeat_interval_seconds: int
    retry_max_attempts: int
    agent_version: str
    config_path: Path
    retry_queue_path: Path

    @classmethod
    def load(cls, path: Optional[Path] = None) -> "AgentConfig":
        config_path = path or DEFAULT_CONFIG_PATH
        data = {}
        if config_path.exists():
            data = json.loads(config_path.read_text())

        backend_url = os.environ.get("NEXARYN_BACKEND_URL", data.get("backend_url", "http://localhost:18000"))
        agent_id = os.environ.get("NEXARYN_AGENT_ID", data.get("agent_id", f"agent-{socket.gethostname()}-{uuid.uuid4()}"))
        device_id = os.environ.get("NEXARYN_DEVICE_ID", data.get("device_id"))
        heartbeat_interval_seconds = int(
            os.environ.get(
                "NEXARYN_HEARTBEAT_INTERVAL_SECONDS",
                data.get("heartbeat_interval_seconds", 60),
            )
        )
        retry_max_attempts = int(os.environ.get("NEXARYN_RETRY_MAX_ATTEMPTS", data.get("retry_max_attempts", 3)))
        agent_version = os.environ.get("NEXARYN_AGENT_VERSION", data.get("agent_version", "0.1.0"))
        retry_queue_path = Path(
            os.environ.get("NEXARYN_RETRY_QUEUE_PATH", data.get("retry_queue_path", "agent_retry_queue.jsonl"))
        )

        return cls(
            backend_url=backend_url.rstrip("/"),
            agent_id=agent_id,
            device_id=device_id,
            heartbeat_interval_seconds=heartbeat_interval_seconds,
            retry_max_attempts=retry_max_attempts,
            agent_version=agent_version,
            config_path=config_path,
            retry_queue_path=retry_queue_path,
        )

    def save(self) -> None:
        data = asdict(self)
        data["config_path"] = str(self.config_path)
        data["retry_queue_path"] = str(self.retry_queue_path)
        self.config_path.write_text(json.dumps(data, indent=2, sort_keys=True))

    def require_device_id(self) -> str:
        if not self.device_id:
            raise RuntimeError("Agent is not registered; device_id is missing")
        return self.device_id
