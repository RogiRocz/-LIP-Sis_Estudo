from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from repositories.user import UserRepository
from schemas.user import UserCreate, UserLogin, User
from schemas.auth import Token
from security import verify_password, create_access_token, get_password_hash
from core.config import settings

class AuthService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.user_repo = UserRepository(db)

    async def register(self, user_data: UserCreate) -> Token:
        if user_data.senha != user_data.confirmar_senha:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Passwords do not match"
            )

        existing_user = await self.user_repo.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        hashed_password = get_password_hash(user_data.senha)

        db_user = await self.user_repo.create_user(user_data, hashed_password)
        db_user.tema = settings.DEFAULT_THETHEME
        db_user.intervalo_revisoes = settings.DEFAULT_REVISION_INTERVAL
        await self.user_repo.update_user(db_user)

        access_token = create_access_token(data={"sub": db_user.email})
        user_schema = User.from_orm(db_user)
        return Token(access_token=access_token, token_type="bearer", user=user_schema)

    async def login(self, user_data: UserLogin) -> Token:
        db_user = await self.user_repo.get_user_by_email(user_data.email)
        if not db_user or not verify_password(user_data.senha, db_user.senha):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token(data={"sub": db_user.email})
        user_schema = User.from_orm(db_user)
        return Token(access_token=access_token, token_type="bearer", user=user_schema)
