from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.base import Base
from app.db.session import engine
from app.routers import airport, flight, aircraft, passenger, ticket, boarding_pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── startup: create table if doesn't exist ──
    Base.metadata.create_all(bind=engine)
    yield
    # ── shutdown: here it's possible to close the connection ──


app = FastAPI(
    title="Airport Database API",
    description="Portfolio REST API: airports, flights, passengers, tickets, boarding passes.",
    version="1.0.0",
    lifespan=lifespan,
)

# each include_router adds all endpoints to the app
app.include_router(airport.router)       # /airports/*
app.include_router(flight.router)        # /flights/*
app.include_router(aircraft.router)      # /aircraft/*
app.include_router(passenger.router)     # /passengers/*
app.include_router(ticket.router)        # /tickets/*
app.include_router(boarding_pass.router) # /boarding-passes/*


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Airport Database API is running ✈️"}