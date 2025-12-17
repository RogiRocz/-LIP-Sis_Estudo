from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.user import User as UserModel
from ..schemas.user import UserCreate

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str) -> UserModel | None:
        query = select(UserModel).where(UserModel.email == email)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def create_user(self, user: UserCreate, hashed_password: str) -> UserModel:
        db_user = UserModel(
            email=user.email,
            senha=hashed_password,
            nome=user.nome
        )
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def update_user(self, user: UserModel) -> UserModel:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete_user(self, user: UserModel):
        await self.db.delete(user)
        await self.db.commit()
