import random
from datetime import date, timedelta, datetime
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.user import User
from ..models.disciplina import Disciplina
from ..models.tema import Tema
from ..models.revisao import Revisao

fake = Faker("pt_BR")

class ExemplosService:
    async def criar_dados_exemplo(self, db: AsyncSession, user: User):
        """
        Populates the user's account with additive, thematically consistent mock data.
        This operation is non-destructive and will add new data alongside existing data.
        """
        # Base de conhecimento para os dados de exemplo
        disciplinas_data = {
            "Técnicas de Estudo": "Como aprender de forma mais eficiente.",
            "Produtividade Pessoal": "Organização e gestão de tempo.",
            "Desenvolvimento Web": "Fundamentos de HTML, CSS e JavaScript.",
        }
        temas_base = {
            "Técnicas de Estudo": [
                "Método Pomodoro",
                "Repetição Espaçada",
                "Mapas Mentais",
            ],
            "Produtividade Pessoal": [
                "Matriz de Eisenhower",
                "GTD (Getting Things Done)",
                "Técnica dos 2 Minutos",
            ],
            "Desenvolvimento Web": [
                "Estrutura HTML5",
                "Seletores CSS",
                "Manipulação do DOM com JS",
            ],
        }

        # --- Criar Disciplinas ---
        disciplinas = []
        for nome, desc in disciplinas_data.items():
            disciplina = Disciplina(
                nome=f"{nome} (Exemplo)",
                cor=fake.hex_color(),
                descricao=desc,
                usuario_id=user.ID
            )
            disciplinas.append(disciplina)

        db.add_all(disciplinas)
        await db.flush()

        # --- Criar Temas e Revisões ---
        today = date.today()
        for disciplina_obj in disciplinas:
            if disciplina_obj.nome.replace(" (Exemplo)", "") in temas_base:
                nome_disciplina_base = disciplina_obj.nome.replace(" (Exemplo)", "")
                for nome_tema in temas_base[nome_disciplina_base]:
                    current_date = today - timedelta(days=random.randint(5, 60))

                    novo_tema = Tema(
                        nome=nome_tema,
                        descricao=f"Estudo sobre {nome_tema}.",
                        disciplina_id=disciplina_obj.ID,
                        criado_em=datetime.combine(current_date, datetime.min.time())
                    )
                    db.add(novo_tema)
                    await db.flush()

                    # --- Gerar Revisões para o Tema ---
                    revision_intervals = [int(i) for i in user.intervalo_revisoes.split(",")]
                    for days in revision_intervals:
                        data_prevista_revisao = current_date + timedelta(days=days)
                        revisao = Revisao(
                            data_prevista=data_prevista_revisao,
                            status="PENDENTE",
                            tema_id=novo_tema.ID,
                        )
                        db.add(revisao)

        await db.commit()
        return {"message": "Dados de exemplo adicionados com sucesso."}
