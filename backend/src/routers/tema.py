from fastapi import APIRouter, Depends, status, Response
from src.schemas.tema import Tema, TemaCreate, TemaUpdate
from src.models.user import User as UserModel
from src.security import get_current_user
from src.services.tema import TemaService
from typing import List

# Router for nested endpoints under /disciplinas/{disciplina_id}/temas
disciplina_tema_router = APIRouter(prefix="/disciplinas/{disciplina_id}/temas", tags=["temas"])

# Router for top-level /temas endpoints
tema_router = APIRouter(prefix="/temas", tags=["temas"])

@disciplina_tema_router.post("/", response_model=Tema)
def create_tema(disciplina_id: int, tema: TemaCreate, user: UserModel = Depends(get_current_user), service: TemaService = Depends()):
    return service.create_tema_for_disciplina(disciplina_id, tema, user)

@disciplina_tema_router.get("/", response_model=List[Tema])
def get_temas_by_disciplina(disciplina_id: int, user: UserModel = Depends(get_current_user), service: TemaService = Depends()):
    return service.get_temas_by_disciplina(disciplina_id, user.ID)

@tema_router.get("/{tema_id}", response_model=Tema)
def get_tema(tema_id: int, user: UserModel = Depends(get_current_user), service: TemaService = Depends()):
    return service.get_tema(tema_id, user.ID)

@tema_router.put("/{tema_id}", response_model=Tema)
def update_tema(tema_id: int, tema: TemaUpdate, user: UserModel = Depends(get_current_user), service: TemaService = Depends()):
    return service.update_tema(tema_id, tema, user.ID)

@tema_router.delete("/{tema_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tema(tema_id: int, user: UserModel = Depends(get_current_user), service: TemaService = Depends()):
    service.delete_tema(tema_id, user.ID)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
