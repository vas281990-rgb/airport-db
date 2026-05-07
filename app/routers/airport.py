from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.airport import Airport
from app.schemas.airport import AirportCreate, AirportRead, AirportUpdate

router = APIRouter(prefix="/airports", tags=["Airports"])


@router.post("/", response_model=AirportRead, status_code=201)
def create_airport(airport: AirportCreate, db: Session = Depends(get_db)):
    existing = db.query(Airport).filter(Airport.code == airport.code).first()
    if existing:
        raise HTTPException(status_code=409, detail=f"Airport with code '{airport.code}' already exists")
    db_airport = Airport(**airport.model_dump())
    db.add(db_airport); db.commit(); db.refresh(db_airport)
    return db_airport


@router.get("/", response_model=list[AirportRead])
def list_airports(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    country: str | None = Query(None),   
    db: Session = Depends(get_db),
):
    query = db.query(Airport)
    if country:
        query = query.filter(Airport.country.ilike(f"%{country}%"))
       
    return query.offset(skip).limit(limit).all()


@router.get("/{airport_id}", response_model=AirportRead)
def get_airport(airport_id: int, db: Session = Depends(get_db)):
    airport = db.query(Airport).filter(Airport.id == airport_id).first()
    if not airport:
        raise HTTPException(status_code=404, detail="Airport not found")
    return airport


@router.patch("/{airport_id}", response_model=AirportRead)
def update_airport(airport_id: int, data: AirportUpdate, db: Session = Depends(get_db)):
    airport = db.query(Airport).filter(Airport.id == airport_id).first()
    if not airport:
        raise HTTPException(status_code=404, detail="Airport not found")
    for field, value in data.model_dump(exclude_none=True).items():
       
        setattr(airport, field, value)
    db.commit(); db.refresh(airport)
    return airport


@router.delete("/{airport_id}", status_code=204)
def delete_airport(airport_id: int, db: Session = Depends(get_db)):
    airport = db.query(Airport).filter(Airport.id == airport_id).first()
    if not airport:
        raise HTTPException(status_code=404, detail="Airport not found")
    db.delete(airport); db.commit()