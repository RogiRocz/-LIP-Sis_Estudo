from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from ..models.disciplina import Disciplina as DisciplinaModel
from ..schemas.disciplina import DisciplinaCreate, DisciplinaUpdate
from typing import Tuple, List

class DisciplinaRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_disciplina(self, disciplina: DisciplinaCreate, usuario_id: int) -> DisciplinaModel:
        db_disciplina = DisciplinaModel(**disciplina.model_dump(), usuario_id=usuario_id)
        self.db.add(db_disciplina)
        await self.db.commit()
        await self.db.refresh(db_disciplina)
        return db_disciplina

    async def get_paginated_disciplinas_by_user_id(self, usuario_id: int, skip: int, limit: int) -> Tuple[List[DisciplinaModel], int]:
        """Busca disciplinas paginadas e a contagem total."""
        # Query para contar o total de itens
        count_query = select(func.count()).select_from(DisciplinaModel).where(DisciplinaModel.usuario_id == usuario_id)
        total = await self.db.scalar(count_query)

        # Query para buscar os itens da página
        query = select(DisciplinaModel).where(DisciplinaModel.usuario_id == usuario_id).offset(skip).limit(limit)
        result = await self.db.execute(query)
        disciplinas = result.scalars().all()
        
        return disciplinas, total

    async def get_disciplina_by_id(self, disciplina_id: int, usuario_id: int) -> DisciplinaModel | None:
        query = select(DisciplinaModel).where(DisciplinaModel.ID == disciplina_id, DisciplinaModel.usuario_id == usuario_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def update_disciplina(self, disciplina_id: int, disciplina: DisciplinaUpdate, usuario_id: int) -> DisciplinaModel | None:
        db_disciplina = await self.get_disciplina_by_id(disciplina_id, usuario_id)
        if not db_disciplina:
            return None

        for key, value in disciplina.model_dump(exclude_unset=True).items():
            setattr(db_disciplina, key, value)

        await self.db.commit()
        await self.db.refresh(db_disciplina)
        return db_disciplina

    async def delete_disciplina(self, disciplina_id: int, usuario_id: int) -> bool:
        db_disciplina = await self.get_disciplina_by_id(disciplina_id, usuario_id)
        if not db_disciplina:
            return False

        await self.db.delete(db_disciplina)
        await self.db.commit()
        return True
