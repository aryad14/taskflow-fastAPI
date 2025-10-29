from fastapi import FastAPI
from core.database import Base, engine
from core.cors import setup_cors
from core.config import settings
from api import router as auth_router
from utils.exceptions import app_exception_handler, AppException, http_exception_handler
from fastapi.exceptions import HTTPException

from models import user, project, task 

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="TaskFlow API for collaborative task management",
    version="1.0.0",
    openapi_url="/api/openapi.json",
)

# Create tables at startup (after models are imported)
@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)

setup_cors(app)
app.include_router(auth_router, prefix="/api")

# Global exception handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

@app.get("/", tags=["Health Check"])
def root():
    """Health check endpoint."""
    return {"message": "TaskFlow API is up and running 🚀"}
