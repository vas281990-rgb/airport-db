import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.db.session import get_db
from app.main import app

TEST_DATABASE_URL = "sqlite:///./test_airport.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Before each test — create tables, after — delete."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)   # full isolation


@pytest.fixture(scope="function")
def db():
    session = TestingSessionLocal()
    try: yield session
    finally: session.close()


@pytest.fixture(scope="function")
def client(db):
    """TestClient with a fake DB."""
    def override_get_db():
        yield db   # a test session instead of production

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# Ready data — used in tests as arguments

@pytest.fixture
def created_airport(client, airport_payload):
    r = client.post("/airports/", json=airport_payload)
    assert r.status_code == 201
    return r.json()


@pytest.fixture
def created_flight(client, flight_payload):
    # flight_payload already has id of created airports
    r = client.post("/flights/", json=flight_payload)
    assert r.status_code == 201
    return r.json()


@pytest.fixture
def created_ticket(client, created_passenger, created_flight):
    r = client.post("/tickets/", json={
        "passenger_id": created_passenger["id"],
        "flight_id": created_flight["id"],
        "seat_number": "14A",
        "price": "199.99",
    })
    assert r.status_code == 201
    return r.json()