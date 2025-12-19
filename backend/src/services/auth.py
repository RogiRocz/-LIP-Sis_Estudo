from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..repositories.user import UserRepository
from ..schemas.user import UserCreate, UserLogin, User
from ..schemas.auth import Token
from ..security import verify_password, create_access_token, get_password_hash
from ..core.config import settings

class AuthService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.user_repo = UserRepository(db)

    async def register(self, user_data: UserCreate) -> Token:
        if user_data.senha != user_data.confirmar_senha:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="As senhas não conferem"
            )

        existing_user = await self.user_repo.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já registrado"
            )

        hashed_password = get_password_hash(user_data.senha)

        db_user = await self.user_repo.create_user(user_data, hashed_password)
        db_user.ui_theme = settings.DEFAULT_THEME
        db_user.intervalo_revisoes = settings.DEFAULT_REVISION_INTERVAL
        await self.user_repo.update_user(db_user)

        token = create_access_token(data={"sub": db_user.email})
        user_schema = User.model_validate(db_user)
        return Token(token=token, token_type="bearer", user=user_schema)

    async def login(self, user_data: UserLogin) -> Token:
        db_user = await self.user_repo.get_user_by_email(user_data.email)
        if not db_user or not verify_password(user_data.senha, db_user.senha):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = create_access_token(data={"sub": db_user.email})
        user_schema = User.model_validate(db_user)
        return Token(token=token, token_type="bearer", user=user_schema)
