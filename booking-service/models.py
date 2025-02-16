from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  # Assuming users are stored in another service
    event_id = Column(String, nullable=False)  # Event IDs will be UUIDs
    booking_date = Column(DateTime, default=datetime.utcnow)
    num_tickets = Column(Integer, nullable=False)
    status = Column(String, default="PENDING")  # PENDING, CONFIRMED, CANCELED
