from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TemaBase(BaseModel):
    nome: str
    descricao: Optional[str] = None

class TemaCreate(TemaBase):
    pass
    intervalos: Optional[list[int]] = None

class TemaUpdate(TemaBase):
    pass
    intervalos: Optional[list[int]] = None

class Tema(TemaBase):
    ID: int
    disciplina_id: int
    criado_em: datetime
    atualizado_em: datetime

    class Config:
        from_attributes = True
