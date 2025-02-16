from fastapi import FastAPI
from database import engine, Base
import routes

# Create database tables before running the server
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include booking routes
app.include_router(routes.router)
