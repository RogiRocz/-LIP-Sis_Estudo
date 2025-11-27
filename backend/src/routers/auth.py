from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.schemas.user import UserCreate, UserLogin, User
from src.schemas.auth import Token
from src.models.user import User as UserModel
from src.security import get_password_hash, verify_password, create_access_token
from src.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if user.senha != user.confirmar_senha:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_password = get_password_hash(user.senha)
    db_user = UserModel(
        email=user.email,
        senha=hashed_password,
        nome=user.nome,
        tema=settings.DEFAULT_THEME,
        intervalo_revisoes=settings.DEFAULT_REVISION_INTERVAL
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    access_token = create_access_token(data={"sub": db_user.email})
    user_schema = User.model_validate(db_user)
    return {"access_token": access_token, "token_type": "bearer", "user": user_schema}

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if not db_user or not verify_password(user.senha, db_user.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": db_user.email})
    user_schema = User.model_validate(db_user)
    return {"access_token": access_token, "token_type": "bearer", "user": user_schema}
