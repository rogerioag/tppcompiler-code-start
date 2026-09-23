# src/tpplexer/ply_lexer/__init__.py
"""
Submódulo PLYLexer - Analisador Léxico para a linguagem TPP usando PLY.
"""

from .tokens import *
from .regexs import *
from .methods import *
from .ply_lexer import PLYLexer

__all__ = [
    'tokens',
    'reserved_words',
    'reserved',
    'TOKENS_SYMBOLS',
    'PLYLexer',
    'get_tokens',
]

