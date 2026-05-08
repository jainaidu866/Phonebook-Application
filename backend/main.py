from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.middleware.cors import CORSMiddleware
import models, re

DATABASE_URL = "postgresql://myuser:mypassword@db:5432/phonebook_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

def validate_phone(phone: str):
    if not re.match(r'^\+?[1-9]\d{6,14}$', phone):
        raise HTTPException(status_code=400, detail="Invalid format. Use +1234567890")

@app.get("/contacts")
def read_contacts(db: Session = Depends(get_db)):
    return db.query(models.Contact).all()

@app.post("/contacts")
def create_contact(contact: dict, db: Session = Depends(get_db)):
    validate_phone(contact.get("phone", ""))
    db_contact = models.Contact(
        name=contact.get("name"),
        phone=contact.get("phone"),
        email=contact.get("email"),
        address=contact.get("address")
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact