import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ensure DATABASE_URL is set
DATABASE_URL = os.getenv("DATABASE_URL")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")  # Ensure this is defined


if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in environment variables!")
