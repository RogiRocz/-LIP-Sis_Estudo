from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..repositories.user import UserRepository
from ..schemas.user import UserCreate, UserUpdate, UserDelete
from ..models.user import User as UserModel
from ..security import get_password_hash, verify_password

class UserService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.repo = UserRepository(db)

    async def create_user(self, user: UserCreate) -> UserModel:
        if user.senha != user.confirmar_senha:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="As senhas não conferem"
            )
        existing_user = await self.repo.get_user_by_email(user.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já registrado"
            )
        hashed_password = get_password_hash(user.senha)
        return await self.repo.create_user(user, hashed_password)

    async def update_user_profile(self, user_update: UserUpdate, current_user: UserModel) -> UserModel:
        update_data = user_update.model_dump(exclude_unset=True)

        if "email" in update_data:
            existing_user = await self.repo.get_user_by_email(update_data["email"])
            if existing_user and existing_user.ID != current_user.ID:
                raise HTTPException(status_code=400, detail="Email já registrado")

        if "nova_senha" in update_data:
            if not user_update.senha_atual or not verify_password(user_update.senha_atual, current_user.senha):
                raise HTTPException(status_code=400, detail="Senha atual incorreta")
            update_data["senha"] = get_password_hash(update_data["nova_senha"])
            del update_data["nova_senha"]
            if "senha_atual" in update_data:
                del update_data["senha_atual"]

        for key, value in update_data.items():
            setattr(current_user, key, value)

        return await self.repo.update_user(current_user)

    async def delete_user_account(self, user_delete: UserDelete, current_user: UserModel):
        if not verify_password(user_delete.senha_confirmacao, current_user.senha):
            raise HTTPException(status_code=400, detail="Senha incorreta")

        await self.repo.delete_user(current_user)
