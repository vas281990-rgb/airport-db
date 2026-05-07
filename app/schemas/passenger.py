from pydantic import BaseModel, Field, EmailStr


class PassengerBase(BaseModel):
    first_name: str      = Field(..., examples=["Ana"])
    last_name: str       = Field(..., examples=["García"])
    passport_number: str = Field(..., examples=["AB123456"])
    email: EmailStr | None = Field(None, examples=["ana@email.com"])
    # EmailStr automatically believes that its a true email
    phone: str | None = Field(None, examples=["+598 99 123 456"])


class PassengerCreate(PassengerBase): pass

class PassengerUpdate(BaseModel):
    email: EmailStr | None = None  # only contacts can be updated
    phone: str | None = None

class PassengerRead(PassengerBase):
    id: int
    model_config = {"from_attributes": True}