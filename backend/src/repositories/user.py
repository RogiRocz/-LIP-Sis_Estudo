from sqlalchemy.orm import Session
from src.models.user import User as UserModel
from src.schemas.user import UserCreate

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> UserModel | None:
        return self.db.query(UserModel).filter(UserModel.email == email).first()

    def create_user(self, user: UserCreate, hashed_password: str) -> UserModel:
        db_user = UserModel(
            email=user.email,
            senha=hashed_password,
            nome=user.nome
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_user(self, user: UserModel) -> UserModel:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user: UserModel):
        self.db.delete(user)
        self.db.commit()
