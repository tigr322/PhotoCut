from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.user import User


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register(self, email: str, password: str) -> User:
        existing_user = self.db.scalar(select(User).where(User.email == email.lower()))
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

        user = User(email=email.lower(), password_hash=hash_password(password), is_active=True)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def authenticate(self, email: str, password: str) -> User:
        user = self.db.scalar(select(User).where(User.email == email.lower()))
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is inactive")
        return user
