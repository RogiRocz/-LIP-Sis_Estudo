from sqlalchemy.orm import Session
from src.models.revisao import Revisao as RevisaoModel
from src.models.tema import Tema as TemaModel
from src.models.disciplina import Disciplina as DisciplinaModel
from typing import List
from datetime import date

class RevisaoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_revisao_by_id(self, revisao_id: int, usuario_id: int) -> RevisaoModel | None:
        return self.db.query(RevisaoModel).join(TemaModel).join(DisciplinaModel).filter(
            RevisaoModel.ID == revisao_id,
            DisciplinaModel.usuario_id == usuario_id
        ).first()

    def get_all_revisoes_by_user_id(self, usuario_id: int) -> List[RevisaoModel]:
        return self.db.query(RevisaoModel).join(TemaModel).join(DisciplinaModel).filter(
            DisciplinaModel.usuario_id == usuario_id
        ).all()

    def update_revisao(self, db_revisao: RevisaoModel) -> RevisaoModel:
        self.db.commit()
        self.db.refresh(db_revisao)
        return db_revisao
