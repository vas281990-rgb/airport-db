from pydantic import BaseModel


class AirportBase(BaseModel):
    """
    Shared properties for Airport.
    """
    name: str
    code: str
    city: str
    country: str


class AirportCreate(AirportBase):
    """
    Data required to create an airport.
    """
    pass


class AirportRead(AirportBase):
    """
    Data returned from the API.
    """
    id: int

    class Config:
        orm_mode = True
