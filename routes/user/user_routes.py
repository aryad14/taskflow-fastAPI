from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from schemas.user import UserRead, UserUpdate, UserDelete

from models.user import User

from utils.responses import response
from utils.exceptions import AppException

from core.dependencies import get_db_session, get_current_user

router = APIRouter(prefix="/user", tags=["User Management"])

@router.get("/me", response_model=dict)
def read_current_user(current_user: User = Depends(get_current_user)):
    return response(True, "Current user fetched successfully", data=UserRead.model_validate(current_user).model_dump())

@router.put("/update", response_model=dict)
def update_current_user(
    user_update: UserUpdate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
):
    for field, value in user_update.model_dump(exclude_unset=True).items():
        setattr(current_user, field, value)

    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return response(True, "User updated successfully", data=UserRead.model_validate(current_user).model_dump())

@router.delete("/delete", response_model=dict)
def delete_current_user(
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
):
    db.delete(current_user)
    db.commit()
    return response(True, "User deleted successfully")
