from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.airport import Airport
from app.schemas.airport import AirportCreate, AirportRead

router = APIRouter(prefix="/airports", tags=["Airports"])


@router.post("/", response_model=AirportRead)
def create_airport(airport: AirportCreate, db: Session = Depends(get_db)):
    """
    Create a new airport.
    """
    db_airport = Airport(**airport.model_dump())
    db.add(db_airport)
    db.commit()
    db.refresh(db_airport)
    return db_airport
