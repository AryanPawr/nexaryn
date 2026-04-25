from fastapi import APIRouter

from app.api.v1.router import api_v1_router
from app.api.routes.health import router as health_router


api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(api_v1_router)
