from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db.base import Base
from app.db.session import engine
from app.routers import airport


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan:
    - startup: create database tables
    - shutdown: clean up resources if needed
    """
    # 🔹 Startup logic
    Base.metadata.create_all(bind=engine)
    yield
    # 🔹 Shutdown logic (пока ничего не нужно)


app = FastAPI(
    title="Airport Database API",
    lifespan=lifespan
)

app.include_router(airport.router)
