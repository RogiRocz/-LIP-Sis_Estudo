from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..repositories.seed import SeedRepository
from ..schemas.seed import SeedRequest


class SeedService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.repo = SeedRepository(db)

    async def generate_mock_data_for_user(
        self, usuario_id: int, intervalo_revisoes: list[int], seed_request: SeedRequest
    ):
        """
        Gera dados mockados para um usuário específico
        """

        disciplinas_existentes = await self.repo.get_user_disciplina_count(usuario_id)

        if disciplinas_existentes >= 20:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuário já tem o número máximo de disciplinas (20).",
            )

        disciplinas_a_criar = min(
            seed_request.num_disciplinas, 20 - disciplinas_existentes
        )

        if disciplinas_a_criar <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não é possível criar mais disciplinas. Limite máximo atingido.",
            )

        result = await self.repo.generate_mock_data(
            usuario_id=usuario_id,
            intervalo_revisoes=intervalo_revisoes,
            num_disciplinas=disciplinas_a_criar,
            num_temas_por_disciplina=seed_request.num_temas_por_disciplina,
            dias_retroceder=seed_request.dias_retroceder,
        )

        return result
