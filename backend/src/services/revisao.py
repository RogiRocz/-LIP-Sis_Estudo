from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from repositories.revisao import RevisaoRepository
from schemas.revisao import RevisaoUpdate
from models.revisao import Revisao as RevisaoModel
from typing import List
from datetime import datetime, date

class RevisaoService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.repo = RevisaoRepository(db)

    async def get_revisoes_for_user(self, user_id: int) -> List[RevisaoModel]:
        return await self.repo.get_all_revisoes_by_user_id(user_id)

    async def _get_revisao_and_validate_ownership(self, revisao_id: int, user_id: int) -> RevisaoModel:
        db_revisao = await self.repo.get_revisao_by_id(revisao_id, user_id)
        if not db_revisao:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Revisao not found")
        return db_revisao

    async def concluir_revisao(self, revisao_id: int, revisao_update: RevisaoUpdate, user_id: int) -> RevisaoModel:
        db_revisao = await self._get_revisao_and_validate_ownership(revisao_id, user_id)

        update_data = revisao_update.model_dump(exclude_unset=True)

        db_revisao.status = "REALIZADA"
        db_revisao.data_realizada = update_data.get("data_realizada", datetime.now())
        
        if "tempo_minutos" in update_data:
            db_revisao.tempo_minutos = update_data["tempo_minutos"]

        if "descricao" in update_data:
            db_revisao.descricao = update_data["descricao"]

        return await self.repo.update_revisao(db_revisao)

    async def get_cronograma(self, user_id: int) -> List[RevisaoModel]:
        return await self.get_revisoes_for_user(user_id)

    async def reagendar_revisao(self, revisao_id: int, nova_data: date, user_id: int) -> RevisaoModel:
        db_revisao = await self._get_revisao_and_validate_ownership(revisao_id, user_id)

        db_revisao.data_prevista = nova_data
        if nova_data.isoformat() >= date.today().isoformat(): # Compare as strings
            db_revisao.status = "PENDENTE"

        return await self.repo.update_revisao(db_revisao)
