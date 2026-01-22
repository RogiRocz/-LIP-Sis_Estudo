from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, text
from datetime import date, timedelta
from ..models.disciplina import Disciplina
from ..models.tema import Tema
from ..models.revisao import Revisao
from ..models.user import User
from ..schemas.painel import EstatisticasGerais, EvolucaoSemanal, RevisaoDoDia
from fastapi import Depends
from ..database import get_db


class PainelService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_estatisticas_gerais(self, usuario_id: int) -> EstatisticasGerais:
        total_disciplinas_query = select(func.count(Disciplina.ID)).filter(
            Disciplina.usuario_id == usuario_id
        )
        total_disciplinas = await self.db.scalar(total_disciplinas_query) or 0

        total_temas_query = (
            select(func.count(Tema.ID))
            .join(Disciplina, Tema.disciplina_id == Disciplina.ID)
            .filter(Disciplina.usuario_id == usuario_id)
        )
        total_temas = await self.db.scalar(total_temas_query) or 0

        total_revisoes_query = (
            select(func.count(Revisao.ID))
            .join(Tema, Revisao.tema_id == Tema.ID)
            .join(Disciplina, Tema.disciplina_id == Disciplina.ID)
            .filter(Disciplina.usuario_id == usuario_id)
        )
        total_revisoes = await self.db.scalar(total_revisoes_query) or 0

        revisoes_hoje_query = (
            select(func.count(Revisao.ID))
            .join(Tema, Revisao.tema_id == Tema.ID)
            .join(Disciplina, Tema.disciplina_id == Disciplina.ID)
            .filter(
                Disciplina.usuario_id == usuario_id,
                Revisao.data_prevista == date.today(),
            )
        )
        revisoes_hoje = await self.db.scalar(revisoes_hoje_query) or 0

        return EstatisticasGerais(
            total_disciplinas=total_disciplinas,
            total_temas=total_temas,
            total_revisoes=total_revisoes,
            revisoes_hoje=revisoes_hoje,
        )

    async def get_evolucao_semanal(self, usuario_id: int) -> list[EvolucaoSemanal]:
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
                Revisao.data_prevista <= today,
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
                EvolucaoSemanal(
                    data=current_date,
                    revisoes_realizadas=revisoes_dict.get(current_date, 0),
                )
            )

        return evolucao

    async def get_revisoes_do_dia(self, usuario_id: int) -> list[RevisaoDoDia]:
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
            RevisaoDoDia(
                id_revisao=id_revisao,
                titulo_tema=titulo_tema,
                nome_disciplina=nome_disciplina,
            )
            for id_revisao, titulo_tema, nome_disciplina in revisoes
        ]

    async def get_relatorio_detalhado(self, user_id: int):
        stmt_disc = select(Disciplina).filter(Disciplina.usuario_id == user_id)
        result_disc = await self.db.execute(stmt_disc)
        disciplinas = result_disc.scalars().all()

        relatorio_lista = []
        total_minutos_geral = 0

        for disc in disciplinas:
            stmt_temas = select(Tema).filter(Tema.disciplina_id == disc.ID)
            result_temas = await self.db.execute(stmt_temas)
            temas = result_temas.scalars().all()

            minutos_disc = 0
            concluidas = 0
            pendentes = 0

            for tema in temas:
                stmt_revs = select(Revisao).filter(Revisao.tema_id == tema.ID)
                result_revs = await self.db.execute(stmt_revs)
                revisoes = result_revs.scalars().all()

                for rev in revisoes:
                    minutos_disc += rev.tempo_dedicado or 0
                    if rev.status in ["REALIZADA", "concluida"]:
                        concluidas += 1
                    else:
                        pendentes += 1

            total_minutos_geral += minutos_disc
            relatorio_lista.append(
                {
                    "subject": disc.nome,
                    "studyMinutes": minutos_disc,
                    "revisionsDone": concluidas,
                    "revisionsPending": pendentes,
                }
            )

        return {
            "totalHours": round(total_minutos_geral / 60, 1),
            "data": relatorio_lista,
        }
