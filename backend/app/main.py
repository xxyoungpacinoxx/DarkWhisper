from fastapi import FastAPI
from contextlib import asynccontextmanager
from db import init_db
from routers import chat

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    init_db()
    yield
    # Shutdown logic (if needed)

app = FastAPI(lifespan=lifespan)

app.include_router(chat.router)