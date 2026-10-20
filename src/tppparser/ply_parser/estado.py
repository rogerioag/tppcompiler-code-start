"""
estado.py - Estado compartilhado entre as regras da gramática durante uma análise.

As regras ficam em módulos separados (grammar/), por isso leem e escrevem estes
valores por meio do módulo (estado.check_key, estado.root), e não por import
direto dos nomes, que copiaria o valor do momento do import.
"""

from src.myerror import MyError

error_handler = MyError('ParserErrors')

# Código-fonte em análise (usado para calcular a coluna dos erros).
source_file = ""

# Imprimir as chaves dos erros em vez das mensagens.
check_key = False

# Gerar a árvore sintática.
check_gentree = False

# Raiz da árvore sintática, definida pela regra programa.
root = None
