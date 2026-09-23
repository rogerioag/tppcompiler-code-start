# src/tpplexer/LogErrorLexer.py
from src.myerror import MyError
import logging

logging.basicConfig(
    level=logging.DEBUG,
    filename="lex.log",
    filemode="w",
    format="%(filename)10s:%(lineno)4d:%(message)s"
)

log = logging.getLogger("tppcompiler")
le = MyError('LexerErrors')

class LogErrorLexer:
    """
    Tratamento de Logging e Erros Léxicos.
    """
    def __init__(self):
        self.log = log
        self.le = le
