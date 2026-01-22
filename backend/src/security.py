from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple
from .core.config import settings
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from .database import get_db
import uuid
import json


security_scheme = HTTPBearer()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_token(
    user_data: dict,
    access_token_expires_minutes: Optional[int] = None,
    token_headers: Optional[dict] = None,
) -> Tuple[str, datetime]:

    payload = user_data.get('claims', {})

    if access_token_expires_minutes is None:
        access_token_expires_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    access_token_expires = timedelta(minutes=access_token_expires_minutes)
    access_token_expires_at = datetime.now(timezone.utc) + access_token_expires

    payload.update(
        {
            "exp": int(access_token_expires_at.timestamp()),
        }
    )

    user_data['claims'] = payload
    access_token_data = user_data

    secret_key = settings.SUPABASE_SECRET_KEY
    if isinstance(secret_key, str):
        secret_key = secret_key.encode('utf-8')

    access_token = jwt.encode(
        access_token_data,
        secret_key,
        algorithm="HS256",
        headers=token_headers,
    )

    return access_token, access_token_expires_at


def verify_token(token: str, token_type: str = "access") -> dict:
    try:
        public_key = json.loads(settings.SUPABASE_PUBLIC_KEY)

        return jwt.decode(
            token, public_key, algorithms=["ES256"], audience="authenticated"
        )
    except Exception:
        try:
            # 2. Fallback: Tenta validar com o Secret (Para tokens HS256)
            return jwt.decode(
                token,
                settings.SUPABASE_SECRET_KEY,
                algorithms=["HS256"],
                audience="authenticated",
            )
        except JWTError as e:
            raise HTTPException(status_code=401, detail="Token inválido ou expirado")


def refresh_access_token(
    user_data: User, supabase_user: dict, token_headers: Optional[dict] = None
) -> Tuple[str, datetime]:
    try:
        supabase_id = user_data.supabase_id

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token_expires_at = datetime.now(timezone.utc) + access_token_expires

        # claims = {
        #     "iss": f"{settings.SUPABASE_URL}/auth/v1",
        #     "session_id": str(uuid.uuid4()),
        #     "sub": str(supabase_id),
        #     "email": user_data.email,
        #     "phone": supabase_user.phone or "",
        #     "app_metadata": {"provider": "email", "providers": ["email"]},
        #     "user_metadata": {"nome": user_data.nome, "email_verified": True},
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
        #     "exp": int(access_token_expires_at.timestamp()),
        #     "is_anonymous": supabase_user.is_anonymous or False,
        # }

        token_data = {
            "user_id": str(supabase_id),
            "claims": claims,
            "authentication_method": "password",
        }

        access_token = jwt.encode(
            token_data,
            settings.SUPABASE_SECRET_KEY,
            algorithm="HS256",
            headers=token_headers,
        )

        return access_token, access_token_expires_at

    except JWTError as e:
        raise e


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: AsyncSession = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token = credentials.credentials

        payload = verify_token(token)
        payload = payload.get("claims", {})

        supabase_id_str = payload.get("sub")
        email = payload.get("email") or payload.get("user_metadata", {}).get("email")

        if not supabase_id_str or supabase_id_str == "None":
            raise credentials_exception

        try:
            supabase_uuid = uuid.UUID(supabase_id_str)
        except ValueError:

            supabase_uuid = None

        user = None

        if supabase_uuid:
            result = await db.execute(
                select(User).where(User.supabase_id == supabase_uuid)
            )
            user = result.scalars().first()

        if not user and email:
            result = await db.execute(select(User).where(User.email == email))
            user = result.scalars().first()

            if user and supabase_uuid and not user.supabase_id:
                user.supabase_id = supabase_uuid
                await db.commit()

        if not user:
            raise credentials_exception

        return user

    except JWTError as e:

        raise credentials_exception
    except Exception as e:

        raise credentials_exception
