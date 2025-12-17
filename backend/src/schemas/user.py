from pydantic import BaseModel, EmailStr
from typing import Optional
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
    email: Optional[EmailStr] = None
    senha_atual: Optional[str] = None
    nova_senha: Optional[str] = None
    ui_theme: Optional[str] = None
    intervalo_revisoes: Optional[str] = None

class User(UserBase):
    ID: int
    ui_theme: str
    intervalo_revisoes: str
    data_cadastro: datetime

    class Config:
        from_attributes = True

class UserDelete(BaseModel):
    senha_confirmacao: str
