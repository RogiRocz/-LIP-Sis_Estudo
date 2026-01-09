from pydantic import BaseModel
from typing import List, Dict, Any
from .revisao import Revisao

class Estatisticas(BaseModel):
    tempo_total: str
    sessoes_completas: int
    dias_seguidos: int

class EvolucaoSemanal(BaseModel):
    labels: List[str]
    datasets: List[Dict[str, Any]]

class RevisoesDoDia(BaseModel):
    atrasadas: List[Revisao]
    hoje: List[Revisao]

    class Config:
        orm_mode = True
