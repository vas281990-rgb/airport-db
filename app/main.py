from fastapi import FastAPI
from app.database import Base, engine

app = FastAPI(title="Airport Database API")

# Create tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"status": "Airport API is running"}
