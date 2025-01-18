from sqlalchemy import Column, Integer, ForeignKey, String, TIMESTAMP, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .settings import Base
import datetime


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    notes = relationship("Note", back_populates="user", cascade="all, delete-orphan")


class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="notes")


class Teste1(Base):
    __tablename__ = "teste1"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    test1 = Column(String(255), nullable=False)
