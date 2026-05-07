from datetime import datetime, timedelta
from app.db.session import SessionLocal
from app.db.base import Base
from app.db.session import engine
from app.models.airport import Airport
from app.models.aircraft import Aircraft
from app.models.flight import Flight, FlightStatus
from app.models.passenger import Passenger
from app.models.ticket import Ticket


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    now = datetime.now()

    try:
        # Airports
        airports_data = [
            {"name": "Carrasco International Airport", "code": "MVD", "city": "Montevideo", "country": "Uruguay"},
            {"name": "Ministro Pistarini International Airport", "code": "EZE", "city": "Buenos Aires", "country": "Argentina"},
            {"name": "Guarulhos International Airport", "code": "GRU", "city": "São Paulo", "country": "Brazil"},
            # ... and 5 more airports
        ]
        airports = {}
        for data in airports_data:
            existing = db.query(Airport).filter(Airport.code == data["code"]).first()
            if not existing:
                a = Airport(**data)
                db.add(a); db.flush()   # flush → get a.id
                airports[data["code"]] = a
                print(f"  ✅ Airport: {data['code']} — {data['city']}")

        # Aircrafts 
        aircraft_list = []
        for data in [{"model": "Boeing 737-800", "capacity": 189, "icao_code": "B738"},
                     {"model": "Airbus A320neo", "capacity": 165, "icao_code": "A20N"}]:
            ac = Aircraft(**data); db.add(ac); db.flush()
            aircraft_list.append(ac)

        # Flights with real numbers 
        db.add(Flight(
            flight_number="PU101",
            departure_airport_id=airports["MVD"].id,
            arrival_airport_id=airports["EZE"].id,
            departure_time=now + timedelta(hours=2),
            arrival_time=now + timedelta(hours=3, minutes=30),
            aircraft_id=aircraft_list[0].id,
            status=FlightStatus.SCHEDULED,
        ))
        # ... and 5 more flights

        db.commit()
        print("\n🎉 Seed complete!")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("🌱 Seeding database...\n")
    seed()