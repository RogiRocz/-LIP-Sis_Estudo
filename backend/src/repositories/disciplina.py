from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.disciplina import Disciplina as DisciplinaModel
from ..schemas.disciplina import DisciplinaCreate, DisciplinaUpdate

class DisciplinaRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_disciplina(self, disciplina: DisciplinaCreate, usuario_id: int) -> DisciplinaModel:
        db_disciplina = DisciplinaModel(**disciplina.model_dump(), usuario_id=usuario_id)
        self.db.add(db_disciplina)
        await self.db.commit()
        await self.db.refresh(db_disciplina)
        return db_disciplina

    async def get_disciplinas_by_user_id(self, usuario_id: int) -> list[DisciplinaModel]:
        query = select(DisciplinaModel).where(DisciplinaModel.usuario_id == usuario_id)
        result = await self.db.execute(query)
        return result.scalars().all()

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
