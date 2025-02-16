from fastapi import FastAPI
import routes

app = FastAPI()

# Include notification routes
app.include_router(routes.router)
