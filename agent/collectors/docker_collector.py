from __future__ import annotations

import json
import shutil
import subprocess

from agent.models import AgentEvent


def collect(device_id: str) -> list[AgentEvent]:
    containers = []
    try:
        if shutil.which("docker") is None:
            containers.append({"available": False, "reason": "docker_not_installed"})
        else:
            output = subprocess.check_output(
                ["docker", "ps", "--format", "{{json .}}"],
                text=True,
                timeout=10,
            )
            for line in output.splitlines()[:200]:
                item = json.loads(line)
                containers.append(
                    {
                        "id": item.get("ID"),
                        "name": item.get("Names"),
                        "image": item.get("Image"),
                        "ports": item.get("Ports"),
                        "status": item.get("Status"),
                    }
                )
    except Exception as exc:
        containers.append({"available": False, "error": exc.__class__.__name__, "message": str(exc)})

    return [
        AgentEvent.create(
            device_id=device_id,
            event_type="docker_metadata_snapshot",
            category="container",
            severity="info",
            payload={"containers": containers},
        )
    ]
