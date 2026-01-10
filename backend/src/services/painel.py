from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from datetime import date, timedelta
from ..models.disciplina import Disciplina
from ..models.tema import Tema
from ..models.revisao import Revisao
from ..schemas import painel as painel_schema
from fastapi import Depends
from ..database import get_db


class PainelService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_estatisticas_gerais(self, usuario_id: int) -> painel_schema.EstatisticasGerais:
        total_disciplinas_query = select(func.count(Disciplina.ID)).filter(Disciplina.usuario_id == usuario_id)
        total_disciplinas = await self.db.scalar(total_disciplinas_query) or 0

        total_temas_query = select(func.count(Tema.ID)).join(Disciplina, Tema.disciplina_id == Disciplina.ID).filter(Disciplina.usuario_id == usuario_id)
        total_temas = await self.db.scalar(total_temas_query) or 0

        total_revisoes_query = select(func.count(Revisao.ID)).join(Tema, Revisao.tema_id == Tema.ID).join(Disciplina, Tema.disciplina_id == Disciplina.ID).filter(Disciplina.usuario_id == usuario_id)
        total_revisoes = await self.db.scalar(total_revisoes_query) or 0

        revisoes_hoje_query = select(func.count(Revisao.ID)).join(Tema, Revisao.tema_id == Tema.ID).join(Disciplina, Tema.disciplina_id == Disciplina.ID).filter(
            Disciplina.usuario_id == usuario_id,
            Revisao.data_prevista == date.today()
        )
        revisoes_hoje = await self.db.scalar(revisoes_hoje_query) or 0

        return painel_schema.EstatisticasGerais(
            total_disciplinas=total_disciplinas,
            total_temas=total_temas,
            total_revisoes=total_revisoes,
            revisoes_hoje=revisoes_hoje
        )

    async def get_evolucao_semanal(self, usuario_id: int) -> list[painel_schema.EvolucaoSemanal]:
        today = date.today()
        seven_days_ago = today - timedelta(days=6)

        revisoes_query = (
            select(Revisao.data_prevista, func.count(Revisao.ID))
            .select_from(Revisao)
            .join(Tema, Revisao.tema_id == Tema.ID)
            .join(Disciplina, Tema.disciplina_id == Disciplina.ID)
            .filter(
                Disciplina.usuario_id == usuario_id,
                Revisao.data_prevista >= seven_days_ago,
                Revisao.data_prevista <= today
            )
            .group_by(Revisao.data_prevista)
        )
        revisoes_result = await self.db.execute(revisoes_query)
        revisoes = revisoes_result.all()

        revisoes_dict = {data: count for data, count in revisoes}

        evolucao = []
        for i in range(7):
            current_date = seven_days_ago + timedelta(days=i)
            evolucao.append(
                painel_schema.EvolucaoSemanal(
                    data=current_date,
                    revisoes_realizadas=revisoes_dict.get(current_date, 0),
                )
            )

        return evolucao

    async def get_revisoes_do_dia(self, usuario_id: int) -> list[painel_schema.RevisaoDoDia]:
        revisoes_query = (
            select(Revisao.ID, Tema.nome, Disciplina.nome)
            .select_from(Revisao)
            .join(Tema, Revisao.tema_id == Tema.ID)
            .join(Disciplina, Tema.disciplina_id == Disciplina.ID)
            .filter(
                Disciplina.usuario_id == usuario_id,
                Revisao.data_prevista == date.today(),
            )
        )
        revisoes_result = await self.db.execute(revisoes_query)
        revisoes = revisoes_result.all()

        return [
            painel_schema.RevisaoDoDia(
                id_revisao=id_revisao,
                titulo_tema=titulo_tema,
                nome_disciplina=nome_disciplina,
            )
            for id_revisao, titulo_tema, nome_disciplina in revisoes
        ]
