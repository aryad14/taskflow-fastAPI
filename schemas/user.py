from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

    @field_validator("password")
    @classmethod
    def ensure_bcrypt_limit(cls, v: str) -> str:
        if len(v.encode("utf-8")) > 72:
            raise ValueError("Password must be at most 72 bytes for bcrypt")
        return v

class UserRead(UserBase):
    id: int
    created_at: datetime

    # Pydantic v2: enable ORM attribute parsing
    model_config = ConfigDict(from_attributes=True)
