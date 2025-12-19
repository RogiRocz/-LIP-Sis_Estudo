from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..repositories.tema import TemaRepository
from ..schemas.tema import TemaCreate, TemaUpdate
from ..models.user import User as UserModel
from ..models.tema import Tema as TemaModel
from typing import Dict, Any

class TemaService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.repo = TemaRepository(db)

    async def create_tema_for_disciplina(self, disciplina_id: int, tema: TemaCreate, user: UserModel) -> TemaModel:
        db_disciplina = await self.repo.get_disciplina_by_id(disciplina_id, user.ID)
        if not db_disciplina:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Disciplina não encontrada")

        try:
            return await self.repo.create_tema_with_revisions(tema, disciplina_id, user.intervalo_revisoes)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao criar tema")

    async def get_temas_by_disciplina(self, disciplina_id: int, user_id: int, page: int, size: int) -> Dict[str, Any]:
        db_disciplina = await self.repo.get_disciplina_by_id(disciplina_id, user_id)
        if not db_disciplina:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Disciplina não encontrada")
        
        if page < 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A página tem que ser maior ou igual a 1")
        if size < 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O tamanho tem que ser maior ou igual a 1")
            
        skip = (page - 1) * size
        limit = size
        
        temas, total = await self.repo.get_paginated_temas_by_disciplina_id(disciplina_id, skip, limit)
        
        return {
            "items": temas,
            "total": total,
            "page": page,
            "size": size,
        }

    async def get_tema(self, tema_id: int, user_id: int) -> TemaModel:
        db_tema = await self.repo.get_tema_by_id(tema_id, user_id)
        if not db_tema:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tema não encontrado")
        return db_tema

    async def update_tema(self, tema_id: int, tema_update: TemaUpdate, user_id: int) -> TemaModel:
        db_tema = await self.get_tema(tema_id, user_id)
        return await self.repo.update_tema(db_tema, tema_update)

    async def delete_tema(self, tema_id: int, user_id: int):
        db_tema = await self.get_tema(tema_id, user_id)
        await self.repo.delete_tema(db_tema)
