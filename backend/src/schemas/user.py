from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    nome: Optional[str] = None

class UserCreate(UserBase):
    senha: str
    confirmar_senha: str

class UserLogin(BaseModel):
    email: EmailStr
    senha: str

class UserUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha_atual: Optional[str] = None
    nova_senha: Optional[str] = None
    ui_theme: Optional[str] = None
    intervalo_revisoes: Optional[List[int]] = None

class User(UserBase):
    ui_theme: str
    intervalo_revisoes: List[int]
    supabase_id: Optional[str] = None

    class Config:
        from_attributes = True

class UserDelete(BaseModel):
    senha_confirmacao: str
