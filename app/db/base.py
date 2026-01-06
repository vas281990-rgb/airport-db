from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import all models here so SQLAlchemy can see them
from app.models.airport import Airport  # noqa
