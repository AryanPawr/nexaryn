from fastapi import APIRouter

from app.api.v1 import actions, agents, cases, devices, events, findings, posture


api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(events.router)
api_v1_router.include_router(findings.router)
api_v1_router.include_router(cases.router)
api_v1_router.include_router(posture.router)
api_v1_router.include_router(actions.router)
api_v1_router.include_router(agents.router)
api_v1_router.include_router(devices.router)
