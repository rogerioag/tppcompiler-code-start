# src/tpplexer/ply_lexer/ply_lexer.py
import sys
import ply.lex as lex
from typing import Optional

from ..base import BaseLexer, Token
from .tokens import *
from .regexs import *
from .methods import *
from . import methods
from ..LogErrorLexer import log, le


class PLYLexer(BaseLexer):
    """
    Implementação do Analisador Léxico de TPP usando Python Lex-Yacc (PLY).
    """

    def __init__(self, check_key: bool = False, optimize: bool = False, debug: bool = False):
        self.check_key = check_key
        methods.check_key = check_key
        methods.le = le

        self.lexer = lex.lex(
            module=sys.modules[__name__],
            optimize=optimize,
            debug=debug,
            debuglog=log if debug else None,
        )

    def input(self, data: str) -> None:
        """Carrega o código-fonte no lexer."""
        self.lexer.input(data)

    def token(self) -> Optional[Token]:
        """Retorna o próximo token padronizado ou None em EOF."""
        tok = self.lexer.token()
        if tok is None:
            return None
        return Token(type=tok.type, value=tok.value, lineno=tok.lineno, lexpos=tok.lexpos)

    def get_tokens(self, data: str):
        """
        Retorna o iterador de tokens sob demanda para o código-fonte fornecido.
        """
        self.input(data)
        return iter(self.token, None)
