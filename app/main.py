from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.base import Base
from app.db.session import engine
from app.routers import airport, flight


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown logic.
    """
    # Startup: create database tables
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown: nothing to clean up yet


app = FastAPI(
    title="Airport Database API",
    lifespan=lifespan,
)


app.include_router(airport.router)
app.include_router(flight.router)


app = FastAPI(
    title="Airport Database API",
    lifespan=lifespan
)

app.include_router(airport.router)
