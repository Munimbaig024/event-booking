from fastapi import APIRouter, HTTPException
from database import notification_collection
from email_service import send_email
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class NotificationCreate(BaseModel):
    user_email: str
    message: str

# Send a notification (Email + Store in DB)
@router.post("/notifications")
def send_notification(notification: NotificationCreate):
    # Send Email
    email_sent = send_email(
        recipient_email=notification.user_email,
        subject="Booking Confirmation",
        body=notification.message
    )

    # Store Notification in MongoDB
    notification_entry = {
        "user_email": notification.user_email,
        "message": notification.message,
        "timestamp": datetime.utcnow()
    }
    notification_collection.insert_one(notification_entry)

    if not email_sent:
        raise HTTPException(status_code=500, detail="Email sending failed, but notification stored in DB")

    return {"message": "Notification sent and stored"}

# Get all notifications for a user
@router.get("/notifications/{user_email}")
def get_notifications(user_email: str):
    notifications = list(notification_collection.find({"user_email": user_email}, {"_id": 0}))
    return notifications
