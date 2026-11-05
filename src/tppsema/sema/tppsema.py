# src/tppsema/sema/tppsema.py
"""
TPPSema: analisador semântico da linguagem TPP.

Recebe a árvore sintática produzida pelo parser (src/tppparser), constrói a
tabela de símbolos, verifica as regras semânticas (docs/SEM-SPECS.md) e
devolve a árvore sintática abstrata podada (ASA).
"""

from src.myerror import MyError
from src.tppsema.base import BaseSema
from src.tppsema.sema.symbol_table import TabelaSimbolos
from src.tppsema.sema.pruning import podar
from src.tppsema.sema import rules


class TPPSema(BaseSema):
    """
    Analisador semântico da linguagem TPP.
    """

    def __init__(self, check_key: bool = False, **kwargs):
        self.check_key = check_key
        self.error_handler = MyError('SemaErrors')
        self.tabela = TabelaSimbolos()
        self.erros = 0
        self.avisos = 0

    def emitir(self, chave: str, *args, linha=None, coluna=None):
        """
        Imprime uma mensagem de erro (ERR-SEM-*) ou de aviso (WAR-SEM-*).

        Com a opção -k, imprime apenas a chave; caso contrário, imprime a
        mensagem do SemaErrorMessages.properties, preenchendo os '{}' com args.
        Todas as regras devem emitir suas mensagens por este método.
        """
        if chave.startswith('ERR-'):
            self.erros += 1
        else:
            self.avisos += 1
        print(self.error_handler.newError(self.check_key, chave, linha, coluna, *args))

    def analyze(self, tree, check_key: bool = None, **kwargs):
        if check_key is not None:
            self.check_key = check_key
        self.tabela = TabelaSimbolos()
        self.erros = 0
        self.avisos = 0

        # Cada módulo de rules/ verifica uma categoria de regras do SEM-SPECS.
        for regra in rules.REGRAS:
            regra.verificar(tree, self.tabela, self)

        return podar(tree)
