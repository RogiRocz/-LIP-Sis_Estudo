from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class RevisaoBase(BaseModel):
    data_prevista: Optional[date] = None
    data_realizada: Optional[datetime] = None
    tempo_minutos: Optional[int] = None
    status: str = 'PENDENTE'
    tipo_revisao: Optional[str] = None
    descricao: Optional[str] = None

class RevisaoUpdate(BaseModel):
    data_prevista: Optional[date] = None
    data_realizada: Optional[datetime] = None
    tempo_minutos: Optional[int] = None
    status: Optional[str] = None
    descricao: Optional[str] = None

class Revisao(RevisaoBase):
    ID: int
    tema_id: int

    class Config:
        from_attributes = True
