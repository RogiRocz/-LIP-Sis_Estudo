from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..repositories.user import UserRepository
from ..schemas.user import UserCreate, UserLogin, User
from ..schemas.auth import Token, RefreshTokenResponse
from ..security import (
    create_tokens,
    refresh_access_token,
    verify_token,
    get_password_hash,
    verify_password,
)
from ..core.config import settings
from ..core.supabase_client import supabase
import uuid

class AuthService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.user_repo = UserRepository(db)
        self.db = db

    async def register(self, user_data: UserCreate) -> Token:
        if user_data.senha != user_data.confirmar_senha:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="As senhas não conferem"
            )

        existing_user = await self.user_repo.get_user_by_email(user_data.email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email já registrado"
            )

        try:

            auth_response = supabase.auth.admin.create_user(
                {
                    "email": user_data.email,
                    "password": user_data.senha,
                    "email_confirm": True,
                    "user_metadata": {"nome": user_data.nome},
                }
            )

            supabase_user = auth_response.user
            supabase_id = str(supabase_user.id)

        except Exception as e:

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao criar usuário no sistema de autenticação: {str(e)}",
            )

        hashed_password = get_password_hash(user_data.senha)

        db_user = await self.user_repo.create_user(user_data, hashed_password)
        db_user.ui_theme = settings.DEFAULT_THEME
        db_user.intervalo_revisoes = settings.DEFAULT_REVISION_INTERVAL
        db_user.supabase_id = uuid.UUID(supabase_id)

        await self.user_repo.update_user(db_user)

        token_data = {
            "sub": supabase_id,
            "email": db_user.email,
            "nome": db_user.nome,
            "role": "authenticated",
            "aud": "authenticated",
        }

        access_token, refresh_token, expires_at = create_tokens(
            token_data,
        )

        user_schema = User.model_validate(db_user)
        return Token(
            token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at,
            token_type="bearer",
            user=user_schema,
        )

    async def login(self, user_data: UserLogin) -> Token:

        try:

            auth_response = supabase.auth.sign_in_with_password(
                {"email": user_data.email, "password": user_data.senha}
            )

            supabase_user = auth_response.user
            supabase_id = str(supabase_user.id)

        except Exception as e:
            print(f"Erro no login do Supabase: {e}")

        db_user = await self.user_repo.get_user_by_email(user_data.email)
        if not db_user or not verify_password(user_data.senha, db_user.senha):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not db_user.supabase_id:
            try:
                auth_users = supabase.auth.admin.list_users()
                for auth_user in auth_users:
                    if auth_user.email == user_data.email:
                        db_user.supabase_id = uuid.UUID(str(auth_user.id))
                        await self.user_repo.update_user(db_user)
                        supabase_id = str(auth_user.id)
                        break
            except Exception as supabase_error:
                print(f"Erro ao atualizar o ID Supabase no banco de dados: {supabase_error}")
                raise supabase_error
        else:
            supabase_id = str(db_user.supabase_id)

        if not db_user:
            raise HTTPException(
                status_code=404,
                detail="Usuário não encontrado na base local. Entre em contato com o suporte.",
            )

        token_data = {
            "sub": supabase_id,
            "email": db_user.email,
            "nome": db_user.nome,
            "role": "authenticated",
            "aud": "authenticated",
        }

        access_token, refresh_token, expires_at = create_tokens(
            token_data,
        )

        user_schema = User.model_validate(db_user)
        return Token(
            token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at,
            token_type="bearer",
            user=user_schema,
        )


async def refresh(self, refresh_token: str) -> RefreshTokenResponse:
    try:
        payload = verify_token(refresh_token, "refresh")
        supabase_id = payload.get("sub")

        existing_user = await self.user_repo.get_user_by_supabase_id(supabase_id)

        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Refresh token inválido",
            )

        new_access_token, expires_at = refresh_access_token(refresh_token)

        new_refresh_token = None
        if settings.REFRESH_TOKEN_ROTATION:
            _, new_refresh_token, _ = create_tokens({"sub": supabase_id})

        return RefreshTokenResponse(
            token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            expires_at=expires_at,
        )

    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido ou expirado",
        )

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao renovar token: {str(e)}",
        )
