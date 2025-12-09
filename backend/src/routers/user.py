from fastapi import APIRouter, Depends, status, Response
from src.schemas.user import User, UserUpdate, UserDelete
from src.models.user import User as UserModel
from src.security import get_current_user
from src.services.user import UserService

router = APIRouter(prefix="/usuario", tags=["usuario"])

@router.get("/perfil", response_model=User)
def get_user_profile(user: UserModel = Depends(get_current_user)):
    return user

@router.put("/perfil", response_model=User)
def update_user_profile(user_update: UserUpdate, user: UserModel = Depends(get_current_user), service: UserService = Depends()):
    return service.update_user_profile(user_update, user)

@router.delete("/conta", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_account(user_delete: UserDelete, user: UserModel = Depends(get_current_user), service: UserService = Depends()):
    service.delete_user_account(user_delete, user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
