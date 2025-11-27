from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from src.database import Base

class Tema(Base):
    __tablename__ = "Tema"

    ID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text)
    disciplina_id = Column(Integer, ForeignKey("Disciplina.ID", ondelete="CASCADE"), nullable=False)
    data_criacao = Column(DateTime, default=func.now())

    disciplina = relationship("Disciplina", back_populates="temas")
    revisoes = relationship("Revisao", back_populates="tema")
