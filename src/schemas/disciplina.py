from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DisciplinaBase(BaseModel):
    nome: str
    cor: Optional[str] = None
    descricao: Optional[str] = None

class DisciplinaCreate(DisciplinaBase):
    pass

class DisciplinaUpdate(DisciplinaBase):
    pass

class Disciplina(DisciplinaBase):
    ID: int
    usuario_id: int
    data_criacao: datetime

    class Config:
        from_attributes = True
