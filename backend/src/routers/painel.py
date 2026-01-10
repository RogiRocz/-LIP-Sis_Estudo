from fastapi import APIRouter, Depends
from ..models.user import User as UserModel
from ..security import get_current_user
from ..schemas import painel as painel_schema
from ..services.painel import PainelService
from typing import List

router = APIRouter(prefix="/painel", tags=["Painel"])


@router.get("/estatisticas", response_model=painel_schema.EstatisticasGerais)
async def get_estatisticas(
    user: UserModel = Depends(get_current_user),
    service: PainelService = Depends(),
):
    return await service.get_estatisticas_gerais(user.ID)


@router.get("/evolucao-semanal", response_model=List[painel_schema.EvolucaoSemanal])
async def get_evolucao_semanal(
    user: UserModel = Depends(get_current_user),
    service: PainelService = Depends(),
):
    return await service.get_evolucao_semanal(user.ID)


@router.get("/revisoes-do-dia", response_model=List[painel_schema.RevisaoDoDia])
async def get_revisoes_do_dia(
    user: UserModel = Depends(get_current_user),
    service: PainelService = Depends(),
):
    return await service.get_revisoes_do_dia(user.ID)
