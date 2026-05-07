from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base


class Aircraft(Base):
    """
    Aircraft database model.
    Represents an aircraft used for flights.
    """
    __tablename__ = "aircraft"

    id = Column(Integer, primary_key=True, index=True)
    model = Column(String, nullable=False)           # "Boeing 737-800"
    capacity = Column(Integer, nullable=False)        # 189
    icao_code = Column(String(10), nullable=True)     # "B738" — опционально

    # один самолёт → много рейсов
    flights = relationship(
        "Flight",
        back_populates="aircraft",
        cascade="all, delete",
    )

    def __repr__(self) -> str:
        return f"<Aircraft id={self.id} model={self.model!r} capacity={self.capacity}>"