from datetime import datetime
from pydantic import BaseModel

from app.schemas.airport import AirportRead


class FlightBase(BaseModel):
    flight_number: str
    departure_time: datetime
    arrival_time: datetime
    departure_airport_id: int
    arrival_airport_id: int


class FlightCreate(FlightBase):
    """
    Schema for creating a flight.
    """
    pass


class FlightRead(BaseModel):
    """
    Schema for reading flight data.
    Includes nested airport information.
    """

    id: int
    flight_number: str
    departure_time: datetime
    arrival_time: datetime

    departure_airport: AirportRead
    arrival_airport: AirportRead

    class Config:
        from_attributes = True
