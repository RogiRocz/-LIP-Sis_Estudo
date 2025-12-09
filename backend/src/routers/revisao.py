from fastapi import APIRouter, Depends, status
from src.schemas.revisao import Revisao, RevisaoUpdate
from src.models.user import User as UserModel
from src.security import get_current_user
from src.services.revisao import RevisaoService
from typing import List
from datetime import date

router = APIRouter(prefix="/revisoes", tags=["revisoes"])

@router.get("/", response_model=List[Revisao])
def get_revisoes(user: UserModel = Depends(get_current_user), service: RevisaoService = Depends()):
    return service.get_revisoes_for_user(user.ID)

@router.put("/{revisao_id}/concluir", response_model=Revisao)
def concluir_revisao(revisao_id: int, revisao_update: RevisaoUpdate, user: UserModel = Depends(get_current_user), service: RevisaoService = Depends()):
    return service.concluir_revisao(revisao_id, revisao_update, user.ID)

@router.get("/cronograma", response_model=List[Revisao])
def get_cronograma(user: UserModel = Depends(get_current_user), service: RevisaoService = Depends()):
    return service.get_cronograma(user.ID)

@router.put("/{revisao_id}/reagendar", response_model=Revisao)
def reagendar_revisao(revisao_id: int, nova_data: date, user: UserModel = Depends(get_current_user), service: RevisaoService = Depends()):
    return service.reagendar_revisao(revisao_id, nova_data, user.ID)
