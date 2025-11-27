from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from src.database import get_db
from src.schemas.disciplina import Disciplina, DisciplinaCreate, DisciplinaUpdate
from src.models.disciplina import Disciplina as DisciplinaModel
from src.models.user import User as UserModel
from src.security import get_current_user
from typing import List

router = APIRouter(prefix="/disciplinas", tags=["disciplinas"])

@router.post("/", response_model=Disciplina)
def create_disciplina(disciplina: DisciplinaCreate, user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    db_disciplina = DisciplinaModel(**disciplina.model_dump(), usuario_id=user.ID)
    db.add(db_disciplina)
    db.commit()
    db.refresh(db_disciplina)
    return db_disciplina

@router.get("/", response_model=List[Disciplina])
def get_disciplinas(user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(DisciplinaModel).filter(DisciplinaModel.usuario_id == user.ID).all()

@router.get("/{disciplina_id}", response_model=Disciplina)
def get_disciplina(disciplina_id: int, user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    db_disciplina = db.query(DisciplinaModel).filter(DisciplinaModel.ID == disciplina_id, DisciplinaModel.usuario_id == user.ID).first()
    if not db_disciplina:
        raise HTTPException(status_code=404, detail="Disciplina not found")
    return db_disciplina

@router.put("/{disciplina_id}", response_model=Disciplina)
def update_disciplina(disciplina_id: int, disciplina: DisciplinaUpdate, user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    db_disciplina = db.query(DisciplinaModel).filter(DisciplinaModel.ID == disciplina_id, DisciplinaModel.usuario_id == user.ID).first()
    if not db_disciplina:
        raise HTTPException(status_code=404, detail="Disciplina not found")

    for key, value in disciplina.model_dump(exclude_unset=True).items():
        setattr(db_disciplina, key, value)

    db.commit()
    db.refresh(db_disciplina)
    return db_disciplina

@router.delete("/{disciplina_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_disciplina(disciplina_id: int, user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    db_disciplina = db.query(DisciplinaModel).filter(DisciplinaModel.ID == disciplina_id, DisciplinaModel.usuario_id == user.ID).first()
    if not db_disciplina:
        raise HTTPException(status_code=404, detail="Disciplina not found")

    db.delete(db_disciplina)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
