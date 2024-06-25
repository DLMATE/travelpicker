from contextlib import asynccontextmanager
from typing import Union

from fastapi import FastAPI

from .router import *
from .utils import common_response
from config import *


@asynccontextmanager
async def lifespan(app: FastAPI):
    AppConfig.setup()
    GoogleConfig.setup(AppConfig.HOST, AppConfig.PORT)
    AuthConfig.setup()
    # SqlConnector.connect(url="sqlite+aiosqlite:///saved/database.db")
    # await SqlConnector.setup()
    yield
    # SqlConnector.disconnect()


app = FastAPI(lifespan=lifespan, responses=common_response())
app.include_router(auth_router)
app.include_router(test_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}