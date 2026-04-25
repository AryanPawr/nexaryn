from __future__ import annotations

import shutil
import socket
import subprocess
from typing import Optional

from agent.models import AgentEvent


def _service_guess(port: int) -> Optional[str]:
    try:
        return socket.getservbyport(port)
    except OSError:
        return None


def collect(device_id: str) -> list[AgentEvent]:
    ports = []
    try:
        if shutil.which("lsof"):
            output = subprocess.check_output(
                ["lsof", "-nP", "-iTCP", "-sTCP:LISTEN"],
                text=True,
                timeout=10,
            )
            for line in output.splitlines()[1:200]:
                columns = line.split()
                if len(columns) < 9:
                    continue
                endpoint = columns[-1]
                if ":" not in endpoint:
                    continue
                bind_address, port_text = endpoint.rsplit(":", 1)
                try:
                    port = int(port_text)
                except ValueError:
                    continue
                ports.append(
                    {
                        "port": port,
                        "protocol": "tcp",
                        "bind_address": bind_address,
                        "service_guess": _service_guess(port),
                    }
                )
    except Exception as exc:
        ports.append({"error": exc.__class__.__name__, "message": str(exc)})

    return [
        AgentEvent.create(
            device_id=device_id,
            event_type="open_port_snapshot",
            category="network",
            severity="info",
            payload={"ports": ports},
        )
    ]
