from fastapi import FastAPI
from devtrack.api.routes import health,projects,issues
app=FastAPI()
app.include_router(health.router)
app.include_router(projects.router)
app.include_router(issues.router)