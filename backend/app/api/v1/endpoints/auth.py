from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.db.session import get_db
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.user import UserOut
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=UserOut)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> UserOut:
    user = AuthService(db).register(email=payload.email, password=payload.password)
    return UserOut.model_validate(user)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = AuthService(db).authenticate(email=payload.email, password=payload.password)
    token = create_access_token(subject=user.id)
    return TokenResponse(access_token=token, user=UserOut.model_validate(user))
