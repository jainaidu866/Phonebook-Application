from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True) # Primary Key [cite: 10]
    name = Column(String(255), nullable=False) # Name [cite: 11]
    phone_number = Column(String, unique=True, nullable=False) # Unique Phone [cite: 12]
    email = Column(String, unique=True, nullable=True) # Optional Email [cite: 13]
    address = Column(String, nullable=True) # Optional Address [cite: 14]
    created_at = Column(DateTime, default=datetime.datetime.utcnow) # Timestamp [cite: 15]