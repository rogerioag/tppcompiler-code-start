import sys
import ply.yacc as yacc
import logging

# Get the token map from the lexer.  This is required.
from src.tpplexer.ply_lexer.tokens import tokens
from src.tpplexer.ply_lexer.methods import define_column
from src.tppparser.base import BaseParser
from src.tppparser.ply_parser import estado
from src.tppparser.ply_parser.newline_filter import NewlineFilter

# Regras da gramática (funções p_*), separadas por categoria em grammar/.
from src.tppparser.ply_parser.grammar import *

from anytree.exporter import DotExporter, UniqueDotExporter
from anytree import RenderTree, AsciiStyle

logging.basicConfig(
     level = logging.DEBUG,
     filename = "parser.log",
     filemode = "w",
     format = "%(filename)10s:%(lineno)4d:%(message)s"
)
log = logging.getLogger()

# NEWLINE não é produzido pelos analisadores léxicos: é inserido pelo
# NewlineFilter, entre o lexer e o parser.
tokens = list(tokens) + ['NEWLINE']

# Regra genérica de tratamento de erros. Se não existir um p_regra_error para tratar o erro, vem para essa geral.
def p_error(p):
    if p:
        token = p
        line = token.lineno
        column = define_column(estado.source_file, token.lexpos)
        if not estado.check_key:
            print("Erro:[{line},{column}]: Erro próximo ao token '{token}'".format(line=line, column=column, token=token.value))
        else:
            print(estado.error_handler.newError(estado.check_key, "ERR-SYN-EOF-INESPERADO"))
    else:
        print(estado.error_handler.newError(estado.check_key, "ERR-SYN-EOF-INESPERADO"))


class PLYParser(BaseParser):
    """
    Classe do analisador sintático baseado em PLY (Yacc).
    """

    # Construtor
    def __init__(self, check_key: bool = False, check_gentree: bool = False, lexer: str = "ply", **kwargs):
        self.check_key = check_key
        self.check_gentree = check_gentree
        self.lexer_strategy = lexer
        # module=: as regras (funções p_*) são procuradas neste módulo, que as
        # importa de grammar/.
        self.parser = yacc.yacc(module=sys.modules[__name__], method="LALR", optimize=True,
                                    start='programa', debug=False, debuglog=log,
                                    write_tables=False, tabmodule='tpp_parser_tab',
                                    errorlog=yacc.NullLogger())

    def parse(self, source_code: str, filename: str = "", check_key: bool = None, check_gentree: bool = None, **kwargs):
        estado.root = None
        estado.source_file = source_code
        ck = check_key if check_key is not None else self.check_key
        cg = check_gentree if check_gentree is not None else self.check_gentree
        estado.check_key = ck
        estado.check_gentree = cg

        from src.tpplexer import get_lexer
        lexer = NewlineFilter(get_lexer(self.lexer_strategy, check_key=ck))
        ast = self.parser.parse(source_code, lexer=lexer)

        if estado.root and estado.root.children != () and cg:
            print(estado.error_handler.newError(ck, 'WAR-SYN-GEN-SYNTAX-TREE'))
            if filename:
                try:
                    UniqueDotExporter(estado.root).to_picture(filename + ".unique.ast.png")
                    DotExporter(estado.root).to_dotfile(filename + ".ast.dot")
                    UniqueDotExporter(estado.root).to_dotfile(filename + ".unique.ast.dot")
                    with open(filename + "ascii_tree.txt", "w") as f:
                        f.write(RenderTree(estado.root, style=AsciiStyle()).by_attr())
                except Exception:
                    pass
                print(estado.error_handler.newError(ck, 'WAR-SYN-OUTPUT-FILE', file=filename + ".ast.png", teste='bla'))
            else:
                print(estado.error_handler.newError(ck, 'WAR-SYN-OUTPUT-FILE'))
            print(estado.error_handler.newError(ck, 'WAR-SYN-ANA-SUCCESS'))
        else:
            print(estado.error_handler.newError(ck, "ERR-SYN-IRRECUPERAVEL"))
            print(estado.error_handler.newError(ck, 'WAR-SYN-NOT-GEN-SYNTAX-TREE'))

        return estado.root or ast

