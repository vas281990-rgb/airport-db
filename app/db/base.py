from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# for create_all() to create tables, and Alembic see migrations
# Import all models here so SQLAlchemy can see them
from app.models.airport      import Airport       # noqa
from app.models.aircraft     import Aircraft      # noqa
from app.models.flight       import Flight        # noqa
from app.models.passenger    import Passenger     # noqa
from app.models.ticket       import Ticket        # noqa
from app.models.boarding_pass import BoardingPass # noqa