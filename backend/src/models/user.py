from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base
from .base import TimestampMixin

class User(Base, TimestampMixin):
    __tablename__ = 'Usuario'
    ID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(100), index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    senha = Column(String(100), nullable=False)
    ui_theme = Column(String(10), default='light')
    intervalo_revisoes = Column(String(50), default='1,7,14')
        
    disciplinas = relationship("Disciplina", back_populates="usuario")
