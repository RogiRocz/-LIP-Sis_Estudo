from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case
from datetime import date, timedelta
from ..models.user import User
from ..models.revisao import Revisao
from ..schemas.painel import Estatisticas, EvolucaoSemanal, RevisoesDoDia

class PainelService:
    async def get_estatisticas(self, db: AsyncSession, user: User) -> Estatisticas:
        """Calculates and returns study statistics for the user."""

        revisao_query = select(Revisao).join(Revisao.tema).where(Revisao.tema.has(usuario_id=user.ID))

        result = await db.execute(
            select(
                func.sum(case((Revisao.status == 'REALIZADA', Revisao.tempo_dedicado), else_=0)).label('tempo_total'),
                func.count(case((Revisao.status == 'REALIZADA', 1), else_=None)).label('sessoes_completas')
            ).select_from(revisao_query.subquery())
        )
        stats = result.one_or_none()

        tempo_total_minutos = stats.tempo_total or 0
        horas = tempo_total_minutos // 60
        minutos = tempo_total_minutos % 60

        # NOTE: Dias seguidos requires a more complex logic involving daily login tracking,
        # which is out of the current scope. Returning a placeholder.
        return Estatisticas(
            tempo_total=f"{horas}h {minutos}m",
            sessoes_completas=stats.sessoes_completas or 0,
            dias_seguidos=0  # Placeholder
        )

    async def get_evolucao_semanal(self, db: AsyncSession, user: User) -> EvolucaoSemanal:
        """Returns data for the weekly study evolution chart."""
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())

        labels = [(start_of_week + timedelta(days=i)).strftime("%a") for i in range(7)]

        revisao_query = select(
            func.date(Revisao.data_realizada).label('dia'),
            func.sum(Revisao.tempo_dedicado).label('total_minutos')
        ).join(Revisao.tema).where(
            Revisao.tema.has(usuario_id=user.ID),
            Revisao.status == 'REALIZADA',
            Revisao.data_realizada >= start_of_week
        ).group_by('dia').order_by('dia')

        result = await db.execute(revisao_query)
        daily_data = {row.dia.strftime("%a"): (row.total_minutos / 60.0) for row in result.all()}

        dataset_data = [daily_data.get(label, 0) for label in labels]

        return EvolucaoSemanal(
            labels=labels,
            datasets=[
                {
                    "label": "Horas Estudadas",
                    "backgroundColor": "#17a2b8",
                    "data": dataset_data
                }
            ]
        )

    async def get_revisoes_do_dia(self, db: AsyncSession, user: User) -> RevisoesDoDia:
        """Fetches scheduled revisions for today and those that are overdue."""
        today = date.today()

        atrasadas_query = select(Revisao).join(Revisao.tema).where(
            Revisao.tema.has(usuario_id=user.ID),
            Revisao.status == 'PENDENTE',
            Revisao.data_prevista < today
        ).order_by(Revisao.data_prevista.asc())

        hoje_query = select(Revisao).join(Revisao.tema).where(
            Revisao.tema.has(usuario_id=user.ID),
            Revisao.status == 'PENDENTE',
            Revisao.data_prevista == today
        )

        atrasadas_result = await db.execute(atrasadas_query)
        hoje_result = await db.execute(hoje_query)

        return RevisoesDoDia(
            atrasadas=atrasadas_result.scalars().all(),
            hoje=hoje_result.scalars().all()
        )
