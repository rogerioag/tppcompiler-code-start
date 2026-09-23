# src/tpplexer/base.py
from abc import ABC, abstractmethod
from typing import Optional, List, Any


class Token:
    """
    Representação padronizada de um Token no compilador.
    Totalmente compatível com as expectativas do ply.yacc e parsers manuais.
    """
    def __init__(self, type: str, value: Any, lineno: int = 1, lexpos: int = 0):
        self.type = type
        self.value = value
        self.lineno = lineno
        self.lexpos = lexpos

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, line={self.lineno}, pos={self.lexpos})"

    def __eq__(self, other):
        if not isinstance(other, Token):
            return False
        return (self.type == other.type and 
                self.value == other.value and 
                self.lineno == other.lineno)


class BaseLexer(ABC):
    """
    Classe Abstrata que define a interface obrigatória de todos os Lexers.
    """

    @abstractmethod
    def input(self, data: str) -> None:
        """
        Carrega a string do código-fonte TPP no lexer.
        """
        pass

    @abstractmethod
    def token(self) -> Optional[Token]:
        """
        Retorna o próximo Token da entrada ou None quando atingir o Fim de Arquivo (EOF).
        """
        pass

    def tokenize(self, data: str) -> List[Token]:
        """
        Método utilitário que consome toda a entrada e retorna a lista de Tokens.
        Muito útil para a suíte de testes automatizados e impressão na CLI.
        """
        self.input(data)
        tokens = []
        while True:
            tok = self.token()
            if tok is None:
                break
            tokens.append(tok)
        return tokens

    @staticmethod
    def get_column(data: str, lexpos: int) -> int:
        """
        Calcula a coluna (1-indexed) a partir da posição lexpos no texto.
        """
        begin_line = data.rfind('\n', 0, lexpos) + 1
        return (lexpos - begin_line) + 1
