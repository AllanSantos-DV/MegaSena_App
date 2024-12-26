# src/data/storage_factory.py
from typing import Optional

from .excel_storage import ExcelStorage
from .storage_interface import StorageInterface


class StorageFactory:
    @staticmethod
    def get_storage(storage_type: str = "excel", **kwargs) -> Optional[StorageInterface]:
        """
        Cria e retorna uma instância do armazenamento especificado.

        Args:
            storage_type: Tipo de armazenamento ("Excel", etc)
            **kwargs: Argumentos específicos para o tipo de armazenamento

        Returns:
            StorageInterface or None: Instância do armazenamento ou None se tipo inválido
        """
        if storage_type.lower() == "excel":
            file_path = kwargs.get("file_path", "xlsx/carrinhos.xlsx")
            return ExcelStorage(file_path)

        return None
