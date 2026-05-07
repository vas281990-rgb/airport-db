from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.base import Base


class FlightStatus(str, enum.Enum):
    """All possible status."""
    SCHEDULED = "scheduled"   
    BOARDING  = "boarding"   
    DEPARTED  = "departed"   
    ARRIVED   = "arrived"     
    CANCELLED = "cancelled" 
    DELAYED   = "delayed"   


class Flight(Base):
    __tablename__ = "flights"

    id            = Column(Integer, primary_key=True, index=True)
    flight_number = Column(String,  nullable=False, index=True)
    departure_time = Column(DateTime, nullable=False)
    arrival_time   = Column(DateTime, nullable=False)

    departure_airport_id = Column(Integer, ForeignKey("airports.id",  ondelete="CASCADE"), nullable=False)
    arrival_airport_id   = Column(Integer, ForeignKey("airports.id",  ondelete="CASCADE"), nullable=False)
    aircraft_id          = Column(Integer, ForeignKey("aircraft.id",  ondelete="SET NULL"), nullable=True)

    # ondelete="SET NULL" — without a plane, a flight isn't deleted: aircraft_id - NULL
    status = Column(SAEnum(FlightStatus), default=FlightStatus.SCHEDULED, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    departure_airport = relationship("Airport",   foreign_keys=[departure_airport_id], back_populates="departing_flights")
    arrival_airport   = relationship("Airport",   foreign_keys=[arrival_airport_id],   back_populates="arriving_flights")
    aircraft          = relationship("Aircraft",  back_populates="flights")
    tickets           = relationship("Ticket",    back_populates="flight", cascade="all, delete")