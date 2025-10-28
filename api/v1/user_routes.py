from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserRead
from models.user import User
from utils.responses import response
from utils.exceptions import AppException
from core.dependencies import get_db_session
from core.security import hash_password

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=dict)
def create_user(user: UserCreate, db: Session = Depends(get_db_session)):
    existing = db.query(User).filter((User.name == user.name) | (User.email == user.email)).first()
    if existing:
        raise AppException("Email already exists", 400)

    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Pydantic v2
    return response(True, "User created successfully", data=UserRead.model_validate(new_user).model_dump())

@router.get("/", response_model=dict)
def get_all_users(db: Session = Depends(get_db_session)):
    users = db.query(User).all()
    data = [UserRead.from_orm(u).dict() for u in users]
    return response(True, "Fetched all users", data=data)
