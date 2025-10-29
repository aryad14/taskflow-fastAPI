from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    id: int | None = None

class LoginSchema(BaseModel):
    email: str
    password: str
