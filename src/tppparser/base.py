# src/tppparser/base.py
from abc import ABC, abstractmethod
from typing import Any


class BaseParser(ABC):
    """
    Classe base para analisadores sintáticos da linguagem TPP.
    """

    @abstractmethod
    def parse(self, source_code: str, **kwargs) -> Any:
        """
        Executa a análise sintática sobre o código-fonte fornecido.
        """
        pass
