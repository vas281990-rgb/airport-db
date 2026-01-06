# ✈️ Airport Database API

## 📌 Project Overview

**Airport Database API** is a backend project that models the core operations of an airport.
The main focus of this project is **database design**, **relationships**, and **backend architecture**.

This project is built as a **portfolio project for a Middle Python Backend Developer** and demonstrates:
- relational database modeling
- complex entity relationships
- clean backend structure
- preparation for real-world API development

---

## 🎯 Goals of the Project

- Design a **realistic airport database schema**
- Demonstrate strong understanding of:
  - one-to-many relationships
  - many-to-many relationships
  - data normalization
- Build a solid foundation for a REST API using FastAPI
- Show professional Git and project structure

---

## 🧠 Domain Model (Core Entities)

### 🏢 Airport
Represents an airport as a physical location.

**Key fields:**
- id
- code (IATA code, e.g. `JFK`, `MAD`)
- name
- city
- country

---

### ✈️ Aircraft
Represents an aircraft model used for flights.

**Key fields:**
- id
- model
- capacity

---

### 🛫 Flight
Represents a specific flight occurring at a certain time.

**Key fields:**
- id
- flight_number
- departure_airport_id
- arrival_airport_id
- departure_time
- arrival_time
- aircraft_id
- status

---

### 🧍 Passenger
Represents a passenger.

**Key fields:**
- id
- first_name
- last_name
- passport_number

---

### 🎟️ Ticket
Represents a ticket purchased by a passenger for a flight.

This table resolves the **many-to-many relationship** between passengers and flights.

**Key fields:**
- id
- passenger_id
- flight_id
- seat_number
- price

---

### 🪪 BoardingPass
Represents a boarding pass issued for a ticket.

**Key fields:**
- id
- ticket_id
- boarding_time
- gate

---

## 🔗 Entity Relationships

- **Airport → Flight**: one-to-many  
- **Aircraft → Flight**: one-to-many  
- **Passenger ↔ Flight**: many-to-many (via Ticket)  
- **Ticket → BoardingPass**: one-to-one  

---

## 🛠️ Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Git & GitHub

---

## 🚧 Project Status

🚀 In progress  
Currently focusing on database design and SQLAlchemy models.
