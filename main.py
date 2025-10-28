from fastapi import FastAPI
from core.database import Base, engine
from core.cors import setup_cors
from core.config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

setup_cors(app)

@app.get("/", tags=["Health Check"])
def root():
    """
    Health check endpoint to verify the API is running.
    """
    return {"message": "TaskFlow API is up and running"}
