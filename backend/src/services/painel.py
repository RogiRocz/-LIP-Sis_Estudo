from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, timedelta
from .. import models
from ..schemas import painel as painel_schema


class PainelService:
    def __init__(self, db: Session):
        self.db = db

    def get_estatisticas_gerais(self, id_usuario: int) -> painel_schema.EstatisticasGerais:
        total_disciplinas = self.db.query(func.count(models.Disciplina.id_disciplina)).filter(models.Disciplina.id_usuario == id_usuario).scalar() or 0
        total_temas = self.db.query(func.count(models.Tema.id_tema)).join(models.Disciplina).filter(models.Disciplina.id_usuario == id_usuario).scalar() or 0
        total_revisoes = self.db.query(func.count(models.Revisao.id_revisao)).join(models.Tema).join(models.Disciplina).filter(models.Disciplina.id_usuario == id_usuario).scalar() or 0
        revisoes_hoje = self.db.query(func.count(models.Revisao.id_revisao)).join(models.Tema).join(models.Disciplina).filter(
            models.Disciplina.id_usuario == id_usuario,
            models.Revisao.data_revisao == date.today()
        ).scalar() or 0

        return painel_schema.EstatisticasGerais(
            total_disciplinas=total_disciplinas,
            total_temas=total_temas,
            total_revisoes=total_revisoes,
            revisoes_hoje=revisoes_hoje
        )

    def get_evolucao_semanal(self, id_usuario: int) -> list[painel_schema.EvolucaoSemanal]:
        today = date.today()
        seven_days_ago = today - timedelta(days=6)

        revisoes = self.db.query(
            models.Revisao.data_revisao,
            func.count(models.Revisao.id_revisao)
        ).join(models.Tema).join(models.Disciplina).filter(
            models.Disciplina.id_usuario == id_usuario,
            models.Revisao.data_revisao >= seven_days_ago,
            models.Revisao.data_revisao <= today
        ).group_by(models.Revisao.data_revisao).all()

        revisoes_dict = {data: count for data, count in revisoes}

        evolucao = []
        for i in range(7):
            current_date = seven_days_ago + timedelta(days=i)
            evolucao.append(painel_schema.EvolucaoSemanal(
                data=current_date,
                revisoes_realizadas=revisoes_dict.get(current_date, 0)
            ))

        return evolucao

    def get_revisoes_do_dia(self, id_usuario: int) -> list[painel_schema.RevisaoDoDia]:
        revisoes = self.db.query(
            models.Revisao.id_revisao,
            models.Tema.titulo,
            models.Disciplina.nome
        ).join(models.Tema).join(models.Disciplina).filter(
            models.Disciplina.id_usuario == id_usuario,
            models.Revisao.data_revisao == date.today()
        ).all()

        return [painel_schema.RevisaoDoDia(
            id_revisao=id_revisao,
            titulo_tema=titulo_tema,
            nome_disciplina=nome_disciplina
        ) for id_revisao, titulo_tema, nome_disciplina in revisoes]

    def get_painel_data(self, id_usuario: int) -> painel_schema.PainelData:
        estatisticas = self.get_estatisticas_gerais(id_usuario)
        evolucao = self.get_evolucao_semanal(id_usuario)
        revisoes = self.get_revisoes_do_dia(id_usuario)

        return painel_schema.PainelData(
            estatisticas=estatisticas,
            evolucao_semanal=evolucao,
            revisoes_do_dia=revisoes
        )
