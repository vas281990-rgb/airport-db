from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

# Import all models here so SQLAlchemy can see them
from app.models.airport import Airport  # noqa: F401
from app.models.flight import Flight  # noqa: F401
