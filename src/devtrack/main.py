from fastapi import FastAPI, Request,HTTPException
from fastapi.responses import JSONResponse
from devtrack.api.routes import health,projects,issues,comments,auth
from fastapi.exceptions import RequestValidationError
from devtrack.core.logging_config import setup_logging
import logging
from fastapi.middleware.cors import CORSMiddleware

setup_logging()
logger=logging.getLogger(__name__)

app=FastAPI()
app.include_router(health.router)
app.include_router(projects.router)
app.include_router(issues.router)
app.include_router(comments.router)
app.include_router(auth.router)

@app.exception_handler(HTTPException)   
async def custom_http_exception_handler(request:Request, exc:HTTPException):
    logger.warning(f"HTTPException: {exc.status_code}-{exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={'error':exc.detail}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(req:Request, exc:RequestValidationError):
    logger.warning(f"HTTPException: 422-{exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"error":exc.errors()}
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)