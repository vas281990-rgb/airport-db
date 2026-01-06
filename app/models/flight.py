from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base


class Flight(Base):
    """
    Flight database model.
    Represents a flight between two airports.
    """

    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)

    # Flight number (e.g. "BA2490")
    flight_number = Column(String, nullable=False, index=True)

    # Departure time
    departure_time = Column(DateTime, nullable=False)

    # Arrival time
    arrival_time = Column(DateTime, nullable=False)

    # Airport IDs
    departure_airport_id = Column(
        Integer,
        ForeignKey("airports.id", ondelete="CASCADE"),
        nullable=False,
    )

    arrival_airport_id = Column(
        Integer,
        ForeignKey("airports.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Relationships
    departure_airport = relationship(
        "Airport",
        foreign_keys=[departure_airport_id],
        back_populates="departing_flights",
    )

    arrival_airport = relationship(
        "Airport",
        foreign_keys=[arrival_airport_id],
        back_populates="arriving_flights",
    )

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
