from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base

class Cronograma(Base):
    __tablename__ = "Cronograma"

    ID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("Usuario.ID", ondelete="CASCADE"), nullable=False)
    disciplina_id = Column(Integer, ForeignKey("Disciplina.ID", ondelete="CASCADE"), nullable=False)
    dia_semana = Column(String(20), nullable=False)
    ordem = Column(Integer, default=0)

    usuario = relationship("User", back_populates="cronogramas")
    disciplina = relationship("Disciplina", back_populates="cronogramas")
