from fastapi import FastAPI
from devtrack.api.routes import health
app=FastAPI()
app.include_router(health.router)