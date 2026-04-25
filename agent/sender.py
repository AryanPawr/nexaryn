from __future__ import annotations

import uuid
from typing import Iterable

from agent.config import AgentConfig
from agent.http_client import BackendRequestError, post_json
from agent.models import AgentEvent
from agent.retry_queue import RetryQueue


class EventSender:
    def __init__(self, config: AgentConfig, retry_queue: RetryQueue):
        self.config = config
        self.retry_queue = retry_queue

    def _batch(self, events: Iterable[AgentEvent]) -> dict:
        device_id = self.config.require_device_id()
        return {
            "device_id": device_id,
            "batch_id": str(uuid.uuid4()),
            "events": [event.to_dict() for event in events],
        }

    def send_events(self, events: Iterable[AgentEvent]) -> dict:
        batch = self._batch(events)
        if not batch["events"]:
            return {"accepted_count": 0, "rejected_count": 0, "validation_errors": []}
        try:
            return post_json(f"{self.config.backend_url}/api/v1/events/ingest", batch)
        except BackendRequestError:
            batch["_retry_attempts"] = 0
            self.retry_queue.enqueue_batch(batch)
            raise

    def retry_failed(self) -> tuple[int, int]:
        queued = self.retry_queue.load_batches()
        remaining = []
        sent = 0
        failed = 0
        for batch in queued:
            attempts = int(batch.get("_retry_attempts", 0))
            clean_batch = {key: value for key, value in batch.items() if key != "_retry_attempts"}
            try:
                post_json(f"{self.config.backend_url}/api/v1/events/ingest", clean_batch)
                sent += len(clean_batch.get("events", []))
            except BackendRequestError:
                failed += len(clean_batch.get("events", []))
                attempts += 1
                if attempts < self.config.retry_max_attempts:
                    batch["_retry_attempts"] = attempts
                    remaining.append(batch)
        self.retry_queue.replace_batches(remaining)
        return sent, failed
