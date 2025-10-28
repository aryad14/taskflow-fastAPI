from typing import Any, Optional

def response(success: bool, message: str, data: Optional[Any] = None, error: Optional[Any] = None):
    return {
        "success": success,
        "message": message,
        "data": data,
        "error": error,
    }
