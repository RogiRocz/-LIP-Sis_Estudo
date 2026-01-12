from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
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

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if "aud" not in to_encode:
        to_encode.update({"aud": "authenticated"})

    if "role" not in to_encode:
        to_encode.update({"role": "authenticated"})

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SUPABASE_JWT_SECRET, algorithm="HS256")  # Use o mesmo secret do Supabase
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        
        # Decodifica o token usando o secret do Supabase
        payload = jwt.decode(
            token, 
            settings.SUPABASE_JWT_SECRET, 
            algorithms=["HS256"], 
            audience="authenticated"
        )
        
        supabase_id_str = payload.get("sub")
        email = payload.get("email")
        
        print(f"DEBUG: supabase_id do token: {supabase_id_str}")
        print(f"DEBUG: email do token: {email}")
        
        if not supabase_id_str or supabase_id_str == "None":
            raise credentials_exception
            
        # Tenta converter para UUID
        try:
            supabase_uuid = uuid.UUID(supabase_id_str)
        except ValueError:
            # Se não for um UUID válido, pode ser um ID local (ex: "local-123")
            print(f"DEBUG: supabase_id não é UUID válido: {supabase_id_str}")
            supabase_uuid = None
        
        user = None
        
        # Busca por supabase_id (se for UUID)
        if supabase_uuid:
            result = await db.execute(select(User).where(User.supabase_id == supabase_uuid))
            user = result.scalars().first()
        
        # Fallback: busca por email
        if not user and email:
            result = await db.execute(select(User).where(User.email == email))
            user = result.scalars().first()
            
            # Se encontrou por email e tem um supabase_id do token, atualiza
            if user and supabase_uuid and not user.supabase_id:
                user.supabase_id = supabase_uuid
                await db.commit()
                print(f"DEBUG: Atualizado supabase_id para usuário {email}")
        
        if not user:
            print(f"DEBUG: Usuário não encontrado (supabase_id: {supabase_id_str}, email: {email})")
            raise credentials_exception
            
        return user
        
    except JWTError as e:
        print(f"DEBUG: Erro JWT: {e}")
        raise credentials_exception
    except Exception as e:
        print(f"DEBUG: Erro inesperado: {e}")
        raise credentials_exception