from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.repositories.user import UserRepository
from src.schemas.user import UserCreate, UserLogin, User
from src.schemas.auth import Token
from src.security import verify_password, create_access_token, get_password_hash
from src.core.config import settings

class AuthService:
    def __init__(self, db: Session = Depends(get_db)):
        self.user_repo = UserRepository(db)

    def register(self, user_data: UserCreate) -> Token:
        if user_data.senha != user_data.confirmar_senha:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Passwords do not match"
            )

        existing_user = self.user_repo.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        hashed_password = get_password_hash(user_data.senha)

        # We handle user creation directly here because it's tied to auth flow
        # and has specific default settings.
        db_user = self.user_repo.create_user(user_data, hashed_password)
        db_user.tema = settings.DEFAULT_THEME
        db_user.intervalo_revisoes = settings.DEFAULT_REVISION_INTERVAL
        self.user_repo.update_user(db_user) # Commit the new settings

        access_token = create_access_token(data={"sub": db_user.email})
        user_schema = User.model_validate(db_user)
        return Token(access_token=access_token, token_type="bearer", user=user_schema)

    def login(self, user_data: UserLogin) -> Token:
        db_user = self.user_repo.get_user_by_email(user_data.email)
        if not db_user or not verify_password(user_data.senha, db_user.senha):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token(data={"sub": db_user.email})
        user_schema = User.model_validate(db_user)
        return Token(access_token=access_token, token_type="bearer", user=user_schema)
