from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import date, timedelta, datetime
import random
from faker import Faker

from ..models.disciplina import Disciplina
from ..models.tema import Tema
from ..models.revisao import Revisao

fake = Faker("pt_BR")


class SeedRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_disciplina_count(self, usuario_id: int) -> int:
        """Conta quantas disciplinas o usuário já tem"""
        query = select(Disciplina).where(Disciplina.usuario_id == usuario_id)
        result = await self.db.execute(query)
        return len(result.scalars().all())

    async def generate_mock_data(
        self,
        usuario_id: int,
        intervalo_revisoes: list[int],
        num_disciplinas: int = 7,
        num_temas_por_disciplina: int = 5,
        dias_retroceder: int = 365,
    ):
        """
        Gera dados mockados para um usuário específico sem sobrescrever dados existentes
        """

        todas_disciplinas = {
            "Cálculo I": "Estudo de limites, derivadas e integrais.",
            "Estrutura de Dados": "Implementação de estruturas como grafos e árvores.",
            "Inteligência Artificial": "Fundamentos de IA e machine learning.",
            "História do Brasil": "Do descobrimento à república.",
            "Literatura Clássica": "Análise de obras greco-romanas.",
            "Química Orgânica": "Estudo dos compostos de carbono.",
            "Física Moderna": "Princípios de relatividade e mecânica quântica.",
            "Biologia Molecular": "Estudo das moléculas biológicas e processos celulares.",
            "Geografia Humana": "Relação entre sociedade e espaço geográfico.",
            "Filosofia Antiga": "Pensamento dos filósofos gregos e romanos.",
            "Estatística": "Coleta, análise e interpretação de dados.",
            "Programação Web": "Desenvolvimento de aplicações para internet.",
            "Economia": "Produção, distribuição e consumo de bens e serviços.",
            "Psicologia Cognitiva": "Processos mentais como pensamento e memória.",
            "Direito Constitucional": "Estudo da constituição e direitos fundamentais.",
        }

        temas_base = {
            "Cálculo I": ["Limites", "Derivadas", "Integrais", "Séries", "EDOs"],
            "Estrutura de Dados": [
                "Grafos",
                "Árvores",
                "Hash Tables",
                "Filas",
                "Pilhas",
            ],
            "Inteligência Artificial": [
                "Redes Neurais",
                "ML",
                "NLP",
                "Visão Computacional",
            ],
            "História do Brasil": ["Colonial", "Império", "República", "Era Vargas"],
            "Literatura Clássica": ["Épicos Gregos", "Tragédias", "Comédias", "Poesia"],
            "Química Orgânica": ["Hidrocarbonetos", "Funções Orgânicas", "Polímeros"],
            "Física Moderna": ["Relatividade", "Mecânica Quântica", "Física Nuclear"],
        }

        disciplinas_selecionadas = dict(
            random.sample(
                list(todas_disciplinas.items()),
                min(num_disciplinas, len(todas_disciplinas)),
            )
        )

        disciplinas_criadas = []
        for nome, desc in disciplinas_selecionadas.items():
            disciplina = Disciplina(
                nome=nome,
                cor=f"#{random.randint(0, 0xFFFFFF):06x}",
                descricao=desc,
                usuario_id=usuario_id,
            )
            self.db.add(disciplina)
            disciplinas_criadas.append(disciplina)

        await self.db.flush()

        today = date.today()
        temas_criados = 0
        revisoes_criadas = 0

        for disciplina in disciplinas_criadas:

            temas_para_criar = min(num_temas_por_disciplina, 10)

            temas_da_disciplina = temas_base.get(
                disciplina.nome, [f"Tópico {i+1}" for i in range(5)]
            )

            for _ in range(temas_para_criar):

                if temas_da_disciplina:
                    nome_tema_base = random.choice(temas_da_disciplina)
                    descricao_tema = f"Estudo aprofundado sobre {nome_tema_base} na disciplina {disciplina.nome}."
                else:
                    nome_tema_base = fake.catch_phrase()
                    descricao_tema = fake.paragraph(nb_sentences=3)

                data_criacao = today - timedelta(
                    days=random.randint(0, dias_retroceder)
                )

                tema = Tema(
                    nome=f"{nome_tema_base}",
                    descricao=descricao_tema,
                    disciplina_id=disciplina.ID,
                    criado_em=datetime.combine(data_criacao, datetime.min.time()),
                )
                self.db.add(tema)
                await self.db.flush()
                temas_criados += 1

                for dias in intervalo_revisoes:
                    data_prevista = data_criacao + timedelta(days=dias)

                    if data_prevista < today and random.random() < 0.7:
                        status = "REALIZADA"
                        data_realizada = data_prevista + timedelta(
                            days=random.randint(0, 3)
                        )
                        tempo_dedicado = random.choice([15, 30, 45, 60, 90])
                        descricao_revisao = fake.sentence(nb_words=10)
                    else:
                        status = "PENDENTE" if data_prevista >= today else "ATRASADA"
                        data_realizada = None
                        tempo_dedicado = None
                        descricao_revisao = None

                    revisao = Revisao(
                        tema_id=tema.ID,
                        data_prevista=data_prevista,
                        data_realizada=data_realizada,
                        tempo_dedicado=tempo_dedicado,
                        status=status,
                        descricao=descricao_revisao,
                    )
                    self.db.add(revisao)
                    revisoes_criadas += 1

        await self.db.commit()

        return {
            "disciplinas_criadas": len(disciplinas_criadas),
            "temas_criados": temas_criados,
            "revisoes_criadas": revisoes_criadas,
            "mensagem": "Dados mockados gerados com sucesso!",
        }
