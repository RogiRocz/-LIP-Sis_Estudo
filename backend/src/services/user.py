from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.repositories.user import UserRepository
from src.schemas.user import UserCreate, UserUpdate, UserDelete
from src.models.user import User as UserModel
from src.security import get_password_hash, verify_password

class UserService:
    def __init__(self, db: Session = Depends(get_db)):
        self.repo = UserRepository(db)

    def create_user(self, user: UserCreate) -> UserModel:
        if user.senha != user.confirmar_senha:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Passwords do not match"
            )
        existing_user = self.repo.get_user_by_email(user.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        hashed_password = get_password_hash(user.senha)
        return self.repo.create_user(user, hashed_password)

    def update_user_profile(self, user_update: UserUpdate, current_user: UserModel) -> UserModel:
        update_data = user_update.model_dump(exclude_unset=True)

        if "email" in update_data:
            existing_user = self.repo.get_user_by_email(update_data["email"])
            if existing_user and existing_user.ID != current_user.ID:
                raise HTTPException(status_code=400, detail="Email already registered")

        if "nova_senha" in update_data:
            if not user_update.senha_atual or not verify_password(user_update.senha_atual, current_user.senha):
                raise HTTPException(status_code=400, detail="Incorrect current password")
            update_data["senha"] = get_password_hash(update_data["nova_senha"])
            del update_data["nova_senha"]
            if "senha_atual" in update_data:
                del update_data["senha_atual"]

        for key, value in update_data.items():
            setattr(current_user, key, value)

        return self.repo.update_user(current_user)

    def delete_user_account(self, user_delete: UserDelete, current_user: UserModel):
        if not verify_password(user_delete.senha_confirmacao, current_user.senha):
            raise HTTPException(status_code=400, detail="Incorrect password")

        self.repo.delete_user(current_user)
