from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from datetime import datetime
from app.db.session import get_db
from app.models.ticket import Ticket
from app.models.flight import Flight, FlightStatus
from app.models.passenger import Passenger
from app.schemas.ticket import TicketCreate, TicketRead, TicketListItem

router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.post("/", response_model=TicketRead, status_code=201)
def book_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    # 1. A passenger should exist 
    passenger = db.query(Passenger).filter(Passenger.id == ticket.passenger_id).first()
    if not passenger:
        raise HTTPException(status_code=404, detail="Passenger not found")

    # 2. A flight should exist
    flight = db.query(Flight).filter(Flight.id == ticket.flight_id).first()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    # 3. Not allowed on a cancelled flight
    if flight.status == FlightStatus.CANCELLED:
        raise HTTPException(status_code=400, detail="Cannot book a ticket for a cancelled flight")

    # 4. Not allowed on a departed flight
    if flight.status in (FlightStatus.DEPARTED, FlightStatus.ARRIVED):
        raise HTTPException(status_code=400, detail="Cannot book a ticket for a flight that has already departed")

    # 5. Not allowed on a past flight
    if flight.departure_time < datetime.now():
        raise HTTPException(status_code=400, detail="Cannot book a ticket for a flight in the past")

    # 6. A seat should be free
    seat_taken = db.query(Ticket).filter(
        Ticket.flight_id == ticket.flight_id,
        Ticket.seat_number == ticket.seat_number,
    ).first()
    if seat_taken:
        raise HTTPException(status_code=409,
                            detail=f"Seat '{ticket.seat_number}' is already taken on this flight")

    db_ticket = Ticket(**ticket.model_dump())
    db.add(db_ticket); db.commit(); db.refresh(db_ticket)
    return _get_ticket_or_404(db_ticket.id, db)


@router.delete("/{ticket_id}", status_code=204)
def cancel_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    # not allowed to cancell a departed flight
    flight = db.query(Flight).filter(Flight.id == ticket.flight_id).first()
    if flight and flight.status in (FlightStatus.DEPARTED, FlightStatus.ARRIVED):
        raise HTTPException(status_code=400,
                            detail="Cannot cancel a ticket for a flight that has already departed")
    db.delete(ticket); db.commit()