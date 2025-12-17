from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declared_attr

class TimestampMixin:
    """
    Mixin que adiciona colunas de timestamp `criado_em` e `atualizado_em` a um modelo.
    `criado_em` é definido uma vez na criação do registro.
    `atualizado_em` é atualizado toda vez que o registro é modificado.
    """
    @declared_attr
    def criado_em(cls):
        return Column(DateTime, server_default=func.now(), nullable=False)

    @declared_attr
    def atualizado_em(cls):
        return Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
