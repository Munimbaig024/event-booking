from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Pydantic schema for Event API requests
class Event(BaseModel):
    title: str
    description: Optional[str] = None
    date: datetime
    location: str
    available_tickets: int
