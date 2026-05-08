class TestBookTicket:
    def test_book_ticket_success(self, client, created_passenger, created_flight):
        r = client.post("/tickets/", json={
            "passenger_id": created_passenger["id"],
            "flight_id": created_flight["id"],
            "seat_number": "14A",
            "price": "199.99",
        })
        assert r.status_code == 201
        assert "passenger" in r.json()   
        assert "flight" in r.json()

    def test_book_ticket_seat_already_taken(self, client, created_ticket):
        # creating the second passenger and try the same
        r2 = client.post("/passengers/", json={
            "first_name": "Bob", "last_name": "Smith", "passport_number": "XX999999"
        })
        r = client.post("/tickets/", json={
            "passenger_id": r2.json()["id"],
            "flight_id": created_ticket["flight"]["id"],
            "seat_number": created_ticket["seat_number"],  # то же место!
            "price": "150.00",
        })
        assert r.status_code == 409
        assert "already taken" in r.json()["detail"]

    def test_book_ticket_cancelled_flight(self, client, created_passenger, created_flight):
        # first cancel the flight
        client.patch(f"/flights/{created_flight['id']}", json={"status": "cancelled"})
        r = client.post("/tickets/", json={
            "passenger_id": created_passenger["id"],
            "flight_id": created_flight["id"],
            "seat_number": "7B", "price": "120.00",
        })
        assert r.status_code == 400
        assert "cancelled" in r.json()["detail"]

    def test_cancel_ticket_on_departed_flight(self, client, created_ticket):
        # if a flight departed → it's not allowed to cancel
        flight_id = created_ticket["flight"]["id"]
        client.patch(f"/flights/{flight_id}", json={"status": "departed"})
        r = client.delete(f"/tickets/{created_ticket['id']}")
        assert r.status_code == 400
        assert "departed" in r.json()["detail"]

    def test_issue_boarding_pass_duplicate(self, client, created_ticket):
        payload = {"ticket_id": created_ticket["id"], "gate": "B12", "boarding_time": "2099-06-01T09:30:00"}
        client.post("/boarding-passes/", json=payload)   # firts — ok
        r = client.post("/boarding-passes/", json=payload)  # second — 409
        assert r.status_code == 409
        assert "already issued" in r.json()["detail"]