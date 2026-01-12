from pydantic import BaseModel
from typing import Optional

class SeedRequest(BaseModel):
    num_disciplinas: Optional[int] = 7
    num_temas_por_disciplina: Optional[int] = 5
    dias_retroceder: Optional[int] = 365