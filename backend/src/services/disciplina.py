from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..repositories.disciplina import DisciplinaRepository
from ..schemas.disciplina import DisciplinaCreate, DisciplinaUpdate
from ..models.disciplina import Disciplina as DisciplinaModel

class DisciplinaService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.repo = DisciplinaRepository(db)

    async def create_disciplina(self, disciplina: DisciplinaCreate, usuario_id: int) -> DisciplinaModel:
        return await self.repo.create_disciplina(disciplina, usuario_id)

    async def get_disciplinas(self, usuario_id: int) -> list[DisciplinaModel]:
        return await self.repo.get_disciplinas_by_user_id(usuario_id)

    async def get_disciplina(self, disciplina_id: int, usuario_id: int) -> DisciplinaModel:
        db_disciplina = await self.repo.get_disciplina_by_id(disciplina_id, usuario_id)
        if not db_disciplina:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Disciplina not found")
        return db_disciplina

    async def update_disciplina(self, disciplina_id: int, disciplina: DisciplinaUpdate, usuario_id: int) -> DisciplinaModel:
        db_disciplina = await self.repo.update_disciplina(disciplina_id, disciplina, usuario_id)
        if not db_disciplina:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Disciplina not found")
        return db_disciplina

    async def delete_disciplina(self, disciplina_id: int, usuario_id: int):
        success = await self.repo.delete_disciplina(disciplina_id, usuario_id)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Disciplina not found")
        return
