from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=True)
    address = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)