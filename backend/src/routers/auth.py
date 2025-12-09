from fastapi import APIRouter, Depends
from src.schemas.user import UserCreate, UserLogin
from src.schemas.auth import Token
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token)
def register(user: UserCreate, service: AuthService = Depends()):
    return service.register(user)

@router.post("/login", response_model=Token)
def login(user: UserLogin, service: AuthService = Depends()):
    return service.login(user)
