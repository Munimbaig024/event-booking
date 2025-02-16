from fastapi import FastAPI
import routes

app = FastAPI()

# Include event routes
app.include_router(routes.router)
