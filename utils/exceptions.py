from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from utils.responses import response

class AppException(Exception):
    def __init__(self, message: str, status_code: int = 400, error: str | None = None):
        self.message = message
        self.status_code = status_code
        self.error = error or message

async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content=response(False, exc.message, data=None, error=exc.error),
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=response(False, str(exc.detail), data=None, error=str(exc.detail)),
    )
