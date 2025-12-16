from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Date, func
from sqlalchemy.orm import relationship
from database import Base

class Revisao(Base):
    __tablename__ = "Revisao"

    ID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tema_id = Column(Integer, ForeignKey("Tema.ID", ondelete="CASCADE"), nullable=False)
    data_prevista = Column(Date, nullable=True)
    data_realizada = Column(DateTime, nullable=True)
    tempo_minutos = Column(Integer, nullable=True)
    status = Column(String(20), default='PENDENTE')
    tipo_revisao = Column(String(10))
    descricao = Column(Text, nullable=True)

    tema = relationship("Tema", back_populates="revisoes")
