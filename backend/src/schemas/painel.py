from pydantic import BaseModel
from datetime import date, timedelta


class EstatisticasGerais(BaseModel):
    total_disciplinas: int
    total_temas: int
    total_revisoes: int
    revisoes_hoje: int


class EvolucaoSemanal(BaseModel):
    data: date
    revisoes_realizadas: int


class RevisaoDoDia(BaseModel):
    id_revisao: int
    titulo_tema: str
    nome_disciplina: str


class PainelData(BaseModel):
    estatisticas: EstatisticasGerais
    evolucao_semanal: list[EvolucaoSemanal]
    revisoes_do_dia: list[RevisaoDoDia]

class RelatorioEstudos(BaseModel):
    subject: str
    studyMinutes: int
    revisionsDone: int
    revisionsPending: int

class RelatorioGeral(BaseModel):
    totalHours: float
    data: list[RelatorioEstudos]