from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from src.database import get_db
from src.schemas.user import User, UserUpdate, UserDelete
from src.models.user import User as UserModel
from src.security import get_current_user, get_password_hash, verify_password

router = APIRouter(prefix="/usuario", tags=["usuario"])

@router.get("/perfil", response_model=User)
def get_user_profile(user: UserModel = Depends(get_current_user)):
    return user

@router.put("/perfil", response_model=User)
def update_user_profile(user_update: UserUpdate, user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    update_data = user_update.model_dump(exclude_unset=True)
    if "email" in update_data:
        existing_user = db.query(UserModel).filter(UserModel.email == update_data["email"]).first()
        if existing_user and existing_user.ID != user.ID:
            raise HTTPException(status_code=400, detail="Email already registered")

    if "nova_senha" in update_data:
        if not user_update.senha_atual or not verify_password(user_update.senha_atual, user.senha):
            raise HTTPException(status_code=400, detail="Incorrect current password")
        update_data["senha"] = get_password_hash(update_data["nova_senha"])
        del update_data["nova_senha"]
        if "senha_atual" in update_data:
            del update_data["senha_atual"]

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

@router.delete("/conta", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_account(user_delete: UserDelete, user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    if not verify_password(user_delete.senha_confirmacao, user.senha):
        raise HTTPException(status_code=400, detail="Incorrect password")

    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
