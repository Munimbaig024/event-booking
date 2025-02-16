import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://booking_user:booking_password@localhost:5434/booking_db")

config = Config()
