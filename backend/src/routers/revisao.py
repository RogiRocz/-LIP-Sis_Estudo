from fastapi import APIRouter, Depends, status
from schemas.revisao import Revisao, RevisaoUpdate
from models.user import User as UserModel
from security import get_current_user
from services.revisao import RevisaoService
from typing import List
from datetime import date

router = APIRouter(prefix="/revisoes", tags=["revisoes"])

@router.get("/", response_model=List[Revisao])
async def get_revisoes(user: UserModel = Depends(get_current_user), service: RevisaoService = Depends()):
    return await service.get_revisoes_for_user(user.id)

@router.put("/{revisao_id}/concluir", response_model=Revisao)
async def concluir_revisao(revisao_id: int, revisao_update: RevisaoUpdate, user: UserModel = Depends(get_current_user), service: RevisaoService = Depends()):
    return await service.concluir_revisao(revisao_id, revisao_update, user.id)

@router.get("/cronograma", response_model=List[Revisao])
async def get_cronograma(user: UserModel = Depends(get_current_user), service: RevisaoService = Depends()):
    return await service.get_cronograma(user.id)

@router.put("/{revisao_id}/reagendar", response_model=Revisao)
async def reagendar_revisao(revisao_id: int, nova_data: date, user: UserModel = Depends(get_current_user), service: RevisaoService = Depends()):
    return await service.reagendar_revisao(revisao_id, nova_data, user.id)
