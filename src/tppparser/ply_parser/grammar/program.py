"""
program.py - Regras do programa e da lista de declarações globais.
"""

from src.tppparser.ply_parser import estado
from src.tppparser.mytree import MyNode


# Sub-árvore.
#       (programa)
#           |
#   (lista_declaracoes)
#     /     |      \
#   ...    ...     ...

def p_programa(p):
    """programa : lista_declaracoes"""

    programa = MyNode(name='programa', type='PROGRAMA')

    estado.root = programa
    p[0] = programa
    p[1].parent = programa


#    (lista_declaracoes)                          (lista_declaracoes)
#          /           \                                    |
# (lista_declaracoes)  (declaracao)                    (declaracao)

def p_lista_declaracoes(p):
    """lista_declaracoes : lista_declaracoes declaracao NEWLINE
                        | declaracao NEWLINE
    """
    pai = MyNode(name='lista_declaracoes', type='LISTA_DECLARACOES')
    p[0] = pai
    p[1].parent = pai

    if len(p) > 3:
        p[2].parent = pai


# Sub-árvore.
#      (declaracao)
#           |
#  (declaracao_variaveis ou
#   inicializacao_variaveis ou
#   declaracao_funcao)


def p_declaracao(p):
    """declaracao : declaracao_variaveis
                | inicializacao_variaveis
                | declaracao_funcao
    """
    pai = MyNode(name='declaracao', type='DECLARACAO')
    p[0] = pai
    p[1].parent = pai


# Regra para representar \epsilon (vazio).
def p_vazio(p):
    """vazio : """

    pai = MyNode(name='vazio', type='VAZIO')
    p[0] = pai
