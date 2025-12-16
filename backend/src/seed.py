
import asyncio
from datetime import datetime, date, timedelta
from sqlalchemy import text

# Configuration to allow the script to import application modules
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal, engine, Base
from models.user import User
from models.disciplina import Disciplina
from models.tema import Tema
from models.revisao import Revisao
from models.cronograma import Cronograma
from security import get_password_hash
from core.config import settings

async def seed_data():
    # Reset the database
    async with engine.begin() as conn:
        await conn.execute(text("DROP SCHEMA public CASCADE;"))
        await conn.execute(text("CREATE SCHEMA public;"))
        await conn.run_sync(Base.metadata.create_all)

    db = SessionLocal()
    try:
        # --- Create User ---
        hashed_password = get_password_hash("123456")
        user = User(
            nome="Usuário de Teste",
            email="teste@exemplo.com",
            senha=hashed_password,
            tema=settings.DEFAULT_THEME,
            intervalo_revisoes=settings.DEFAULT_REVISION_INTERVAL
        )
        db.add(user)
        await db.flush()  # Flush to get user.ID
        print("Usuário de teste criado.")

        # --- Create Disciplinas ---
        disciplina1 = Disciplina(nome="Matemática", usuario_id=user.ID)
        disciplina2 = Disciplina(nome="História", usuario_id=user.ID)
        db.add_all([disciplina1, disciplina2])
        await db.flush()  # Flush to get discipline IDs
        print("Disciplinas de teste criadas.")

        # --- Create Temas ---
        tema1 = Tema(
            nome="Álgebra",
            data_criacao=date.today(),
            disciplina_id=disciplina1.ID
        )
        db.add(tema1)
        
        tema2 = Tema(
            nome="Revolução Francesa",
            data_criacao=date.today(),
            disciplina_id=disciplina2.ID
        )
        db.add(tema2)
        await db.flush()  # Flush to get tema IDs
        print("Temas de teste criados.")

        # --- Generate Revisões from Tema ---
        def create_revisions_for_tema(tema, revision_intervals):
            intervals = [int(i) for i in revision_intervals.split(',')]
            revisions = []
            for days in intervals:
                revisao_date = tema.data_criacao + timedelta(days=days)
                revisao = Revisao(
                    data_prevista=revisao_date,
                    status="PENDENTE",
                    tema_id=tema.ID
                )
                revisions.append(revisao)
            return revisions

        revisoes_tema1 = create_revisions_for_tema(tema1, user.intervalo_revisoes)
        db.add_all(revisoes_tema1)
        print(f"Revisões para o tema 'Álgebra' criadas.")

        revisoes_tema2 = create_revisions_for_tema(tema2, user.intervalo_revisoes)
        db.add_all(revisoes_tema2)
        print(f"Revisões para o tema 'Revolução Francesa' criadas.")

        await db.commit()  # Commit all changes
        print("\nDados mockados criados com sucesso!")

    finally:
        await db.close()

if __name__ == "__main__":
    asyncio.run(seed_data())
