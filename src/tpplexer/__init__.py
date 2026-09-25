# src/tpplexer/__init__.py
"""
Pacote principal de análise léxica (tpplexer).
Factory para obtenção do lexer com base na estratégia solicitada.
"""

from .ply_lexer import PLYLexer
from .base import BaseLexer, Token
from .mandfa_lexer.mandfa_lexer import ManualDFALexer
from .symtable_lexer.symtableman_lexer import SymbolTableManLexer
from .symtable_lexer.symtable_lexer import SymbolTableLexer
from .automatalib_lexer.automatalibman_lexer import AutomataLibManLexer
from .automatalib_lexer.automatalib_lexer import AutomataLibLexer

__all__ = [
    "get_lexer",
    "PLYLexer",
    "ManualDFALexer",
    "SymbolTableManLexer",
    "SymbolTableLexer",
    "AutomataLibManLexer",
    "AutomataLibLexer",
    "BaseLexer",
    "Token",
]


def get_lexer(strategy="ply", **kwargs) -> BaseLexer:
    """
    Factory que retorna a instância do analisador léxico de acordo com a estratégia.
    """
    strategy = strategy.lower()
    if strategy == "ply":
        return PLYLexer(**kwargs)
    elif strategy in ("manual", "mandfa", "dfa"):
        return ManualDFALexer(**kwargs)
    elif strategy in ("symtableman"):
        return SymbolTableManLexer(**kwargs)
    elif strategy in ("symtable"):
        return SymbolTableLexer(**kwargs)
    elif strategy in ("automatalibman"):
        return AutomataLibManLexer(**kwargs)
    elif strategy in ("automatalib"):
        return AutomataLibLexer(**kwargs)
    else:
        raise ValueError(f"Estratégia léxica desconhecida: '{strategy}'")
