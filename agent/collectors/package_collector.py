from __future__ import annotations

import shutil
import subprocess

from agent.models import AgentEvent


def collect(device_id: str) -> list[AgentEvent]:
    packages = []
    try:
        if shutil.which("python3"):
            output = subprocess.check_output(
                ["python3", "-m", "pip", "list", "--format=json"],
                text=True,
                timeout=20,
            )
            import json

            for package in json.loads(output)[:300]:
                packages.append(
                    {
                        "name": package.get("name"),
                        "version": package.get("version"),
                        "manager": "pip",
                    }
                )
        elif shutil.which("brew"):
            output = subprocess.check_output(["brew", "list", "--versions"], text=True, timeout=20)
            for line in output.splitlines()[:300]:
                parts = line.split()
                packages.append({"name": parts[0], "version": " ".join(parts[1:]), "manager": "brew"})
    except Exception as exc:
        packages.append({"error": exc.__class__.__name__, "message": str(exc)})

    return [
        AgentEvent.create(
            device_id=device_id,
            event_type="package_inventory_snapshot",
            category="package",
            severity="info",
            payload={"packages": packages},
        )
    ]
