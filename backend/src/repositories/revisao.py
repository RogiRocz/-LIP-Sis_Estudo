from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete
from ..models.revisao import Revisao as RevisaoModel
from ..models.tema import Tema as TemaModel
from ..models.disciplina import Disciplina as DisciplinaModel
from typing import List, Tuple
from sqlalchemy.orm import joinedload

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

    async def get_paginated_all_revisoes_by_user_id(self, user_id: int, skip: int, limit: int) -> Tuple[List[RevisaoModel], int]:
        """Busca todas as revisões de um usuário com paginação."""
        base_query = (
            select(RevisaoModel)
            .join(TemaModel)
            .join(DisciplinaModel)
            .where(DisciplinaModel.usuario_id == user_id)
            .options(joinedload(RevisaoModel.tema).joinedload(TemaModel.disciplina))
        )

        count_query = select(func.count()).select_from(base_query.subquery())
        total = await self.db.scalar(count_query)

        items_query = base_query.order_by(RevisaoModel.data_prevista.desc()).offset(skip).limit(limit)
        result = await self.db.execute(items_query)
        revisoes = result.scalars().all()

        return revisoes, total
        
    async def get_paginated_cronograma_by_user_id(self, user_id: int, skip: int, limit: int) -> Tuple[List[RevisaoModel], int]:
        """Busca o cronograma (revisões pendentes) de um usuário com paginação."""
        base_query = (
            select(RevisaoModel)
            .join(TemaModel)
            .join(DisciplinaModel)
            .where(
                DisciplinaModel.usuario_id == user_id,
                RevisaoModel.status == "PENDENTE"
            )
        )
        
        count_query = select(func.count()).select_from(base_query.subquery())
        total = await self.db.scalar(count_query)

        items_query = base_query.order_by(RevisaoModel.data_prevista.asc()).offset(skip).limit(limit)
        result = await self.db.execute(items_query)
        revisoes = result.scalars().all()
        
        return revisoes, total

    async def update_revisao(self, db_revisao: RevisaoModel) -> RevisaoModel:
        await self.db.commit()
        await self.db.refresh(db_revisao)
        return db_revisao

    async def delete_revisao(self, db_revisao: RevisaoModel) -> None:
        await self.db.delete(db_revisao)
        await self.db.commit()
        return
