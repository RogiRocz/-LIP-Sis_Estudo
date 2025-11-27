from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TemaBase(BaseModel):
    nome: str
    descricao: Optional[str] = None

class TemaCreate(TemaBase):
    pass

class TemaUpdate(TemaBase):
    pass

class Tema(TemaBase):
    ID: int
    disciplina_id: int
    data_criacao: datetime

    class Config:
        from_attributes = True
