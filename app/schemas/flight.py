from pydantic import BaseModel


class FlightBase(BaseModel):
    flight_number: str
    destination: str


class FlightCreate(FlightBase):
    airport_id: int


class FlightRead(FlightBase):
    id: int
    airport_id: int

    class Config:
        orm_mode = True
