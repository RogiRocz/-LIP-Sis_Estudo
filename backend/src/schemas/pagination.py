from pydantic import BaseModel, computed_field
from typing import List, TypeVar, Generic
from math import ceil

T = TypeVar('T')

class Page(BaseModel, Generic[T]):
    """Modelo de resposta para listas paginadas."""
    items: List[T]
    total: int
    page: int
    size: int

    @computed_field
    @property
    def pages(self) -> int:
        """O número total de páginas."""
        if self.size == 0:
            return 0
        return ceil(self.total / self.size)
