from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional
import re
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://phonebook_user:phonebook_pass@db:5432/phonebook_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ── Model ──────────────────────────────────────────────────────────────────────

class Contact(Base):
    __tablename__ = "contacts"

    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String(255), nullable=False)
    phone_number = Column(String(50), unique=True, nullable=False)
    email      = Column(String(255), unique=True, nullable=True)
    address    = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# ── Schemas ────────────────────────────────────────────────────────────────────

class ContactCreate(BaseModel):
    name: str
    phone_number: str
    email: Optional[str] = None
    address: Optional[str] = None

    @validator("name")
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()

    @validator("phone_number")
    def phone_valid(cls, v):
        cleaned = re.sub(r"[\s\-\(\)]", "", v)
        if not re.match(r"^\+?\d{7,15}$", cleaned):
            raise ValueError("Invalid phone number format (e.g. +1234567890)")
        return cleaned

    @validator("email")
    def email_valid(cls, v):
        if v and not re.match(r"^[^@]+@[^@]+\.[^@]+$", v):
            raise ValueError("Invalid email format")
        return v

class ContactUpdate(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None

    @validator("phone_number", pre=True)
    def phone_valid(cls, v):
        if v is None:
            return v
        cleaned = re.sub(r"[\s\-\(\)]", "", v)
        if not re.match(r"^\+?\d{7,15}$", cleaned):
            raise ValueError("Invalid phone number format")
        return cleaned

class ContactOut(BaseModel):
    id: int
    name: str
    phone_number: str
    email: Optional[str]
    address: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True

# ── App ────────────────────────────────────────────────────────────────────────

app = FastAPI(title="Phonebook API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ── Routes ─────────────────────────────────────────────────────────────────────

@app.get("/contacts", response_model=list[ContactOut])
def get_contacts(search: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Contact)
    if search:
        query = query.filter(
            Contact.name.ilike(f"%{search}%") |
            Contact.phone_number.ilike(f"%{search}%")
        )
    return query.order_by(Contact.created_at.desc()).all()

@app.post("/contacts", response_model=ContactOut, status_code=201)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    existing_phone = db.query(Contact).filter(Contact.phone_number == contact.phone_number).first()
    if existing_phone:
        raise HTTPException(status_code=409, detail="Phone number already exists")
    if contact.email:
        existing_email = db.query(Contact).filter(Contact.email == contact.email).first()
        if existing_email:
            raise HTTPException(status_code=409, detail="Email already exists")
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@app.get("/contacts/{id}", response_model=ContactOut)
def get_contact(id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@app.put("/contacts/{id}", response_model=ContactOut)
def update_contact(id: int, update: ContactUpdate, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    for field, value in update.dict(exclude_unset=True).items():
        setattr(contact, field, value)
    db.commit()
    db.refresh(contact)
    return contact

@app.delete("/contacts/{id}", status_code=204)
def delete_contact(id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()

@app.get("/health")
def health():
    return {"status": "ok"}