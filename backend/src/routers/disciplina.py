from fastapi import APIRouter, Depends, status, Response
from src.schemas.disciplina import Disciplina, DisciplinaCreate, DisciplinaUpdate
from src.models.user import User as UserModel
from src.security import get_current_user
from src.services.disciplina import DisciplinaService
from typing import List

router = APIRouter(prefix="/disciplinas", tags=["disciplinas"])

@router.post("/", response_model=Disciplina)
def create_disciplina(disciplina: DisciplinaCreate, user: UserModel = Depends(get_current_user), service: DisciplinaService = Depends()):
    return service.create_disciplina(disciplina, user.ID)

@router.get("/", response_model=List[Disciplina])
def get_disciplinas(user: UserModel = Depends(get_current_user), service: DisciplinaService = Depends()):
    return service.get_disciplinas(user.ID)

@router.get("/{disciplina_id}", response_model=Disciplina)
def get_disciplina(disciplina_id: int, user: UserModel = Depends(get_current_user), service: DisciplinaService = Depends()):
    return service.get_disciplina(disciplina_id, user.ID)

@router.put("/{disciplina_id}", response_model=Disciplina)
def update_disciplina(disciplina_id: int, disciplina: DisciplinaUpdate, user: UserModel = Depends(get_current_user), service: DisciplinaService = Depends()):
    return service.update_disciplina(disciplina_id, disciplina, user.ID)

@router.delete("/{disciplina_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_disciplina(disciplina_id: int, user: UserModel = Depends(get_current_user), service: DisciplinaService = Depends()):
    service.delete_disciplina(disciplina_id, user.ID)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
