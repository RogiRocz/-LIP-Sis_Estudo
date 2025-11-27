from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from src.database import get_db
from src.schemas.tema import Tema, TemaCreate, TemaUpdate
from src.models.tema import Tema as TemaModel
from src.models.disciplina import Disciplina as DisciplinaModel
from src.models.revisao import Revisao as RevisaoModel
from src.models.user import User as UserModel
from src.security import get_current_user
from typing import List
from datetime import date, timedelta

# Router for nested endpoints under /disciplinas/{disciplina_id}/temas
disciplina_tema_router = APIRouter(prefix="/disciplinas/{disciplina_id}/temas", tags=["temas"])

# Router for top-level /temas endpoints
tema_router = APIRouter(prefix="/temas", tags=["temas"])

@disciplina_tema_router.post("/", response_model=Tema)
def create_tema(disciplina_id: int, tema: TemaCreate, user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    db_disciplina = db.query(DisciplinaModel).filter(DisciplinaModel.ID == disciplina_id, DisciplinaModel.usuario_id == user.ID).first()
    if not db_disciplina:
        raise HTTPException(status_code=404, detail="Disciplina not found")

    db_tema = TemaModel(**tema.model_dump(), disciplina_id=disciplina_id)
    db.add(db_tema)

    # Create virtual revisions in the same transaction
    try:
        intervals = [int(i) for i in user.intervalo_revisoes.split(',')]
        # We need to flush to get the ID of the new tema before creating the revisoes
        db.flush()
        for day in intervals:
            revisao = RevisaoModel(
                tema_id=db_tema.ID,
                data_prevista=date.today() + timedelta(days=day),
                tipo_revisao=f"D+{day}"
            )
            db.add(revisao)
        db.commit()
        db.refresh(db_tema)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create revisions: {e}")

    return db_tema

@disciplina_tema_router.get("/", response_model=List[Tema])
def get_temas_by_disciplina(disciplina_id: int, user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    db_disciplina = db.query(DisciplinaModel).filter(DisciplinaModel.ID == disciplina_id, DisciplinaModel.usuario_id == user.ID).first()
    if not db_disciplina:
        raise HTTPException(status_code=404, detail="Disciplina not found")

    return db.query(TemaModel).filter(TemaModel.disciplina_id == disciplina_id).all()

@tema_router.get("/{tema_id}", response_model=Tema)
def get_tema(tema_id: int, user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    db_tema = db.query(TemaModel).join(DisciplinaModel).filter(TemaModel.ID == tema_id, DisciplinaModel.usuario_id == user.ID).first()
    if not db_tema:
        raise HTTPException(status_code=404, detail="Tema not found")
    return db_tema

@tema_router.put("/{tema_id}", response_model=Tema)
def update_tema(tema_id: int, tema: TemaUpdate, user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    db_tema = db.query(TemaModel).join(DisciplinaModel).filter(TemaModel.ID == tema_id, DisciplinaModel.usuario_id == user.ID).first()
    if not db_tema:
        raise HTTPException(status_code=404, detail="Tema not found")

    for key, value in tema.model_dump(exclude_unset=True).items():
        setattr(db_tema, key, value)

    db.commit()
    db.refresh(db_tema)
    return db_tema

@tema_router.delete("/{tema_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tema(tema_id: int, user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    db_tema = db.query(TemaModel).join(DisciplinaModel).filter(TemaModel.ID == tema_id, DisciplinaModel.usuario_id == user.ID).first()
    if not db_tema:
        raise HTTPException(status_code=404, detail="Tema not found")

    db.delete(db_tema)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
