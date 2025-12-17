from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from ..database import Base
from .base import TimestampMixin

class Revisao(Base, TimestampMixin):
    __tablename__ = "Revisao"

    ID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tema_id = Column(Integer, ForeignKey("Tema.ID", ondelete="CASCADE"), nullable=False)
    data_prevista = Column(Date, nullable=False)
    data_realizada = Column(DateTime, nullable=True)
    tempo_dedicado = Column(Integer, nullable=True)
    status = Column(String(20), default='PENDENTE')
    descricao = Column(Text, nullable=True)

    tema = relationship("Tema", back_populates="revisoes")
