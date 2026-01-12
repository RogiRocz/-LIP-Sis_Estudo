from fastapi import APIRouter, Depends
from ..schemas.seed import SeedRequest
from ..models.user import User as UserModel
from ..security import get_current_user
from ..services.seed import SeedService

router = APIRouter(prefix="/seed", tags=["seed"])


@router.post("/mock-data")
async def generate_mock_data(
    seed_request: SeedRequest,
    user: UserModel = Depends(get_current_user),
    service: SeedService = Depends(),
):
    """
    Gera dados mockados para o usuário autenticado.
    Os dados são adicionados aos existentes, não substituem.
    """
    return await service.generate_mock_data_for_user(
        usuario_id=user.ID,
        intervalo_revisoes=user.intervalo_revisoes,
        seed_request=seed_request,
    )
