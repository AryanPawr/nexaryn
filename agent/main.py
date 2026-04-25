from __future__ import annotations

import argparse
import logging
import time

from agent.collectors import docker_collector, package_collector, port_collector, process_collector
from agent.config import AgentConfig
from agent.heartbeat import heartbeat_event, send_heartbeat
from agent.http_client import BackendRequestError
from agent.registration import register_agent
from agent.retry_queue import RetryQueue
from agent.sender import EventSender


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger("nexaryn.agent")


def collect_all(device_id: str):
    events = []
    for collector in (process_collector, port_collector, package_collector, docker_collector):
        try:
            events.extend(collector.collect(device_id))
        except Exception:
            logger.exception("collector failed: %s", collector.__name__)
    return events


def run_once(config: AgentConfig) -> None:
    if not config.device_id:
        logger.info("registering agent_id=%s", config.agent_id)
        register_agent(config)
    logger.info("sending heartbeat for device_id=%s", config.device_id)
    send_heartbeat(config)

    queue = RetryQueue(config.retry_queue_path)
    sender = EventSender(config, queue)
    retry_sent, retry_failed = sender.retry_failed()
    if retry_sent or retry_failed:
        logger.info("retry queue processed: sent=%s failed=%s", retry_sent, retry_failed)

    events = [heartbeat_event(config), *collect_all(config.require_device_id())]
    try:
        response = sender.send_events(events)
        logger.info("sent events: %s", response)
    except BackendRequestError as exc:
        logger.warning("event send failed; queued for retry: %s", exc)


def main() -> None:
    parser = argparse.ArgumentParser(description="Nexaryn local telemetry agent")
    parser.add_argument("--once", action="store_true", help="Run one registration/heartbeat/collection cycle")
    args = parser.parse_args()

    config = AgentConfig.load()
    if args.once:
        run_once(config)
        return

    while True:
        run_once(config)
        time.sleep(config.heartbeat_interval_seconds)


if __name__ == "__main__":
    main()
