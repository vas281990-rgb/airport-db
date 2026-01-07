from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.flight import Flight
from app.models.airport import Airport
from app.schemas.flight import FlightCreate, FlightRead


router = APIRouter(prefix="/flights", tags=["Flights"])


@router.post("/", response_model=FlightRead, status_code=status.HTTP_201_CREATED)
def create_flight(
    flight: FlightCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new flight between two airports.
    """

    # Check departure airport exists
    departure_airport = db.query(Airport).filter(
        Airport.id == flight.departure_airport_id
    ).first()
    if not departure_airport:
        raise HTTPException(
            status_code=404,
            detail="Departure airport not found",
        )

    # Check arrival airport exists
    arrival_airport = db.query(Airport).filter(
        Airport.id == flight.arrival_airport_id
    ).first()
    if not arrival_airport:
        raise HTTPException(
            status_code=404,
            detail="Arrival airport not found",
        )

    db_flight = Flight(
        flight_number=flight.flight_number,
        departure_time=flight.departure_time,
        arrival_time=flight.arrival_time,
        departure_airport_id=flight.departure_airport_id,
        arrival_airport_id=flight.arrival_airport_id,
    )

    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)

    return db_flight


@router.get("/", response_model=list[FlightRead])
def get_flights(db: Session = Depends(get_db)):
    """
    Get list of all flights.
    """
    return db.query(Flight).all()
