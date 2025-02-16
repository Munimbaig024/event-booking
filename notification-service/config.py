import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI")
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = int(os.getenv("SMTP_PORT"))
    EMAIL_SENDER = os.getenv("EMAIL_SENDER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

config = Config()
