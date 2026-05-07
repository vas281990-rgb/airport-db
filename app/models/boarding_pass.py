from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class BoardingPass(Base):
    __tablename__ = "boarding_passes"

    id = Column(Integer, primary_key=True, index=True)

    # unique=True makes one-to-one in db
    ticket_id = Column(Integer, ForeignKey("tickets.id", ondelete="CASCADE"),
                       unique=True, nullable=False)

    gate         = Column(String(10),  nullable=False)   # "B12"
    boarding_time = Column(DateTime,   nullable=False)
    issued_at    = Column(DateTime,    default=datetime.utcnow)

    ticket = relationship("Ticket", back_populates="boarding_pass")