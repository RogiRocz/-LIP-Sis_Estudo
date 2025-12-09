from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.repositories.revisao import RevisaoRepository
from src.schemas.revisao import RevisaoUpdate
from src.models.revisao import Revisao as RevisaoModel
from typing import List
from datetime import datetime, date

class RevisaoService:
    def __init__(self, db: Session = Depends(get_db)):
        self.repo = RevisaoRepository(db)

    def get_revisoes_for_user(self, user_id: int) -> List[RevisaoModel]:
        return self.repo.get_all_revisoes_by_user_id(user_id)

    def _get_revisao_and_validate_ownership(self, revisao_id: int, user_id: int) -> RevisaoModel:
        db_revisao = self.repo.get_revisao_by_id(revisao_id, user_id)
        if not db_revisao:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Revisao not found")
        return db_revisao

    def concluir_revisao(self, revisao_id: int, revisao_update: RevisaoUpdate, user_id: int) -> RevisaoModel:
        db_revisao = self._get_revisao_and_validate_ownership(revisao_id, user_id)

        db_revisao.status = "REALIZADA"
        db_revisao.data_realizada = revisao_update.data_realizada or datetime.now()
        db_revisao.tempo_minutos = revisao_update.tempo_minutos

        return self.repo.update_revisao(db_revisao)

    def get_cronograma(self, user_id: int) -> List[RevisaoModel]:
        # This logic is identical to get_revisoes for now, but can be expanded
        return self.get_revisoes_for_user(user_id)

    def reagendar_revisao(self, revisao_id: int, nova_data: date, user_id: int) -> RevisaoModel:
        db_revisao = self._get_revisao_and_validate_ownership(revisao_id, user_id)

        db_revisao.data_prevista = nova_data
        if nova_data >= date.today():
            db_revisao.status = "PENDENTE"

        return self.repo.update_revisao(db_revisao)
