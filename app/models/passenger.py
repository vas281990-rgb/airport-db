from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base


class Passenger(Base):
    __tablename__ = "passengers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name  = Column(String, nullable=False)

    # уникальный — нельзя зарегистрировать одного пассажира дважды
    passport_number = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)

    tickets = relationship("Ticket", back_populates="passenger", cascade="all, delete")

    @property
    def full_name(self) -> str:
        # не колонка в БД — просто удобный атрибут
        return f"{self.first_name} {self.last_name}"