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


security_scheme = HTTPBearer()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_tokens(
    user_data: dict,
    access_token_expires_minutes: Optional[int] = None,
    refresh_token_expires_days: int = 7,
) -> Tuple[str, str, datetime]:
    Retorna: (access_token, refresh_token, expires_at)

    if access_token_expires_minutes is None:
        access_token_expires_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    access_token_expires = timedelta(minutes=access_token_expires_minutes)
    access_token_expires_at = datetime.now(timezone.utc) + access_token_expires

    access_token_data = user_data.copy()
    access_token_data.update(
        {
            "exp": access_token_expires_at,
            "token_type": "access",
            "aud": "authenticated",
            "role": "authenticated",
        }
    )

    if "sub" not in access_token_data:
        access_token_data["sub"] = str(
            user_data.get("ID")
            or user_data.get("supabase_id")
            or user_data.get("email")
        )

    access_token = jwt.encode(
        access_token_data, settings.SUPABASE_JWT_SECRET, algorithm="HS256"
    )

    refresh_token_expires = timedelta(days=refresh_token_expires_days)
    refresh_token_expires_at = datetime.now(timezone.utc) + refresh_token_expires

    refresh_token_data = {
        "sub": access_token_data["sub"],
        "exp": refresh_token_expires_at,
        "token_type": "refresh",
        "jti": str(uuid.uuid4()),
    }

    refresh_token = jwt.encode(
        refresh_token_data, settings.SUPABASE_JWT_SECRET, algorithm="HS256"
    )

    return access_token, refresh_token, access_token_expires_at


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if "aud" not in to_encode:
        to_encode.update({"aud": "authenticated"})

    if "role" not in to_encode:
        to_encode.update({"role": "authenticated"})

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SUPABASE_JWT_SECRET, algorithm="HS256")
    return encoded_jwt


def verify_token(token: str, token_type: str = "access") -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            audience="authenticated",
        )

        if payload.get("token_type") != token_type:
            raise JWTError("Tipo de token inválido")

        return payload

    except JWTError as e:
        raise e


def refresh_access_token(refresh_token: str) -> Tuple[str, datetime]:
    try:

        payload = verify_token(refresh_token, "refresh")

        supabase_id = payload.get("sub")

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token_expires_at = datetime.now(timezone.utc) + access_token_expires

        access_token_data = {
            "sub": supabase_id,
            "token_type": "access",
            "aud": "authenticated",
            "role": "authenticated",
            "exp": access_token_expires_at,
        }

        access_token = jwt.encode(
            access_token_data, settings.SUPABASE_JWT_SECRET, algorithm="HS256"
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

        payload = jwt.decode(
            token,
            settings.SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            audience="authenticated",
        )

        supabase_id_str = payload.get("sub")
        email = payload.get("email")

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
