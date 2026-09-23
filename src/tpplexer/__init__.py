# src/tpplexer/__init__.py
"""
Pacote principal de análise léxica (tpplexer).
Factory para obtenção do lexer com base na estratégia solicitada.
"""

from .ply_lexer import PLYLexer
from .base import BaseLexer, Token

__all__ = ["get_lexer", "PLYLexer", "BaseLexer", "Token"]


def get_lexer(strategy="ply", **kwargs) -> BaseLexer:
    """
    Factory que retorna a instância do analisador léxico de acordo com a estratégia.
    """
    strategy = strategy.lower()
    if strategy == "ply":
        return PLYLexer(**kwargs)
    elif strategy == "manual":
        try:
            from .mandfa_lexer.mandfa_lexer import ManualDFALexer
            return ManualDFALexer(**kwargs)
        except (ImportError, AttributeError):
            raise NotImplementedError("ManualDFALexer ainda não está implementado.")
    elif strategy == "symtable":
        try:
            from .symtable_lexer.symtable_lexer import SymbolTableLexer
            return SymbolTableLexer(**kwargs)
        except (ImportError, AttributeError):
            raise NotImplementedError("SymbolTableLexer ainda não está implementado.")
    else:
        raise ValueError(f"Estratégia léxica desconhecida: '{strategy}'")
