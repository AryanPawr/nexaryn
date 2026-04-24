from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings
from app.core.redis import close_redis_client


settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    try:
        yield
    finally:
        await close_redis_client()


app = FastAPI(title=settings.service_name, version=settings.api_version, lifespan=lifespan)
app.include_router(api_router)
