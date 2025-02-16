# from fastapi import FastAPI
# from database import engine, Base
# import routes

# # Create database tables
# Base.metadata.create_all(bind=engine)

# app = FastAPI()

# # Include routes
# app.include_router(routes.router)
from fastapi import FastAPI
from database import init_db
import routes

app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_db()  # Ensure tables are created before queries

app.include_router(routes.router)
