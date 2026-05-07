from pydantic import BaseModel, Field


class AircraftBase(BaseModel):
    model: str    = Field(..., examples=["Boeing 737-800"])
    capacity: int = Field(..., gt=0, examples=[189])  # gt=0 → more then 0
    icao_code: str | None = Field(None, examples=["B738"])

class AircraftCreate(AircraftBase): pass

class AircraftUpdate(BaseModel):
    model: str | None = None
    capacity: int | None = Field(None, gt=0)
    icao_code: str | None = None

class AircraftRead(AircraftBase):
    id: int
    model_config = {"from_attributes": True}