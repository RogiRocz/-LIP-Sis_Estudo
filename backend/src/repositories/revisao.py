from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.revisao import Revisao as RevisaoModel
from ..models.tema import Tema as TemaModel
from ..models.disciplina import Disciplina as DisciplinaModel
from typing import List

class RevisaoRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_revisao_by_id(self, revisao_id: int, user_id: int) -> RevisaoModel | None:
        query = (
            select(RevisaoModel)
            .join(TemaModel)
            .join(DisciplinaModel)
            .where(RevisaoModel.ID == revisao_id, DisciplinaModel.usuario_id == user_id)
        )
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_all_revisoes_by_user_id(self, user_id: int) -> List[RevisaoModel]:
        query = (
            select(RevisaoModel)
            .join(TemaModel)
            .join(DisciplinaModel)
            .where(DisciplinaModel.usuario_id == user_id)
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def update_revisao(self, db_revisao: RevisaoModel) -> RevisaoModel:
        await self.db.commit()
        await self.db.refresh(db_revisao)
        return db_revisao
