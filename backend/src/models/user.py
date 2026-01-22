from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base
from .base import TimestampMixin
from sqlalchemy.dialects.postgresql import UUID, ARRAY


class User(Base, TimestampMixin):
    __tablename__ = "Usuario"
    ID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(100), index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    senha = Column(String(100), nullable=False)
    ui_theme = Column(String(10), default='light')
    intervalo_revisoes = Column(ARRAY(Integer), default=[1, 7, 14])
    supabase_id = Column(UUID(as_uuid=True), unique=True, nullable=True)
        
    disciplinas = relationship("Disciplina", back_populates="usuario", cascade="all, delete-orphan")
