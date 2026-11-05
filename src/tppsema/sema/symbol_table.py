# src/tppsema/sema/symbol_table.py
"""
Tabela de Símbolos da linguagem TPP.

TODO (alunos): implementar a tabela de símbolos conforme a seção
"Tabela de Símbolos" do docs/SEM-SPECS.md. Cada entrada deve guardar, por
exemplo: token, lexema, tipo, número de dimensões e tamanho de cada dimensão,
escopo, se foi inicializada, se foi utilizada, linha e coluna. Para funções,
também os tipos dos parâmetros e os tipos de retorno (retorno múltiplo).
"""


class TabelaSimbolos:
    """
    Tabela de símbolos com suporte a escopos (global e de cada função).
    """

    def __init__(self):
        # TODO (alunos): definir a estrutura de armazenamento dos símbolos e escopos.
        self.simbolos = {}
