"""
Regras da gramática TPP, separadas por categoria (ver docs/grammar/grammar.md).

Cada regra de recuperação de erro (p_*_error) fica junto da regra principal.

O PLY procura as regras (funções p_*) no módulo que chama yacc.yacc(); por isso
ply_parser.py importa tudo deste pacote. O PLY ordena as regras pelo número da
linha, que se repete entre os arquivos: isso não altera o parser enquanto o
símbolo inicial for passado explicitamente (start='programa') e não houver
conflitos reduce/reduce, que seriam resolvidos pela ordem das regras.
"""

from .program import *
from .declarations import *
from .functions import *
from .commands import *
from .expressions import *
from .operators import *
