from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api import default_api_router as API_ROUTER
from src.background_tasks import sync as sync_bg_task


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Этот тред не закрывается вручную, 
    # поскольку он автоматически уничтожится 
    # после отключения сервера
    sync_bg_task.THREAD.start()
    yield


app = FastAPI(title="BWG Test Task", lifespan=lifespan)

app.include_router(API_ROUTER)
