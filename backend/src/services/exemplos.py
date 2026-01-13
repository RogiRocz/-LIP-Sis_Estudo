from sqlalchemy.ext.asyncio import AsyncSession
from ..models.user import User
from ..models.disciplina import Disciplina
from ..models.tema import Tema
from ..models.revisao import Revisao
from datetime import datetime, timedelta


class ExemplosService:
    async def criar_dados_exemplo(self, db: AsyncSession, user: User):

        disciplinas_exemplo = [
            {
                "nome": "Matemática",
                "cor": "#FF5733",
                "descricao": "Estudo de matemática básica e avançada.",
            },
            {
                "nome": "História",
                "cor": "#33FF57",
                "descricao": "História do Brasil e do mundo.",
            },
        ]

        temas_exemplo = {
            "Matemática": [
                {
                    "nome": "Álgebra Linear",
                    "descricao": "Estudo de vetores, matrizes e espaços lineares.",
                },
                {
                    "nome": "Cálculo Diferencial",
                    "descricao": "Estudo de limites, derivadas e suas aplicações.",
                },
            ],
            "História": [
                {
                    "nome": "Brasil Colônia",
                    "descricao": "Período da história do Brasil entre 1500 e 1822.",
                },
                {
                    "nome": "Revolução Francesa",
                    "descricao": "Período de intensa agitação política e social na França.",
                },
            ],
        }

        revisoes_exemplo = {
            "Álgebra Linear": [
                {"data_revisao": datetime.now() - timedelta(days=2)},
                {"data_revisao": datetime.now() + timedelta(days=5)},
            ],
            "Cálculo Diferencial": [
                {"data_revisao": datetime.now() - timedelta(days=1)},
            ],
            "Brasil Colônia": [
                {"data_revisao": datetime.now() - timedelta(days=3)},
                {"data_revisao": datetime.now() + timedelta(days=4)},
            ],
        }

        for disc_data in disciplinas_exemplo:
            disciplina = Disciplina(**disc_data, user_id=user.id)
            db.add(disciplina)
            await db.flush()

            if disc_data["nome"] in temas_exemplo:
                for tema_data in temas_exemplo[disc_data["nome"]]:
                    tema = Tema(
                        **tema_data, disciplina_id=disciplina.id, user_id=user.id
                    )
                    db.add(tema)
                    await db.flush()

                    if tema_data["nome"] in revisoes_exemplo:
                        for rev_data in revisoes_exemplo[tema_data["nome"]]:
                            revisao = Revisao(
                                **rev_data,
                                tema_id=tema.id,
                                user_id=user.id,
                                concluida=True
                            )
                            db.add(revisao)

        await db.commit()
