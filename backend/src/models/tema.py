from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base
from .base import TimestampMixin

class Tema(Base, TimestampMixin):
    __tablename__ = "Tema"

    ID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text)
    disciplina_id = Column(Integer, ForeignKey("Disciplina.ID", ondelete="CASCADE"), nullable=False)

    disciplina = relationship("Disciplina", back_populates="temas")
    revisoes = relationship("Revisao", back_populates="tema")
