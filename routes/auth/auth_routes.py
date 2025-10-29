from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserRead
from models.user import User
from utils.responses import response
from utils.exceptions import AppException
from core.dependencies import get_db_session, get_current_user
from core.security import hash_password, verify_password, create_access_token
from schemas.token import Token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=dict)
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

    return response(True, "User created successfully", data=UserRead.model_validate(new_user).model_dump())

@router.post("/login", response_model=Token)
async def login_user(request: Request, db: Session = Depends(get_db_session)):
    # Support both JSON and form (OAuth2Password flow) in a single route
    content_type = request.headers.get("content-type", "")
    email = None
    password = None

    if "application/json" in content_type:
        try:
            data = await request.json()
        except Exception:
            data = {}
        email = (data or {}).get("email")
        password = (data or {}).get("password")
    else:
        form = await request.form()
        # OAuth2 uses "username"; accept "email" as well
        email = form.get("username") or form.get("email")
        password = form.get("password")

    if not email or not password:
        raise AppException("Email and password are required", 400)

    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise AppException("Invalid email or password", 400)

    access_token = create_access_token({"sub": str(user.id)})
    return Token(access_token=access_token, token_type="bearer")

@router.post('/logout')
def logout_user(current_user: User = Depends(get_current_user)):
    return response(True, "User logged out successfully")