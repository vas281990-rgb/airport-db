from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.boarding_pass import BoardingPass
from app.models.ticket import Ticket
from app.models.flight import Flight, FlightStatus
from app.schemas.boarding_pass import BoardingPassCreate, BoardingPassRead

router = APIRouter(prefix="/boarding-passes", tags=["Boarding Passes"])


@router.post("/", response_model=BoardingPassRead, status_code=201)
def issue_boarding_pass(data: BoardingPassCreate, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == data.ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Is a bording_pass diven?
    existing = db.query(BoardingPass).filter(BoardingPass.ticket_id == data.ticket_id).first()
    if existing:
        raise HTTPException(status_code=409, detail="Boarding pass already issued for this ticket")

    flight = db.query(Flight).filter(Flight.id == ticket.flight_id).first()
    if flight and flight.status == FlightStatus.CANCELLED:
        raise HTTPException(status_code=400, detail="Cannot issue boarding pass for a cancelled flight")
    if flight and flight.status in (FlightStatus.DEPARTED, FlightStatus.ARRIVED):
        raise HTTPException(status_code=400, detail="Flight has already departed")

    db_bp = BoardingPass(**data.model_dump())
    db.add(db_bp); db.commit(); db.refresh(db_bp)
    return db_bp


@router.get("/by-ticket/{ticket_id}", response_model=BoardingPassRead)
def get_boarding_pass_by_ticket(ticket_id: int, db: Session = Depends(get_db)):
    bp = db.query(BoardingPass).filter(BoardingPass.ticket_id == ticket_id).first()
    if not bp:
        raise HTTPException(status_code=404, detail="No boarding pass found for this ticket")
    return bp