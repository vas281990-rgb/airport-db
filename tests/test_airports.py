class TestCreateAirport:
    def test_create_airport_success(self, client, airport_payload):
        r = client.post("/airports/", json=airport_payload)
        assert r.status_code == 201
        assert r.json()["code"] == "MVD"
        assert "id" in r.json()

    def test_create_airport_duplicate_code(self, client, airport_payload):
        client.post("/airports/", json=airport_payload)  # first — ok
        r = client.post("/airports/", json=airport_payload)  # second — 409
        assert r.status_code == 409
        assert "already exists" in r.json()["detail"]

    def test_create_airport_missing_field(self, client):
        r = client.post("/airports/", json={"name": "Test", "code": "TST"})
        assert r.status_code == 422  # not a city and a country → Pydantic error


class TestListAirports:
    def test_list_airports_pagination(self, client, airport_payload):
        for code, city in [("AAA", "City A"), ("BBB", "City B"), ("CCC", "City C")]:
            client.post("/airports/", json={**airport_payload, "code": code, "city": city})
        r = client.get("/airports/?limit=2&skip=0")
        assert len(r.json()) == 2   # first 2
        r = client.get("/airports/?limit=2&skip=2")
        assert len(r.json()) == 1   # third

    def test_filter_by_country(self, client, created_airport, created_second_airport):
        r = client.get("/airports/?country=Uruguay")
        assert len(r.json()) == 1
        assert r.json()[0]["code"] == "MVD"