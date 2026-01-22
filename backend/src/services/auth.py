from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..repositories.user import UserRepository
from ..schemas.user import UserCreate, UserLogin, User
from ..schemas.auth import Token, RefreshTokenResponse
from ..security import (
    create_token,
    refresh_access_token,
    verify_token,
    get_password_hash,
    verify_password,
)
from ..core.config import settings
from ..core.supabase_client import supabase
from datetime import datetime, timezone
import uuid
from jose import jwt

CURRENT_KID = None


def get_kid_from_supabase_token(token: str):
    unverified_header = jwt.get_unverified_header(token)
    return unverified_header.get("kid")


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

        global CURRENT_KID

        try:
            auth_response = supabase.auth.sign_in_with_password(
                {"email": user_data.email, "password": user_data.senha}
            )

            refresh_token_supabase = auth_response.session.refresh_token
            access_token_supabase = auth_response.session.access_token
            official_claims = supabase.auth.get_claims(access_token_supabase)
            CURRENT_KID = get_kid_from_supabase_token(access_token_supabase)

        except Exception as e:
            print(f"Erro ao fazer login no Supabase: {e}")
            raise e

        # claims = {
        #     "iss": f"{settings.SUPABASE_URL}/auth/v1",
        #     "session_id": str(uuid.uuid4()),
        #     "sub": str(supabase_id),
        #     "email": db_user.email,
        #     "phone": supabase_user.phone or "",
        #     "app_metadata": {"provider": "email", "providers": ["email"]},
        #     "user_metadata": {"nome": db_user.nome, "email_verified": True},
        #     "aal": "aal1",
        #     "amr": [
        #         {
        #             "method": "password",
        #             "timestamp": int(datetime.now(timezone.utc).timestamp()),
        #         }
        #     ],
        #     "iat": int(datetime.now(timezone.utc).timestamp()),
        #     "role": "authenticated",
        #     "aud": "authenticated",
        #     "is_anonymous": supabase_user.is_anonymous or False,
        # }

        token = {
            "user_id": str(supabase_id),
            "claims": official_claims.get('claims', {}),
            "authentication_method": "password",
        }

        headers = {
            "kid": "89ed0414-93b3-4382-ac29-65619f17ffd6",
            "typ": "JWT",
            "alg": "HS256",
        }

        access_token, expires_at = create_token(user_data=token, token_headers=headers)

        user_schema = User.model_validate(db_user)
        return Token(
            token=access_token,
            refresh_token=refresh_token_supabase,
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
            refresh_token_supabase = auth_response.session.refresh_token
            access_token_supabase = auth_response.session.access_token
            official_claims = supabase.auth.get_claims(access_token_supabase)

            global CURRENT_KID
            CURRENT_KID = get_kid_from_supabase_token(access_token_supabase)

        except Exception as e:
            print(f"Erro no login do Supabase: {e}")

        db_user = await self.user_repo.get_user_by_email(user_data.email)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not verify_password(user_data.senha, db_user.senha):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Senha incorreta",
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
                print(
                    f"Erro ao atualizar o ID Supabase no banco de dados: {supabase_error}"
                )
                raise supabase_error
        else:
            supabase_id = str(db_user.supabase_id)

        if not db_user:
            raise HTTPException(
                status_code=404,
                detail="Usuário não encontrado na base local. Entre em contato com o suporte.",
            )

        # custom_claims = {
        #     "iss": f"{settings.SUPABASE_URL}/auth/v1",
        #     "session_id": str(uuid.uuid4()),
        #     "sub": str(supabase_id),
        #     "email": db_user.email,
        #     "phone": supabase_user.phone or "",
        #     "app_metadata": {"provider": "email", "providers": ["email"]},
        #     "user_metadata": {"nome": db_user.nome, "email_verified": True},
        #     "amr": [
        #         {
        #             "method": "password",
        #             "timestamp": int(datetime.now(timezone.utc).timestamp()),
        #         }
        #     ],
        #     "aal": "aal1",
        #     "iat": int(datetime.now(timezone.utc).timestamp()),
        #     "role": "authenticated",
        #     "aud": "authenticated",
        #     "is_anonymous": supabase_user.is_anonymous or False,
        # }

        token = {
            "user_id": str(supabase_id),
            "claims": official_claims.get('claims', {}),
            "authentication_method": "password",
        }

        headers = {
            "kid": "89ed0414-93b3-4382-ac29-65619f17ffd6",
            "typ": "JWT",
            "alg": "HS256",
        }

        access_token, expires_at = create_token(user_data=token, token_headers=headers)

        user_schema = User.model_validate(db_user)

        return Token(
            token=access_token,
            refresh_token=refresh_token_supabase,
            expires_at=expires_at,
            token_type="bearer",
            user=user_schema,
        )

    async def refresh(self, refresh_token: str) -> RefreshTokenResponse:
        try:
            res = supabase.auth.refresh_session(refresh_token)
        
            if not res.session:
                raise HTTPException(status_code=401, detail="Sessão expirada")

            official_claims = supabase.auth.get_claims(res.session.access_token)
            access_token_exp = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            official_claims.update('exp', access_token_exp.timestamp())
            
            return RefreshTokenResponse(
                token=res.session.access_token,
                refresh_token=res.session.refresh_token,
                expires_at=datetime.fromtimestamp(official_claims['exp'], tz=timezone.utc)
            )
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Falha ao atualizar token. {str(e)}")

    async def logout(self, token: str):
        # Aplicar verificação se o token é do usuário que fez a requisição
        try:
            supabase.auth.sign_out(token)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=f"Token inválido para deslogar: {str(e)}",
            )
