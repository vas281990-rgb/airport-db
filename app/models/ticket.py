from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base import Base


class Ticket(Base):
    __tablename__ = "tickets"

    # protection in db: one seat on the plane - one time
    __table_args__ = (
        UniqueConstraint("flight_id", "seat_number", name="uq_flight_seat"),
    )

    id = Column(Integer, primary_key=True, index=True)

    passenger_id = Column(Integer, ForeignKey("passengers.id", ondelete="CASCADE"),
                          nullable=False, index=True)
    flight_id    = Column(Integer, ForeignKey("flights.id",    ondelete="CASCADE"),
                          nullable=False, index=True)

    seat_number = Column(String(5),        nullable=False)   # "14A"
    price       = Column(Numeric(10, 2),   nullable=False)   # 199.99

    passenger    = relationship("Passenger",    back_populates="tickets")
    flight       = relationship("Flight",       back_populates="tickets")

    # one-to-one → one ticket = one boarding pass
    boarding_pass = relationship("BoardingPass", back_populates="ticket",
                                 uselist=False, cascade="all, delete")