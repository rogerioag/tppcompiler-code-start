"""
methods.py - Funções e regras de ação semântica/léxica do PLY para TPP.
"""

from ply.lex import TOKEN
from .tokens import reserved_words
from .regexs import (
    id_regex,
    notacao_cientifica,
    flutuante,
    inteiro,
)
from src.myerror import MyError

le = MyError('LexerErrors')
check_key = False

# Caracteres ignorados (espaço e tabulação)
t_ignore = " \t"


def define_column(input_data: str, lexpos: int) -> int:
    """Calcula o número da coluna (1-indexed) a partir do deslocamento lexpos."""
    begin_line = input_data.rfind("\n", 0, lexpos) + 1
    return (lexpos - begin_line) + 1


@TOKEN(id_regex)
def t_ID(token):
    """Reconhece identificadores e palavras reservadas."""
    token.type = reserved_words.get(token.value, "ID")
    return token


@TOKEN(notacao_cientifica)
def t_NUM_NOTACAO_CIENTIFICA(token):
    """Reconhece literais em notação científica."""
    return token

@TOKEN(flutuante)
def t_NUM_PONTO_FLUTUANTE(token):
    """Reconhece números de ponto flutuante."""
    return token

@TOKEN(inteiro)
def t_NUM_INTEIRO(token):
    """Reconhece números inteiros."""
    return token

def t_COMENTARIO(token):
    r"(\{((.|\n)*?)\})"
    token.lexer.lineno += token.value.count("\n")

def t_COMENTARIO_NAO_FECHADO(t):
    r'\{[^}]*$'
    column = define_column(t.lexer.lexdata, t.lexpos)
    message = le.newError(check_key, 'ERR-LEX-UNC-COMMENT', t.lineno, column)
    print(message)
    t.lexer.lineno += t.value.count('\n')

def t_newline(token):
    r"\n+"
    token.lexer.lineno += len(token.value)

def t_error(token):
    column = define_column(token.lexer.lexdata, token.lexpos)
    message = le.newError(check_key, 'ERR-LEX-INV-CHAR', token.lineno, column, valor=token.value[0])
    print(message)
    token.lexer.skip(1)
