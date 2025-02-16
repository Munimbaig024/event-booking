import requests
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Booking
from pydantic import BaseModel
from typing import List
from datetime import datetime

router = APIRouter()

USER_SERVICE_URL = "http://user-service:8000"
EVENT_SERVICE_URL = "http://event-service:8001"
NOTIFICATION_SERVICE_URL = "http://notification-service:8003"


# Pydantic schema for request/response
class BookingCreate(BaseModel):
    user_id: int
    event_id: str
    num_tickets: int

class BookingResponse(BaseModel):
    id: int
    user_id: int
    event_id: str
    num_tickets: int
    booking_date: str
    status: str

# Function to check event validity and available tickets
def get_event_details(event_id: str):
    response = requests.get(f"{EVENT_SERVICE_URL}/events/{event_id}")
    if response.status_code != 200:
        return None
    return response.json()

# Function to update event ticket count
def update_event_tickets(event_id: str, available_tickets: int):
    response = requests.put(f"{EVENT_SERVICE_URL}/events/{event_id}/update_tickets",
                            json={"available_tickets": available_tickets})
    return response.status_code == 200


# Function to fetch user email from User Service
def get_user_email(user_id: int):
    response = requests.get(f"{USER_SERVICE_URL}/users/{user_id}")
    
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = response.json()
    return user_data["email"]

def send_notification(email, message):
    requests.post(f"{NOTIFICATION_SERVICE_URL}/notifications", json={"user_email": email, "message": message})

@router.post("/bookings", response_model=BookingResponse)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    event_data = get_event_details(booking.event_id)
    if not event_data:
        raise HTTPException(status_code=404, detail="Event not found")

    available_tickets = event_data["available_tickets"]
    if booking.num_tickets > available_tickets:
        raise HTTPException(status_code=400, detail="Not enough tickets available")
    
    user_email = get_user_email(booking.user_id)

    new_booking = Booking(
        user_id=booking.user_id,
        event_id=booking.event_id,
        num_tickets=booking.num_tickets,
        booking_date=datetime.utcnow(),
        status="CONFIRMED"
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    updated_tickets = available_tickets - booking.num_tickets
    if not update_event_tickets(booking.event_id, updated_tickets):
        raise HTTPException(status_code=500, detail="Failed to update event tickets")


    # Trigger Notification
    send_notification(user_email, f"Your booking for {event_data['title']} is confirmed!")

    return {
        "id": new_booking.id,
        "user_id": new_booking.user_id,
        "event_id": new_booking.event_id,
        "num_tickets": new_booking.num_tickets,
        "booking_date": new_booking.booking_date.isoformat(),
        "status": new_booking.status
    }
