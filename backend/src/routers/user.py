from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..schemas.user import User, UserUpdate, UserDelete
from ..models.user import User as UserModel
from ..security import get_current_user
from ..services.user import UserService
from ..services.exemplos import ExemplosService

router = APIRouter(prefix="/usuario", tags=["usuario"])

@router.get("/perfil", response_model=User)
async def get_user_profile(user: UserModel = Depends(get_current_user)):
    return user

@router.put("/perfil", response_model=User)
async def update_user_profile(user_update: UserUpdate, user: UserModel = Depends(get_current_user), service: UserService = Depends()):
    return await service.update_user_profile(user_update, user)

@router.delete("/conta", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_account(user_delete: UserDelete, user: UserModel = Depends(get_current_user), service: UserService = Depends()):
    await service.delete_user_account(user_delete, user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/dados-exemplo", status_code=status.HTTP_201_CREATED)
async def create_example_data(
    user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    service: ExemplosService = Depends()
):
    return await service.criar_dados_exemplo(db, user)
