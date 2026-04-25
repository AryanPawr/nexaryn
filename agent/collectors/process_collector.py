from __future__ import annotations

import subprocess

from agent.models import AgentEvent


def collect(device_id: str) -> list[AgentEvent]:
    processes = []
    try:
        output = subprocess.check_output(["ps", "-axo", "pid=,comm=,args="], text=True, timeout=10)
        for line in output.splitlines()[:200]:
            parts = line.strip().split(None, 2)
            if len(parts) >= 2:
                processes.append(
                    {
                        "pid": int(parts[0]),
                        "name": parts[1],
                        "cmdline": parts[2] if len(parts) > 2 else "",
                    }
                )
    except Exception as exc:
        processes.append({"error": exc.__class__.__name__, "message": str(exc)})

    return [
        AgentEvent.create(
            device_id=device_id,
            event_type="process_snapshot",
            category="process",
            severity="info",
            payload={"processes": processes},
        )
    ]
