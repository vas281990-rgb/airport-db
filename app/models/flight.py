from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)

    flight_number = Column(String, nullable=False, index=True)

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
