from sqlalchemy import Column, Integer, String
from app.db.base import Base


class Airport(Base):
    """
    Airport database model.
    Represents a real-world airport.
    """

    __tablename__ = "airports"

    id = Column(Integer, primary_key=True, index=True)

    # Airport name (e.g. "John F. Kennedy International Airport")
    name = Column(String, nullable=False)

    # IATA code (e.g. "JFK", "LHR")
    code = Column(String(3), unique=True, nullable=False, index=True)

    # City where the airport is located
    city = Column(String, nullable=False)

    # Country of the airport
    country = Column(String, nullable=False)
