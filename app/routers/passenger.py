from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.passenger import Passenger
from app.schemas.passenger import PassengerCreate, PassengerRead, PassengerUpdate

router = APIRouter(prefix="/passengers", tags=["Passengers"])


@router.post("/", response_model=PassengerRead, status_code=201)
def create_passenger(passenger: PassengerCreate, db: Session = Depends(get_db)):
    existing = db.query(Passenger).filter(
        Passenger.passport_number == passenger.passport_number
    ).first()
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"Passenger with passport '{passenger.passport_number}' already exists",
        )
    db_passenger = Passenger(**passenger.model_dump())
    db.add(db_passenger); db.commit(); db.refresh(db_passenger)
    return db_passenger


@router.get("/", response_model=list[PassengerRead])
def list_passengers(skip: int = Query(0, ge=0), limit: int = Query(20, le=100),
                    db: Session = Depends(get_db)):
    return db.query(Passenger).offset(skip).limit(limit).all()


@router.get("/{passenger_id}", response_model=PassengerRead)
def get_passenger(passenger_id: int, db: Session = Depends(get_db)):
    p = db.query(Passenger).filter(Passenger.id == passenger_id).first()
    if not p: raise HTTPException(status_code=404, detail="Passenger not found")
    return p


@router.patch("/{passenger_id}", response_model=PassengerRead)
def update_passenger(passenger_id: int, data: PassengerUpdate, db: Session = Depends(get_db)):
    p = db.query(Passenger).filter(Passenger.id == passenger_id).first()
    if not p: raise HTTPException(status_code=404, detail="Passenger not found")
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(p, field, value)
    db.commit(); db.refresh(p); return p


@router.delete("/{passenger_id}", status_code=204)
def delete_passenger(passenger_id: int, db: Session = Depends(get_db)):
    p = db.query(Passenger).filter(Passenger.id == passenger_id).first()
    if not p: raise HTTPException(status_code=404, detail="Passenger not found")
    db.delete(p); db.commit()