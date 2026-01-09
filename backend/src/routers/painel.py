from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..models.user import User as UserModel
from ..security import get_current_user
from ..services.painel import PainelService
from ..schemas.painel import Estatisticas, EvolucaoSemanal, RevisoesDoDia

router = APIRouter(prefix="/painel", tags=["painel"])

@router.get("/estatisticas", response_model=Estatisticas)
async def get_estatisticas(
    user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    service: PainelService = Depends()
):
    return await service.get_estatisticas(db, user)

@router.get("/evolucao-semanal", response_model=EvolucaoSemanal)
async def get_evolucao_semanal(
    user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    service: PainelService = Depends()
):
    return await service.get_evolucao_semanal(db, user)

@router.get("/revisoes-do-dia", response_model=RevisoesDoDia)
async def get_revisoes_do_dia(
    user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    service: PainelService = Depends()
):
    return await service.get_revisoes_do_dia(db, user)
