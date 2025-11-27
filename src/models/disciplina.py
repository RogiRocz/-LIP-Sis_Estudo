from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from src.database import Base

class Disciplina(Base):
    __tablename__ = "Disciplina"

    ID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    cor = Column(String(7))
    descricao = Column(Text)
    usuario_id = Column(Integer, ForeignKey("Usuario.ID", ondelete="CASCADE"), nullable=False)
    data_criacao = Column(DateTime, default=func.now())

    usuario = relationship("User", back_populates="disciplinas")
    temas = relationship("Tema", back_populates="disciplina")
    cronogramas = relationship("Cronograma", back_populates="disciplina")
