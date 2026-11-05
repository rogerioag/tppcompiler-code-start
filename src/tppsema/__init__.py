# src/tppsema/__init__.py
"""
Pacote principal de análise semântica (tppsema).
Factory para obtenção do analisador semântico com base na estratégia solicitada.
"""

from .base import BaseSema
from .sema.tppsema import TPPSema

__all__ = [
    "get_sema",
    "BaseSema",
    "TPPSema",
]


def get_sema(strategy="sema", **kwargs) -> BaseSema:
    """
    Factory que retorna a instância do analisador semântico de acordo com a estratégia.
    """
    strategy = strategy.lower()
    if strategy == "sema":
        return TPPSema(**kwargs)
    else:
        raise ValueError(f"Estratégia semântica desconhecida: '{strategy}'")
