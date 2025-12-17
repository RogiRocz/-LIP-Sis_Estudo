from fastapi import APIRouter, Depends, status, Response
from ..schemas.tema import Tema, TemaCreate, TemaUpdate
from ..models.user import User as UserModel
from ..security import get_current_user
from ..services.tema import TemaService
from typing import List

# Router for nested endpoints under /disciplinas/{disciplina_id}/temas
disciplina_tema_router = APIRouter(prefix="/disciplinas/{disciplina_id}/temas", tags=["temas"])

# Router for top-level /temas endpoints
tema_router = APIRouter(prefix="/temas", tags=["temas"])

@disciplina_tema_router.post("/", response_model=Tema)
async def create_tema(disciplina_id: int, tema: TemaCreate, user: UserModel = Depends(get_current_user), service: TemaService = Depends()):
    return await service.create_tema_for_disciplina(disciplina_id, tema, user)

@disciplina_tema_router.get("/", response_model=List[Tema])
async def get_temas_by_disciplina(disciplina_id: int, user: UserModel = Depends(get_current_user), service: TemaService = Depends()):
    return await service.get_temas_by_disciplina(disciplina_id, user.ID)

@tema_router.get("/{tema_id}", response_model=Tema)
async def get_tema(tema_id: int, user: UserModel = Depends(get_current_user), service: TemaService = Depends()):
    return await service.get_tema(tema_id, user.ID)

@tema_router.put("/{tema_id}", response_model=Tema)
async def update_tema(tema_id: int, tema: TemaUpdate, user: UserModel = Depends(get_current_user), service: TemaService = Depends()):
    return await service.update_tema(tema_id, tema, user.ID)

@tema_router.delete("/{tema_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tema(tema_id: int, user: UserModel = Depends(get_current_user), service: TemaService = Depends()):
    await service.delete_tema(tema_id, user.ID)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
