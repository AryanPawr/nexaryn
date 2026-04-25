from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class RetryQueue:
    def __init__(self, path: Path):
        self.path = path

    def enqueue_batch(self, batch: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(batch) + "\n")

    def load_batches(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        batches: list[dict[str, Any]] = []
        with self.path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if line:
                    batches.append(json.loads(line))
        return batches

    def replace_batches(self, batches: list[dict[str, Any]]) -> None:
        if not batches:
            if self.path.exists():
                self.path.unlink()
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as handle:
            for batch in batches:
                handle.write(json.dumps(batch) + "\n")
