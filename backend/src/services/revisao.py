from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..repositories.revisao import RevisaoRepository
from ..schemas.revisao import RevisaoUpdate
from ..models.revisao import Revisao as RevisaoModel
from .tema import TemaService
from typing import Dict, Any, List
from datetime import datetime, date


class RevisaoService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.repo = RevisaoRepository(db)
        self.tema_service = TemaService(db)

    async def get_revisoes_for_user(
        self, user_id: int, page: int, size: int
    ) -> Dict[str, Any]:
        if page < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A página tem que ser maior ou igual a 1",
            )
        if size < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O tamanho tem que ser maior ou igual a 1",
            )

        skip = (page - 1) * size
        limit = size

        revisoes, total = await self.repo.get_paginated_all_revisoes_by_user_id(
            user_id, skip, limit
        )

        return {
            "items": revisoes,
            "total": total,
            "page": page,
            "size": size,
        }

    async def _get_revisao_and_validate_ownership(
        self, revisao_id: int, user_id: int
    ) -> RevisaoModel:
        db_revisao = await self.repo.get_revisao_by_id(revisao_id, user_id)
        if not db_revisao:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Revisão não encontrada"
            )
        return db_revisao

    async def update_revisao(
        self, revisao_id: int, revisao_update: RevisaoUpdate, user_id: int
    ) -> RevisaoModel:
        db_revisao = await self._get_revisao_and_validate_ownership(revisao_id, user_id)

        update_data = revisao_update.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_revisao, field, value)

        return await self.repo.update_revisao(db_revisao)

    async def concluir_revisao(
        self, revisao_id: int, revisao_update: RevisaoUpdate, user_id: int
    ) -> RevisaoModel:
        db_revisao = await self._get_revisao_and_validate_ownership(revisao_id, user_id)

        update_data = revisao_update.model_dump(exclude_unset=True)

        db_revisao.status = "REALIZADA"
        db_revisao.data_realizada = update_data.get("data_realizada", datetime.now())

        if "tempo_dedicado" in update_data:
            db_revisao.tempo_dedicado = update_data["tempo_dedicado"]

        if "descricao" in update_data:
            db_revisao.descricao = update_data["descricao"]

        return await self.repo.update_revisao(db_revisao)

    async def get_cronograma(
        self, user_id: int, page: int, size: int
    ) -> Dict[str, Any]:
        if page < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A página tem que ser maior ou igual a 1",
            )
        if size < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O tamanho tem que ser maior ou igual a 1",
            )

        skip = (page - 1) * size
        limit = size

        revisoes, total = await self.repo.get_paginated_cronograma_by_user_id(
            user_id, skip, limit
        )

        return {
            "items": revisoes,
            "total": total,
            "page": page,
            "size": size,
        }

    async def reagendar_revisao(
        self, revisao_id: int, nova_data: date, user_id: int
    ) -> RevisaoModel:
        db_revisao = await self._get_revisao_and_validate_ownership(revisao_id, user_id)

        db_revisao.data_prevista = nova_data
        if nova_data.isoformat() >= date.today().isoformat():
            db_revisao.status = "PENDENTE"

        return await self.repo.update_revisao(db_revisao)