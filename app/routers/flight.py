from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from datetime import datetime
from app.db.session import get_db
from app.models.flight import Flight, FlightStatus
from app.models.airport import Airport
from app.schemas.flight import FlightCreate, FlightRead, FlightListItem, FlightUpdate


router = APIRouter(prefix="/flights", tags=["Flights"])

def _get_flight_or_404(flight_id: int, db: Session) -> Flight:
    
    flight = (
        db.query(Flight)
        .options(
            joinedload(Flight.departure_airport),  # JOIN airports AS dep
            joinedload(Flight.arrival_airport),    # JOIN airports AS arr
            joinedload(Flight.aircraft),           # JOIN aircraft
        )
        .filter(Flight.id == flight_id)
        .first()
    )
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    return flight


@router.post("/", response_model=FlightRead, status_code=201)
def create_flight(flight: FlightCreate, db: Session = Depends(get_db)):
    for airport_id in [flight.departure_airport_id, flight.arrival_airport_id]:
        if not db.query(Airport).filter(Airport.id == airport_id).first():
            raise HTTPException(status_code=404, detail=f"Airport id={airport_id} not found")
    if flight.departure_airport_id == flight.arrival_airport_id:
        raise HTTPException(status_code=400, detail="Departure and arrival airports must be different")
    db_flight = Flight(**flight.model_dump())
    db.add(db_flight); db.commit(); db.refresh(db_flight)
    return _get_flight_or_404(db_flight.id, db)


@router.get("/", response_model=list[FlightListItem])
def list_flights(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: FlightStatus | None = Query(None),               # ?status=boarding
    departure_airport_id: int | None = Query(None),          # ?departure_airport_id=1
    arrival_airport_id: int | None = Query(None),
    date_from: datetime | None = Query(None),                # ?date_from=2025-06-01
    date_to: datetime | None = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Flight)
    if status:               query = query.filter(Flight.status == status)
    if departure_airport_id: query = query.filter(Flight.departure_airport_id == departure_airport_id)
    if arrival_airport_id:   query = query.filter(Flight.arrival_airport_id == arrival_airport_id)
    if date_from:            query = query.filter(Flight.departure_time >= date_from)
    if date_to:              query = query.filter(Flight.departure_time <= date_to)
    return query.order_by(Flight.departure_time).offset(skip).limit(limit).all()


@router.patch("/{flight_id}", response_model=FlightRead)
def update_flight(flight_id: int, data: FlightUpdate, db: Session = Depends(get_db)):
    flight = db.query(Flight).filter(Flight.id == flight_id).first()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(flight, field, value)
    db.commit()
    return _get_flight_or_404(flight_id, db)