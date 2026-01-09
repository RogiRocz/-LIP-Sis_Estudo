from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from ..security import get_current_user
from ..schemas import painel as painel_schema
from ..services.painel import PainelService

router = APIRouter(prefix="/painel", tags=["Painel"])


@router.get("/estatisticas", response_model=painel_schema.PainelData)
def get_painel_data(
    db: Session = Depends(get_db),
    user: models.user.User = Depends(get_current_user),
):
    painel_service = PainelService(db)
    return painel_service.get_painel_data(user.id_usuario)
