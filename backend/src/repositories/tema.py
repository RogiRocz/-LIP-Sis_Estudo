from sqlalchemy.orm import Session
from src.models.tema import Tema as TemaModel
from src.models.disciplina import Disciplina as DisciplinaModel
from src.models.revisao import Revisao as RevisaoModel
from src.schemas.tema import TemaCreate, TemaUpdate
from typing import List
from datetime import date, timedelta

class TemaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_disciplina_by_id(self, disciplina_id: int, usuario_id: int) -> DisciplinaModel | None:
        return self.db.query(DisciplinaModel).filter(DisciplinaModel.ID == disciplina_id, DisciplinaModel.usuario_id == usuario_id).first()

    def create_tema_with_revisions(self, tema: TemaCreate, disciplina_id: int, user_intervals: str) -> TemaModel:
        db_tema = TemaModel(**tema.model_dump(), disciplina_id=disciplina_id)
        self.db.add(db_tema)

        try:
            intervals = [int(i) for i in user_intervals.split(',')]
            self.db.flush()  # Get the ID of the new tema
            for day in intervals:
                revisao = RevisaoModel(
                    tema_id=db_tema.ID,
                    data_prevista=date.today() + timedelta(days=day),
                    tipo_revisao=f"D+{day}"
                )
                self.db.add(revisao)
            self.db.commit()
            self.db.refresh(db_tema)
        except Exception as e:
            self.db.rollback()
            raise e

        return db_tema

    def get_temas_by_disciplina_id(self, disciplina_id: int) -> List[TemaModel]:
        return self.db.query(TemaModel).filter(TemaModel.disciplina_id == disciplina_id).all()

    def get_tema_by_id(self, tema_id: int, usuario_id: int) -> TemaModel | None:
        return self.db.query(TemaModel).join(DisciplinaModel).filter(
            TemaModel.ID == tema_id,
            DisciplinaModel.usuario_id == usuario_id
        ).first()

    def update_tema(self, db_tema: TemaModel, tema_update: TemaUpdate) -> TemaModel:
        for key, value in tema_update.model_dump(exclude_unset=True).items():
            setattr(db_tema, key, value)
        self.db.commit()
        self.db.refresh(db_tema)
        return db_tema

    def delete_tema(self, db_tema: TemaModel):
        self.db.delete(db_tema)
        self.db.commit()
