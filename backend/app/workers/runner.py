import asyncio

from app.core.config import get_settings
from app.core.redis import close_redis_client, get_redis_client


async def run_worker() -> None:
    settings = get_settings()
    redis = get_redis_client()
    while True:
        await redis.ping()
        print(f"{settings.service_name} worker heartbeat", flush=True)
        await asyncio.sleep(30)


def main() -> None:
    try:
        asyncio.run(run_worker())
    finally:
        asyncio.run(close_redis_client())


if __name__ == "__main__":
    main()
