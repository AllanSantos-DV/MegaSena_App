# src/data/storage_interface.py
from abc import ABC, abstractmethod
from typing import List

from src.core.base_types import Numbers


class StorageInterface(ABC):
    @abstractmethod
    def create_storage(self) -> bool:
        """Cria o armazenamento se não existir."""
        pass

    @abstractmethod
    def list_carts(self) -> List[str]:
        """Lista todos os carrinhos disponíveis."""
        pass

    @abstractmethod
    def add_cart(self, name: str, tickets: List[Numbers]) -> bool:
        """Adiciona ou atualiza um carrinho com seus jogos."""
        pass

    @abstractmethod
    def get_cart_tickets(self, name: str) -> List[Numbers]:
        """Obtém os jogos de um carrinho específico."""
        pass

    @abstractmethod
    def delete_cart(self, name: str) -> bool:
        """Remove um carrinho específico."""
        pass

    @abstractmethod
    def cart_exists(self, name: str) -> bool:
        """Verifica se um carrinho existe."""
        pass
