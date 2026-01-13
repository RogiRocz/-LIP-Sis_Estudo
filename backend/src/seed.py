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

fake = Faker("pt_BR")


async def seed_data():
    """
    Populates the database with realistic, thematically consistent mock data.
    """
    print("Iniciando o processo de seeding do banco de dados...")

    async with engine.begin() as conn:
        print("Limpando dados existentes (TRUNCATE)...")
        table_names = [
            table.name
            for table in Base.metadata.sorted_tables
            if table.name != "alembic_version"
        ]
        if table_names:
            quoted_names = [f'public."{name}"' for name in table_names]
            await conn.execute(
                text(
                    f"TRUNCATE TABLE {', '.join(quoted_names)} RESTART IDENTITY CASCADE;"
                )
            )
            print(f"Tabelas limpas: {', '.join(table_names)}.")

    db = SessionLocal()
    try:

        print("Criando usuário de teste...")
        user = User(
            nome="Usuário de Teste",
            email="teste@exemplo.com",
            senha=get_password_hash("123456"),
            ui_theme=settings.DEFAULT_THEME,
            intervalo_revisoes=settings.DEFAULT_REVISION_INTERVAL,
        )
        db.add(user)
        await db.flush()

        res = await db.execute(
            text(
                """
            SELECT id FROM auth.users WHERE email = :email
        """
            ),
            {"email": user.email},
        )
        supabase_uuid = res.scalar()

        if supabase_uuid:
            user.supabase_id = supabase_uuid
            print(f"Vínculo com Supabase UUID {supabase_uuid} estabelecido.")
        else:
            print(
                "AVISO: Usuário 'teste@exemplo.com' não encontrado no Auth do Supabase. O RLS não funcionará."
            )

        disciplinas_data = {
            "Cálculo I": "Estudo de limites, derivadas e integrais.",
            "Estrutura de Dados": "Implementação de estruturas como grafos e árvores.",
            "Inteligência Artificial": "Fundamentos de IA e machine learning.",
            "História do Brasil": "Do descobrimento à república.",
            "Literatura Clássica": "Análise de obras greco-romanas.",
            "Química Orgânica": "Estudo dos compostos de carbono.",
            "Física Moderna": "Princípios de relatividade e mecânica quântica.",
        }
        temas_base = {
            "Cálculo I": [
                "Limites",
                "Derivadas",
                "Integrais",
                "Teorema Fundamental do Cálculo",
            ],
            "Estrutura de Dados": [
                "Grafos",
                "Árvores AVL",
                "Hashing",
                "Algoritmo de Dijkstra",
            ],
            "Inteligência Artificial": [
                "Redes Neurais",
                "Algoritmos Genéticos",
                "Modelos de Markov",
                "Deep Learning",
            ],
            "História do Brasil": [
                "Capitanias Hereditárias",
                "Ciclo do Ouro",
                "Inconfidência Mineira",
                "Independência",
            ],
            "Literatura Clássica": [
                "A Odisseia",
                "Édipo Rei",
                "As Metamorfoses",
                "Eneida",
            ],
            "Química Orgânica": [
                "Alcanos e Alcenos",
                "Reações de Substituição",
                "Isomeria Óptica",
                "Espectroscopia",
            ],
            "Física Moderna": [
                "Relatividade Especial",
                "Efeito Fotoelétrico",
                "Equação de Schrödinger",
                "Dualidade Onda-Partícula",
            ],
        }
        descricoes_temas = {
            "Limites": "Estudo do comportamento de funções próximo a um ponto.",
            "Derivadas": "Taxa de variação instantânea e inclinação de curvas.",
            "Integrais": "Cálculo de áreas sob curvas e antiderivação.",
            "Grafos": "Estruturas de dados com vértices e arestas.",
            "Redes Neurais": "Modelos computacionais inspirados no cérebro humano.",
            "Ciclo do Ouro": "Período de intensa mineração de ouro no Brasil colonial.",
            "A Odisseia": "Poema épico sobre o retorno de Odisseu a Ítaca.",
            "Relatividade Especial": "Teoria de Einstein sobre espaço, tempo e gravidade.",
        }

        print("Criando disciplinas...")
        disciplinas = []
        for nome, desc in disciplinas_data.items():
            disciplinas.append(
                Disciplina(
                    nome=nome, cor=fake.hex_color(), descricao=desc, usuario_id=user.ID
                )
            )
        db.add_all(disciplinas)
        await db.flush()

        print("Simulando um ano de estudos com dados tematicamente consistentes...")
        today = date.today()
        for _ in range(150):
            current_date = today - timedelta(days=random.randint(0, 365))
            disciplina_aleatoria = random.choice(disciplinas)

            if disciplina_aleatoria.nome in temas_base:
                nome_tema_base = random.choice(temas_base[disciplina_aleatoria.nome])
                descricao_especifica = descricoes_temas.get(
                    nome_tema_base, f"Estudo aprofundado sobre {nome_tema_base}."
                )

                novo_tema = Tema(
                    nome=f"{nome_tema_base}: {fake.bs()}",
                    descricao=descricao_especifica,
                    disciplina_id=disciplina_aleatoria.ID,
                )

                novo_tema.criado_em = datetime.combine(
                    current_date, datetime.min.time()
                )
                db.add(novo_tema)
                await db.flush()

                revision_intervals = [
                    int(i) for i in user.intervalo_revisoes.split(",")
                ]
                for days in revision_intervals:
                    data_prevista_revisao = current_date + timedelta(days=days)
                    revisao = Revisao(
                        data_prevista=data_prevista_revisao,
                        status="PENDENTE",
                        tema_id=novo_tema.ID,
                    )

                    if data_prevista_revisao < today and random.random() < 0.75:
                        revisao.status = "REALIZADA"
                        revisao.data_realizada = data_prevista_revisao + timedelta(
                            days=random.randint(0, 3)
                        )
                        revisao.tempo_dedicado = random.choice([15, 30, 45, 60, 90])
                        revisao.descricao = f"Revisão focada em {fake.catch_phrase()}. Pontos de dificuldade: {fake.sentence(nb_words=4)}."

                    db.add(revisao)

        print("Simulação concluída. Salvando dados no banco...")
        await db.commit()
        print(
            "\nSeed concluído com sucesso! Dados realistas e temáticos foram criados."
        )

    except Exception as e:
        await db.rollback()
        print(f"Ocorreu um erro durante o seeding: {e}")
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(seed_data())
