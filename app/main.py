from fastapi import FastAPI

from app.db.base import Base
from app.db.session import engine
from app.routers import airport

app = FastAPI(title="Airport Database API")


@app.on_event("startup")
def on_startup():
    """
    Create database tables on application startup.
    """
    Base.metadata.create_all(bind=engine)


app.include_router(airport.router)
