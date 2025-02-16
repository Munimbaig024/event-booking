from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
import models
from database import get_db
from auth import hash_password, verify_password, create_access_token, verify_token
from pydantic import BaseModel
import requests

router = APIRouter()

EVENT_SERVICE_URL = "http://event-service:8001"
BOOKING_SERVICE_URL = "http://booking-service:8002"

# Pydantic schemas
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

class LoginRequest(BaseModel):
    email: str
    password: str

# Register User
@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)
    new_user = models.User(username=user.username, email=user.email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Login User
@router.post("/login")
def login_user(login: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == login.email).first()
    if not user or not verify_password(login.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": user.email, "user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}

# Get User Profile
@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# ✅ Fetch All Users (NEW ENDPOINT)
@router.get("/users", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

# Fetch all events (Only for logged-in users)
@router.get("/events")
def get_events(authorization: str = Header(None)):
    # Verify user is logged in
    user_data = verify_token(authorization)
    if not user_data:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Fetch events from Event Service
    response = requests.get(f"{EVENT_SERVICE_URL}/events")

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch events")

# Create a booking (Only for logged-in users)
@router.post("/bookings")
def create_booking(booking_data: dict, authorization: str = Header(None)):
    # Verify user is logged in
    user_data = verify_token(authorization)
    if not user_data:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Add the user's ID to the booking data
    booking_data["user_id"] = user_data["user_id"]

    # Send request to Booking Service
    response = requests.post(f"{BOOKING_SERVICE_URL}/bookings", json=booking_data)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to create booking")
