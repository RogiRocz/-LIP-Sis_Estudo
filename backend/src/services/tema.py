from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.repositories.tema import TemaRepository
from src.schemas.tema import TemaCreate, TemaUpdate
from src.models.user import User as UserModel
from src.models.tema import Tema as TemaModel
from typing import List

class TemaService:
    def __init__(self, db: Session = Depends(get_db)):
        self.repo = TemaRepository(db)

    def create_tema_for_disciplina(self, disciplina_id: int, tema: TemaCreate, user: UserModel) -> TemaModel:
        db_disciplina = self.repo.get_disciplina_by_id(disciplina_id, user.ID)
        if not db_disciplina:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Disciplina not found")

        try:
            return self.repo.create_tema_with_revisions(tema, disciplina_id, user.intervalo_revisoes)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create revisions: {e}")

    def get_temas_by_disciplina(self, disciplina_id: int, user_id: int) -> List[TemaModel]:
        db_disciplina = self.repo.get_disciplina_by_id(disciplina_id, user_id)
        if not db_disciplina:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Disciplina not found")
        return self.repo.get_temas_by_disciplina_id(disciplina_id)

    def get_tema(self, tema_id: int, user_id: int) -> TemaModel:
        db_tema = self.repo.get_tema_by_id(tema_id, user_id)
        if not db_tema:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tema not found")
        return db_tema

    def update_tema(self, tema_id: int, tema_update: TemaUpdate, user_id: int) -> TemaModel:
        db_tema = self.get_tema(tema_id, user_id) # Reuse get_tema to ensure it exists and user has access
        return self.repo.update_tema(db_tema, tema_update)

    def delete_tema(self, tema_id: int, user_id: int):
        db_tema = self.get_tema(tema_id, user_id) # Reuse get_tema for validation
        self.repo.delete_tema(db_tema)
