from fastapi import FastAPI
from devtrack.api.routes import health,projects,issues,comments,auth
app=FastAPI()
app.include_router(health.router)
app.include_router(projects.router)
app.include_router(issues.router)
app.include_router(comments.router)
app.include_router(auth.router)