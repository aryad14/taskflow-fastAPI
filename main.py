from fastapi import FastAPI
from core.database import Base, engine
from core.cors import setup_cors
from core.config import settings
# Add these imports
from models import user, project, task

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="""
    TaskFlow is a collaborative task management API built with FastAPI and SQLAlchemy. It provides endpoints for user authentication, project creation, and task tracking.
    """,
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",   # base OpenAPI path
    docs_url="/docs",                     # Swagger UI
    redoc_url="/redoc",                   # ReDoc
    root_path="/api/v1"                   # base API path
)

setup_cors(app)

@app.get("/", tags=["Health Check"])
def root():
    """Health check endpoint to verify API is running."""
    return {"message": "TaskFlow API is up and running"}
