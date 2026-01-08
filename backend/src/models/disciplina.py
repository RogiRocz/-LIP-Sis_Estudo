from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base
from .base import TimestampMixin

class Disciplina(Base, TimestampMixin):
    __tablename__ = "Disciplina"

    ID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    cor = Column(String(7))
    descricao = Column(Text)
    usuario_id = Column(Integer, ForeignKey("Usuario.ID", ondelete="CASCADE"), nullable=False)

    usuario = relationship("User", back_populates="disciplinas")
    temas = relationship("Tema", back_populates="disciplina", cascade="all, delete-orphan")
