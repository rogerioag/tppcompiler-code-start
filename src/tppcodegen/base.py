# src/tppcodegen/base.py
from abc import ABC, abstractmethod
from typing import Any


class BaseCodeGen(ABC):
    """
    Classe base para geradores de código da linguagem TPP.
    """

    @abstractmethod
    def generate(self, tree: Any, filename: str = "", symbol_table: Any = None, **kwargs) -> Any:
        """
        Gera o código intermediário/final a partir da árvore sintática abstrata
        (ASA) produzida pela análise semântica e grava o arquivo de saída.
        """
        pass
