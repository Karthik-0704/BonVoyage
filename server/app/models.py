from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TripRequest(Base):
    __tablename__ = "trip_requests"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    raw_prompt = Column(String, nullable=False)
    origin = Column(String, nullable=True)
    destination = Column(String, nullable=True)
    days = Column(Integer, nullable=True)
    people = Column(Integer, nullable=True)
    budget = Column(Float, nullable=True)
    total_cost = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TripPlan(Base):
    __tablename__ = "trip_plans"
    id = Column(Integer, primary_key=True, index=True)
    trip_request_id = Column(Integer, ForeignKey("trip_requests.id"))
    origin = Column(String)
    destination = Column(String)
    airline = Column(String)
    flight_price = Column(Float)
    hotel_name = Column(String)
    hotel_price = Column(Float)
    total_cost = Column(Float)
    summary = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())