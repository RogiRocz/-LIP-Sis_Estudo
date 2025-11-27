from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.schemas.revisao import Revisao, RevisaoUpdate
from src.models.revisao import Revisao as RevisaoModel
from src.models.tema import Tema as TemaModel
from src.models.disciplina import Disciplina as DisciplinaModel
from src.models.user import User as UserModel
from src.security import get_current_user
from typing import List
from datetime import datetime, date

router = APIRouter(prefix="/revisoes", tags=["revisoes"])

@router.get("/", response_model=List[Revisao])
def get_revisoes(user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(RevisaoModel).join(TemaModel).join(DisciplinaModel).filter(DisciplinaModel.usuario_id == user.ID).all()

@router.put("/{revisao_id}/concluir", response_model=Revisao)
def concluir_revisao(revisao_id: int, revisao_update: RevisaoUpdate, user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    db_revisao = db.query(RevisaoModel).join(TemaModel).join(DisciplinaModel).filter(RevisaoModel.ID == revisao_id, DisciplinaModel.usuario_id == user.ID).first()
    if not db_revisao:
        raise HTTPException(status_code=404, detail="Revisao not found")

    db_revisao.status = "REALIZADA"
    db_revisao.data_realizada = revisao_update.data_realizada or datetime.now()
    db_revisao.tempo_minutos = revisao_update.tempo_minutos

    db.commit()
    db.refresh(db_revisao)
    return db_revisao

@router.get("/cronograma", response_model=List[Revisao])
def get_cronograma(user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    revisoes = db.query(RevisaoModel).join(TemaModel).join(DisciplinaModel).filter(DisciplinaModel.usuario_id == user.ID).all()
    return revisoes

@router.put("/{revisao_id}/reagendar", response_model=Revisao)
def reagendar_revisao(revisao_id: int, nova_data: date, user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    db_revisao = db.query(RevisaoModel).join(TemaModel).join(DisciplinaModel).filter(RevisaoModel.ID == revisao_id, DisciplinaModel.usuario_id == user.ID).first()
    if not db_revisao:
        raise HTTPException(status_code=404, detail="Revisao not found")

    db_revisao.data_prevista = nova_data
    if nova_data >= date.today():
        db_revisao.status = "PENDENTE"

    db.commit()
    db.refresh(db_revisao)
    return db_revisao
