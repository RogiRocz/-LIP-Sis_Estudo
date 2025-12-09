from sqlalchemy.orm import Session
from src.models.disciplina import Disciplina as DisciplinaModel
from src.schemas.disciplina import DisciplinaCreate, DisciplinaUpdate

class DisciplinaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_disciplina(self, disciplina: DisciplinaCreate, usuario_id: int) -> DisciplinaModel:
        db_disciplina = DisciplinaModel(**disciplina.model_dump(), usuario_id=usuario_id)
        self.db.add(db_disciplina)
        self.db.commit()
        self.db.refresh(db_disciplina)
        return db_disciplina

    def get_disciplinas_by_user_id(self, usuario_id: int) -> list[DisciplinaModel]:
        return self.db.query(DisciplinaModel).filter(DisciplinaModel.usuario_id == usuario_id).all()

    def get_disciplina_by_id(self, disciplina_id: int, usuario_id: int) -> DisciplinaModel | None:
        return self.db.query(DisciplinaModel).filter(DisciplinaModel.ID == disciplina_id, DisciplinaModel.usuario_id == usuario_id).first()

    def update_disciplina(self, disciplina_id: int, disciplina: DisciplinaUpdate, usuario_id: int) -> DisciplinaModel | None:
        db_disciplina = self.get_disciplina_by_id(disciplina_id, usuario_id)
        if not db_disciplina:
            return None

        for key, value in disciplina.model_dump(exclude_unset=True).items():
            setattr(db_disciplina, key, value)

        self.db.commit()
        self.db.refresh(db_disciplina)
        return db_disciplina

    def delete_disciplina(self, disciplina_id: int, usuario_id: int) -> bool:
        db_disciplina = self.get_disciplina_by_id(disciplina_id, usuario_id)
        if not db_disciplina:
            return False

        self.db.delete(db_disciplina)
        self.db.commit()
        return True
