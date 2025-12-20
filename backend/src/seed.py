
import asyncio
import random
from datetime import date, timedelta, datetime
from sqlalchemy import text
from faker import Faker

from .database import SessionLocal, engine, Base
from .models.user import User
from .models.disciplina import Disciplina
from .models.tema import Tema
from .models.revisao import Revisao
from .security import get_password_hash
from .core.config import settings

# Initialize Faker for generating random data
fake = Faker('pt_BR')

async def seed_data():
    """
    Resets the database and populates it with realistic mock data for one user
    over the course of the last year.
    """
    print("Iniciando o processo de seeding do banco de dados...")

    # Reset the database
    async with engine.begin() as conn:
        print("Resetando o banco de dados (DROP/CREATE SCHEMA)...")
        await conn.execute(text("DROP SCHEMA public CASCADE;"))
        await conn.execute(text("CREATE SCHEMA public;"))
        await conn.run_sync(Base.metadata.create_all)

    db = SessionLocal()
    try:
        # --- 1. Create User ---
        print("Criando usuário de teste...")
        hashed_password = get_password_hash("123456")
        user = User(
            nome="Usuário de Teste",
            email="teste@exemplo.com",
            senha=hashed_password,
            ui_theme=settings.DEFAULT_THEME,
            intervalo_revisoes=settings.DEFAULT_REVISION_INTERVAL
        )
        db.add(user)
        await db.flush()
        print(f"Usuário '{user.email}' criado com ID: {user.ID}.")

        # --- 2. Create Disciplinas ---
        print("Criando um conjunto de disciplinas...")
        disciplinas_nomes = [
            "Cálculo Diferencial e Integral", "Estrutura de Dados Avançada", "Inteligência Artificial",
            "História do Brasil Colonial", "Literatura Clássica", "Química Orgânica", "Física Quântica"
        ]
        disciplinas = []
        for nome in disciplinas_nomes:
            disciplina = Disciplina(
                nome=nome,
                cor=fake.hex_color(),
                usuario_id=user.ID
            )
            disciplinas.append(disciplina)
        db.add_all(disciplinas)
        await db.flush()
        print(f"{len(disciplinas)} disciplinas criadas.")

        # --- 3. Simulate a Year of Study ---
        print("Simulando um ano de estudos e revisões. Isso pode levar um momento...")
        today = date.today()
        start_date = today - timedelta(days=365)
        current_date = start_date
        
        revision_intervals = [int(i) for i in user.intervalo_revisoes.split(',')]

        while current_date <= today:
            # Probabilistic creation of themes to simulate real usage
            if random.random() < 0.3:  # 30% chance of creating a new theme on any given day
                disciplina_aleatoria = random.choice(disciplinas)

                novo_tema = Tema(
                    nome=fake.sentence(nb_words=3),
                    descricao=fake.paragraph(nb_sentences=2),
                    data_criacao=current_date,
                    disciplina_id=disciplina_aleatoria.ID
                )
                db.add(novo_tema)
                await db.flush()

                # --- 4. Generate Revisions for the New Theme ---
                for days in revision_intervals:
                    data_prevista_revisao = novo_tema.data_criacao + timedelta(days=days)
                    revisao = Revisao(
                        data_prevista=data_prevista_revisao,
                        status="PENDENTE",
                        tema_id=novo_tema.ID
                    )

                    # If the revision was in the past, decide if it was completed or missed
                    if data_prevista_revisao < today:
                        if random.random() < 0.7:  # 70% chance of having completed a past revision
                            revisao.status = "REALIZADA"
                            revisao.data_realizada = data_prevista_revisao + timedelta(days=random.randint(0, 2))
                            revisao.tempo_minutos = random.randint(20, 120) # Study time in minutes
                        else:
                            # If not completed, it's implicitly "ATRASADA" as its status is PENDENTE and date is in the past
                            pass

                    db.add(revisao)

            current_date += timedelta(days=1)

        print("Simulação concluída. Committing all changes to the database...")
        await db.commit()
        print("\nDados mockados avançados criados com sucesso!")

    except Exception as e:
        await db.rollback()
        print(f"Ocorreu um erro: {e}")
    finally:
        await db.close()
        print("Sessão do banco de dados fechada.")

async def main():
    await seed_data()

if __name__ == "__main__":
    asyncio.run(main())
