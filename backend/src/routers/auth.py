from fastapi import APIRouter, Depends
from schemas.user import UserCreate, UserLogin
from schemas.auth import Token
from services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token)
async def register(user: UserCreate, service: AuthService = Depends()):
    return await service.register(user)

@router.post("/login", response_model=Token)
async def login(user: UserLogin, service: AuthService = Depends()):
    return await service.login(user)
