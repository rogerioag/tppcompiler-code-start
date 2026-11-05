# src/tppsema/base.py
from abc import ABC, abstractmethod
from typing import Any


class BaseSema(ABC):
    """
    Classe base para analisadores semânticos da linguagem TPP.
    """

    @abstractmethod
    def analyze(self, tree: Any, **kwargs) -> Any:
        """
        Verifica as regras semânticas sobre a árvore sintática produzida pelo
        parser e retorna a árvore sintática abstrata podada (ASA).
        """
        pass
