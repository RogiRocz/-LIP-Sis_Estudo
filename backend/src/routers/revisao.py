from fastapi import APIRouter, Depends, Query, status, Response
from ..schemas.revisao import Revisao, RevisaoUpdate
from ..schemas.pagination import Page
from ..models.user import User as UserModel
from ..security import get_current_user
from ..services.revisao import RevisaoService
from datetime import date

router = APIRouter(prefix="/revisoes", tags=["revisoes"])

@router.get("/", response_model=Page[Revisao])
async def get_revisoes(
    user: UserModel = Depends(get_current_user), 
    service: RevisaoService = Depends(),
    page: int = Query(1, ge=1, description="Número da página"),
    size: int = Query(10, ge=1, le=100, description="Tamanho da página")
):
    return await service.get_revisoes_for_user(user.ID, page, size)

@router.put("/{revisao_id}", response_model=Revisao)
async def update_revisao(
    revisao_id: int,
    revisao: RevisaoUpdate,
    user: UserModel = Depends(get_current_user),
    service: RevisaoService = Depends(),
):
    return await service.update_revisao(revisao_id, revisao, user.ID)

@router.put("/{revisao_id}/concluir", response_model=Revisao)
async def concluir_revisao(revisao_id: int, revisao: RevisaoUpdate, user: UserModel = Depends(get_current_user), service: RevisaoService = Depends()):
    return await service.concluir_revisao(revisao_id, revisao, user.ID)

@router.get("/cronograma", response_model=Page[Revisao])
async def get_cronograma(
    user: UserModel = Depends(get_current_user), 
    service: RevisaoService = Depends(),
    page: int = Query(1, ge=1, description="Número da página"),
    size: int = Query(10, ge=1, le=100, description="Tamanho da página")
):
    return await service.get_cronograma(user.ID, page, size)

@router.put("/{revisao_id}/reagendar", response_model=Revisao)
async def reagendar_revisao(revisao_id: int, nova_data: date, user: UserModel = Depends(get_current_user), service: RevisaoService = Depends()):
    return await service.reagendar_revisao(revisao_id, nova_data, user.ID)

@router.delete("/{revisao_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_revisao(
    revisao_id: int,
    user: UserModel = Depends(get_current_user),
    service: RevisaoService = Depends(),
):
    await service.delete_revisao(revisao_id, user.ID)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
