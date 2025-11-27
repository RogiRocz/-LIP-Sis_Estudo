from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from src.database import Base

class User(Base):
    __tablename__ = "Usuario"

    ID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    senha = Column(String(255), nullable=False)
    tema = Column(String(20), default='claro')
    nome = Column(String(100), nullable=True)
    intervalo_revisoes = Column(String(50), nullable=False, default='1,7,14')
    data_cadastro = Column(DateTime, default=func.now())

    disciplinas = relationship("Disciplina", back_populates="usuario")
    cronogramas = relationship("Cronograma", back_populates="usuario")
