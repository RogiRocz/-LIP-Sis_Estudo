from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.tema import Tema as TemaModel
from ..models.disciplina import Disciplina as DisciplinaModel
from ..models.revisao import Revisao as RevisaoModel
from ..schemas.tema import TemaCreate, TemaUpdate
from typing import List
from datetime import date, timedelta

class TemaRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_disciplina_by_id(self, disciplina_id: int, usuario_id: int) -> DisciplinaModel | None:
        query = select(DisciplinaModel).where(DisciplinaModel.ID == disciplina_id, DisciplinaModel.usuario_id == usuario_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def create_tema_with_revisions(self, tema: TemaCreate, disciplina_id: int, user_intervals: str) -> TemaModel:
        db_tema = TemaModel(**tema.model_dump(), disciplina_id=disciplina_id)
        self.db.add(db_tema)

        try:
            intervals = [int(i) for i in user_intervals.split(',')]
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

    async def get_temas_by_disciplina_id(self, disciplina_id: int) -> List[TemaModel]:
        query = select(TemaModel).where(TemaModel.disciplina_id == disciplina_id)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_tema_by_id(self, tema_id: int, usuario_id: int) -> TemaModel | None:
        query = select(TemaModel).join(DisciplinaModel).where(
            TemaModel.ID == tema_id,
            DisciplinaModel.usuario_id == usuario_id
        )
        result = await self.db.execute(query)
        return result.scalars().first()

    async def update_tema(self, db_tema: TemaModel, tema_update: TemaUpdate) -> TemaModel:
        for key, value in tema_update.model_dump(exclude_unset=True).items():
            setattr(db_tema, key, value)
        await self.db.commit()
        await self.db.refresh(db_tema)
        return db_tema

    async def delete_tema(self, db_tema: TemaModel):
        await self.db.delete(db_tema)
        await self.db.commit()
