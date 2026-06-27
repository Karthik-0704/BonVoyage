from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .database import engine, Base, get_db
from pydantic import BaseModel
from app.agents.llm import call_llm
from app.agents.orchestrator import plan_trip
from sqlalchemy.orm import Session
from .models import TripRequest, TripPlan, User
import traceback
import hashlib
import secrets
import os

app = FastAPI()

FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------- Auth helpers ------------------

def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 260000).hex()
    return f"{salt}:{hashed}"

def verify_password(password: str, stored: str) -> bool:
    salt, hashed = stored.split(":", 1)
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 260000).hex() == hashed


# -------------- Request models ------------------

class SignupRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class PlanTripRequest(BaseModel):
    prompt: str

class PromptRequest(BaseModel):
    prompt: str


# -------------- Startup ------------------

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


# -------------- Health ------------------

@app.get("/health")
def health():
    return {"status": "ok"}


# -------------- Auth ------------------

@app.post("/signup")
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == request.email).first():
        return JSONResponse(status_code=400, content={"error": "Email already registered"})
    user = User(
        name=request.name,
        email=request.email,
        password_hash=hash_password(request.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"user_id": user.id, "name": user.name, "email": user.email}

@app.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not verify_password(request.password, user.password_hash):
        return JSONResponse(status_code=401, content={"error": "Invalid credentials"})
    return {"user_id": user.id, "name": user.name, "email": user.email}


# -------------- Trip planning ------------------

@app.post("/plan_trip")
async def plan_trip_endpoint(user_id: int, request: PlanTripRequest, db: Session = Depends(get_db)):
    try:
        intent = await call_llm(request.prompt)
        result = await plan_trip(request.prompt, intent)
    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}

    trip_request = TripRequest(
        user_id=user_id,
        raw_prompt=request.prompt,
        origin=intent.get("origin"),
        destination=intent.get("destination"),
        days=intent.get("days"),
        people=intent.get("people"),
        budget=intent.get("budget"),
    )
    db.add(trip_request)
    db.commit()
    db.refresh(trip_request)

    plan = result.get("plan")
    flights = []
    hotels = []

    if plan:
        trip_plan = TripPlan(
            trip_request_id=trip_request.id,
            origin=request.source,
            destination=request.destination,
            airline=plan["flight"]["airline"],
            flight_price=plan["flight"]["total_price"],
            hotel_name=plan["hotel"]["name"],
            hotel_price=plan["hotel"]["total_price"],
            total_cost=plan["total_cost"],
        )
        db.add(trip_plan)
        db.commit()

        flights = [{
            "airline": plan["flight"]["airline"],
            "provider": "RapidAPI",
            "price": plan["flight"]["total_price"],
            "duration_hours": plan["flight"].get("duration_hours"),
        }]
        hotels = [{
            "name": plan["hotel"]["name"],
            "provider": "RapidAPI",
            "price_per_day": plan["hotel"].get("price_per_night"),
            "rating": None,
        }]

    return {
        "source": intent.get("origin"),
        "destination": intent.get("destination"),
        "days": intent.get("days"),
        "people_count": intent.get("people"),
        "budget": intent.get("budget"),
        "flights": flights,
        "hotels": hotels,
        "itinerary": [],
        "summary": result.get("summary", ""),
    }


@app.get("/get_trips_of_one_user")
def get_trips_of_one_user(user_id: int, db: Session = Depends(get_db)):
    trip_requests = (
        db.query(TripRequest)
        .filter(TripRequest.user_id == user_id)
        .order_by(TripRequest.created_at.desc())
        .all()
    )
    trips = []
    for tr in trip_requests:
        plan = db.query(TripPlan).filter(TripPlan.trip_request_id == tr.id).first()
        flights = []
        hotels = []
        if plan:
            flights = [{
                "airline": plan.airline,
                "provider": "RapidAPI",
                "price": plan.flight_price,
                "duration_hours": None,
            }]
            hotels = [{
                "name": plan.hotel_name,
                "provider": "RapidAPI",
                "price_per_day": round(plan.hotel_price / tr.days, 2) if tr.days else None,
                "rating": None,
            }]
        trips.append({
            "source": tr.origin,
            "destination": tr.destination,
            "days": tr.days,
            "people_count": tr.people,
            "budget": tr.budget,
            "flights": flights,
            "hotels": hotels,
            "itinerary": [],
        })
    return trips


# -------------- Testing ------------------

@app.post("/test-llm-raw")
async def test_llm_raw(request: PromptRequest):
    try:
        return await call_llm(request.prompt)
    except RuntimeError as e:
        return {"error": str(e)}