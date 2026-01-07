from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from ..models.tema import Tema as TemaModel
from ..models.disciplina import Disciplina as DisciplinaModel
from ..models.revisao import Revisao as RevisaoModel
from ..schemas.tema import TemaCreate, TemaUpdate
from typing import List, Tuple
from datetime import date, timedelta


class TemaRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_disciplina_by_id(
        self, disciplina_id: int, usuario_id: int
    ) -> DisciplinaModel | None:
        query = select(DisciplinaModel).where(
            DisciplinaModel.ID == disciplina_id,
            DisciplinaModel.usuario_id == usuario_id,
        )
        result = await self.db.execute(query)
        return result.scalars().first()

    async def create_tema_with_revisions(
        self, tema: TemaCreate, disciplina_id: int, intervals: list[int]
    ) -> TemaModel:
        db_tema = TemaModel(**tema.model_dump(exclude={'intervalos'}), disciplina_id=disciplina_id)
        self.db.add(db_tema)

        try:
            await self.db.flush()  # Get the ID of the new tema
            for day in intervals:
                revisao = RevisaoModel(
                    tema_id=db_tema.ID,
                    data_prevista=date.today() + timedelta(days=day),
                )
                self.db.add(revisao)
            await self.db.commit()
            await self.db.refresh(db_tema)
        except Exception as e:
            await self.db.rollback()
            raise e

        return db_tema

    async def get_paginated_temas_by_disciplina_id(
        self, disciplina_id: int, skip: int, limit: int
    ) -> Tuple[List[TemaModel], int]:
        """Busca temas paginados por disciplina e a contagem total."""
        count_query = (
            select(func.count())
            .select_from(TemaModel)
            .where(TemaModel.disciplina_id == disciplina_id)
        )
        total = await self.db.scalar(count_query)

        query = (
        select(TemaModel)
        .where(TemaModel.disciplina_id == disciplina_id)
        .order_by(TemaModel.ID.desc()) # Pega os mais recentes primeiro
        .offset(skip)
        .limit(limit)
        )
        result = await self.db.execute(query)
        # O unique() é essencial para evitar duplicados em joins
        temas = result.scalars().unique().all()
        
        return temas, total

    async def get_tema_by_id(self, tema_id: int, usuario_id: int) -> TemaModel | None:
        query = (
            select(TemaModel)
            .join(DisciplinaModel)
            .where(TemaModel.ID == tema_id, DisciplinaModel.usuario_id == usuario_id)
        )
        result = await self.db.execute(query)
        return result.scalars().first()

    async def update_tema(
        self, db_tema: TemaModel, tema_update: TemaUpdate
    ) -> TemaModel:
        try: 
            for key, value in tema_update.model_dump(
                exclude={"intervalos"}, exclude_unset=True
            ).items():
                setattr(db_tema, key, value)

            if tema_update.intervalos is not None:
                stmt = delete(RevisaoModel).where(
                    RevisaoModel.tema_id == db_tema.ID, RevisaoModel.status == "PENDENTE"
                )
                await self.db.execute(stmt)

            base_date = db_tema.criado_em.date() if db_tema.criado_em else date.today()
            for day in tema_update.intervalos:
                nova_revisao = RevisaoModel(
                    tema_id=db_tema.ID, data_prevista=base_date + timedelta(days=day)
                )
                self.db.add(nova_revisao)
        except Exception as e:
            await self.db.rollback()
            raise e
        finally:
            await self.db.commit()
            await self.db.refresh(db_tema)
        
        return db_tema

    async def delete_tema(self, db_tema: TemaModel):
        await self.db.delete(db_tema)
        await self.db.commit()
