from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.middleware.cors import CORSMiddleware
import models

# This matches the database we will set up in Docker later
# Use this exact line to match the YML credentials
DATABASE_URL = "postgresql://myuser:mypassword@db:5432/phonebook_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This creates the table automatically so you don't have to [cite: 22]
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allows your Frontend to talk to this Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/contacts") # Retrieve all [cite: 17]
def read_contacts(db: Session = Depends(get_db)):
    return db.query(models.Contact).all()

@app.post("/contacts") # Add new [cite: 18]
def create_contact(contact: dict, db: Session = Depends(get_db)):
    db_contact = models.Contact(**contact)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@app.delete("/contacts/{id}") # Delete [cite: 21]
def delete_contact(id: int, db: Session = Depends(get_db)):
    db.query(models.Contact).filter(models.Contact.id == id).delete()
    db.commit()
    return {"message": "Deleted"}