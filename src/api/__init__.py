from fastapi import APIRouter

from .v1 import api_router as API_V1_ROUTER

default_api_router = APIRouter(prefix="/api")
default_api_router.include_router(API_V1_ROUTER, tags=["v1"])


@default_api_router.get("/healthcheck")
async def healthcheck() -> int:
    """
    Точка для проверки доступности системы
    """

    return 1
