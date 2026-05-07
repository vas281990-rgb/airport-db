from datetime import datetime
from pydantic import BaseModel, Field, model_validator
from app.models.flight import FlightStatus
from app.schemas.airport import AirportRead
from app.schemas.aircraft import AircraftRead


class FlightBase(BaseModel):
    flight_number: str = Field(..., examples=["IB2490"])
    departure_time: datetime
    arrival_time: datetime
    departure_airport_id: int
    arrival_airport_id: int
    aircraft_id: int | None = None
    status: FlightStatus = FlightStatus.SCHEDULED

    @model_validator(mode="after")
    def arrival_after_departure(self) -> "FlightBase":
        # automatic validation — the arrival is to be after the departure
        if self.arrival_time <= self.departure_time:
            raise ValueError("arrival_time must be after departure_time")
        return self


class FlightCreate(FlightBase):
    pass   


class FlightUpdate(BaseModel):
    # for PATCH — all fields are optional
    status: FlightStatus | None = None
    aircraft_id: int | None = None
    departure_time: datetime | None = None
    arrival_time: datetime | None = None


class FlightRead(BaseModel):
    # full response
    id: int
    flight_number: str
    departure_time: datetime
    arrival_time: datetime
    status: FlightStatus
    departure_airport: AirportRead    
    arrival_airport: AirportRead      
    aircraft: AircraftRead | None = None

    model_config = {"from_attributes": True}  # Pydantic v2 = orm_mode


class FlightListItem(BaseModel):
    # short response
    id: int
    flight_number: str
    departure_time: datetime
    arrival_time: datetime
    status: FlightStatus
    departure_airport_id: int
    arrival_airport_id: int

    model_config = {"from_attributes": True}