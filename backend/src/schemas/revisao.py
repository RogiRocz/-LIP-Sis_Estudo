from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class RevisaoBase(BaseModel):
    data_prevista: Optional[date] = None
    data_realizada: Optional[datetime] = None
    tempo_dedicado: Optional[int] = None
    status: str = 'PENDENTE'
    descricao: Optional[str] = None

class RevisaoUpdate(RevisaoBase):
    pass

class Revisao(RevisaoBase):
    ID: int
    tema_id: int
    criado_em: datetime
    atualizado_em: datetime

    class Config:
        from_attributes = True
