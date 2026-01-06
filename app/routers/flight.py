from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.flight import Flight
from app.models.airport import Airport
from app.schemas.flight import FlightCreate, FlightRead

router = APIRouter(prefix="/flights", tags=["Flights"])


@router.post("/", response_model=FlightRead)
def create_flight(flight: FlightCreate, db: Session = Depends(get_db)):
    """
    Create a new flight.
    """

    airport = db.query(Airport).filter(Airport.id == flight.airport_id).first()
    if not airport:
        raise HTTPException(status_code=404, detail="Airport not found")

    db_flight = Flight(**flight.model_dump())
    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)
    return db_flight
