# src/tppparser/__init__.py
"""
Pacote principal de análise sintática (tppparser).
Factory para obtenção do parser com base na estratégia solicitada.
"""

from .base import BaseParser
from .ply_parser.ply_parser import PLYParser

__all__ = [
    "get_parser",
    "BaseParser",
    "PLYParser",
]


def get_parser(strategy="yacc", **kwargs) -> BaseParser:
    """
    Factory que retorna a instância do analisador sintático de acordo com a estratégia.
    """
    strategy = strategy.lower()
    if strategy in ("yacc", "ply", "lalr"):
        return PLYParser(**kwargs)
    else:
        raise ValueError(f"Estratégia sintática desconhecida: '{strategy}'")
