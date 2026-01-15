from pydantic import BaseModel
from .user import User
from typing import Optional
from datetime import datetime

class Token(BaseModel):
    token: str
    refresh_token: Optional[str] = None
    expires_at: Optional[datetime] = None
    token_type: str
    user: User

class TokenLogout(Token):
    token: str
    refresh_token: Optional[str] = None
    expires_at: Optional[datetime] = None
    token_type: Optional[str] = None
    user: Optional[User] = None

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class RefreshTokenResponse(BaseModel):
    token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_at: datetime
