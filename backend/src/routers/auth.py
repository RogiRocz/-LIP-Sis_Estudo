from fastapi import APIRouter, Depends, Response, status, HTTPException
from ..schemas.user import UserCreate, UserLogin, User
from ..schemas.auth import Token, RefreshTokenResponse, RefreshTokenRequest, TokenLogout
from ..services.auth import AuthService
from ..security import get_current_user
from ..core.supabase_client import supabase


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token)
async def register(user: UserCreate, service: AuthService = Depends()):
    return await service.register(user)


@router.post("/login", response_model=Token)
async def login(user: UserLogin, service: AuthService = Depends()):
    return await service.login(user)


@router.post("/refresh", response_model=RefreshTokenResponse)
async def refresh_token(refresh_token: RefreshTokenRequest, service: AuthService = Depends()):
    return await service.refresh(refresh_token.refresh_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(token: TokenLogout, service: AuthService = Depends()):
    try:
        await service.logout(token.token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
