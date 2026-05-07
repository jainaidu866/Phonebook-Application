from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.middleware.cors import CORSMiddleware
import models
import re

DATABASE_URL = "postgresql://myuser:mypassword@db:5432/phonebook_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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

# Requirement: Validate input data (phone number format) [cite: 23]
def validate_phone(phone: str):
    pattern = r'^\+?[1-9]\d{6,14}$'
    if not re.match(pattern, phone):
        raise HTTPException(
            status_code=400, 
            detail="Invalid format. Use international format like +1234567890"
        )

@app.get("/contacts") # Retrieve all [cite: 17]
def read_contacts(db: Session = Depends(get_db)):
    return db.query(models.Contact).all()

@app.post("/contacts") # Add new [cite: 18, 23]
def create_contact(contact: dict, db: Session = Depends(get_db)):
    validate_phone(contact.get("phone_number", ""))
    db_contact = models.Contact(**contact)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@app.get("/contacts/{id}") # Requirement: Retrieve specific contact [cite: 19]
def read_contact(id: int, db: Session = Depends(get_db)):
    contact = db.query(models.Contact).filter(models.Contact.id == id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@app.put("/contacts/{id}") # Requirement: Update specific contact [cite: 20]
def update_contact(id: int, updated: dict, db: Session = Depends(get_db)):
    contact = db.query(models.Contact).filter(models.Contact.id == id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    if "phone_number" in updated:
        validate_phone(updated["phone_number"])
        
    for key, value in updated.items():
        setattr(contact, key, value)
    
    db.commit()
    db.refresh(contact)
    return contact

@app.delete("/contacts/{id}") # Delete specific contact [cite: 21]
def delete_contact(id: int, db: Session = Depends(get_db)):
    db.query(models.Contact).filter(models.Contact.id == id).delete()
    db.commit()
    return {"message": "Deleted"}