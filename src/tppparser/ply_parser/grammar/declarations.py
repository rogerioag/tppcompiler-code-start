"""
declarations.py - Regras de declaração e inicialização de variáveis, variáveis indexadas e tipos.
"""

import logging

from src.tppparser.ply_parser import estado
from src.tppparser.mytree import MyNode


# Sub-árvore.
#      (declaracao_variaveis)
#      / p[1]    |           \
# (tipo)    (DOIS_PONTOS)    (lista_variaveis)
#                |
#               (:)
#
# Com inicialização, seguem (ATRIBUICAO) e (lista_expressoes) ou
# (atribuicao_encadeada):
#   inteiro: v[5] := {1, 2, 3, 4, 5}
#   inteiro: a := b := 1      {* declara só a; b já foi declarada *}


def p_declaracao_variaveis(p):
    """declaracao_variaveis : tipo DOIS_PONTOS lista_variaveis
                            | tipo DOIS_PONTOS lista_variaveis ATRIBUICAO lista_expressoes
                            | tipo DOIS_PONTOS lista_variaveis ATRIBUICAO atribuicao_encadeada
    """

    pai = MyNode(name='declaracao_variaveis', type='DECLARACAO_VARIAVEIS')
    p[0] = pai

    p[1].parent = pai

    filho = MyNode(name='DOIS_PONTOS', type='DOIS_PONTOS', parent=pai)
    filho_sym = MyNode(name=p[2], type='SIMBOLO', parent=filho)
    p[2] = filho

    p[3].parent = pai

    if len(p) == 6:
        filho4 = MyNode(name='ATRIBUICAO', type='ATRIBUICAO', parent=pai)
        filho_sym4 = MyNode(name=':=', type='SIMBOLO', parent=filho4)
        p[4] = filho4

        p[5].parent = pai  # lista_expressoes ou atribuicao_encadeada


# Sub-árvore:
#             (atribuicao_encadeada)
#           /          |           \
# (lista_alvos)  (ATRIBUICAO)  (lista_expressoes ou atribuicao_encadeada)
#       |
#     (var)
#
# Cada elo do encadeamento tem uma única var como alvo. Com uma lista de
# alvos, em "inteiro: a := b, ..." o parser não conseguiria decidir se b é um
# alvo ou um valor (conflito reduce/reduce). Na árvore, a var fica dentro de
# um nó lista_alvos, como nas demais atribuições.

def p_atribuicao_encadeada(p):
    """atribuicao_encadeada : var ATRIBUICAO lista_expressoes
                            | var ATRIBUICAO atribuicao_encadeada
    """

    pai = MyNode(name='atribuicao_encadeada', type='ATRIBUICAO_ENCADEADA')
    p[0] = pai

    alvos = MyNode(name='lista_alvos', type='LISTA_ALVOS', parent=pai)
    p[1].parent = alvos  # var

    filho2 = MyNode(name='ATRIBUICAO', type='ATRIBUICAO', parent=pai)
    filho_sym2 = MyNode(name=':=', type='SIMBOLO', parent=filho2)
    p[2] = filho2

    p[3].parent = pai  # lista_expressoes ou atribuicao_encadeada


# Sub-árvore.
#          (inicializacao_variaveis)
#          /           |           \
# (lista_alvos)  (ATRIBUICAO)  (lista_expressoes)
#
# Os alvos podem estar entre parênteses: (a, b) := 1, 2
#
# No escopo global os alvos são sempre var (lista_alvos) e não há
# encadeamento: com expressões no lado esquerdo, "f()" seria ambíguo
# entre uma chamada e o cabeçalho de uma função sem parâmetros.

def p_inicializacao_variaveis(p):
    """inicializacao_variaveis : lista_alvos ATRIBUICAO lista_expressoes
                              | ABRE_PARENTESE lista_alvos FECHA_PARENTESE ATRIBUICAO lista_expressoes
    """

    pai = MyNode(name='inicializacao_variaveis', type='INICIALIZACAO_VARIAVEIS')
    p[0] = pai

    if len(p) == 6:
        filho1 = MyNode(name='ABRE_PARENTESE', type='ABRE_PARENTESE', parent=pai)
        filho_sym1 = MyNode(name='(', type='SIMBOLO', parent=filho1)
        p[1] = filho1

        p[2].parent = pai  # lista_alvos

        filho3 = MyNode(name='FECHA_PARENTESE', type='FECHA_PARENTESE', parent=pai)
        filho_sym3 = MyNode(name=')', type='SIMBOLO', parent=filho3)
        p[3] = filho3

        filho4 = MyNode(name='ATRIBUICAO', type='ATRIBUICAO', parent=pai)
        filho_sym4 = MyNode(name=':=', type='SIMBOLO', parent=filho4)
        p[4] = filho4

        p[5].parent = pai  # lista_expressoes
    else:
        p[1].parent = pai  # lista_alvos

        filho2 = MyNode(name='ATRIBUICAO', type='ATRIBUICAO', parent=pai)
        filho_sym2 = MyNode(name=':=', type='SIMBOLO', parent=filho2)
        p[2] = filho2

        p[3].parent = pai  # lista_expressoes


def p_lista_variaveis(p):
    """lista_variaveis : lista_variaveis VIRGULA var
                        | var
    """
    pai = MyNode(name='lista_variaveis', type='LISTA_VARIAVEIS')
    p[0] = pai
    if len(p) > 2:
        p[1].parent = pai
        filho = MyNode(name='virgula', type='VIRGULA', parent=pai)
        filho_sym = MyNode(name=',', type='SIMBOLO', parent=filho)
        p[3].parent = pai
    else:
       p[1].parent = pai


def p_lista_alvos(p):
    """lista_alvos : lista_alvos VIRGULA var
                    | var
    """
    pai = MyNode(name='lista_alvos', type='LISTA_ALVOS')
    p[0] = pai
    p[1].parent = pai

    if len(p) > 2:
        filho2 = MyNode(name='VIRGULA', type='VIRGULA', parent=pai)
        filho_sym2 = MyNode(name=',', type='SIMBOLO', parent=filho2)
        p[2] = filho2
        p[3].parent = pai


def p_var(p):
    """var : ID
            | ID indice
    """

    pai = MyNode(name='var', type='VAR')
    p[0] = pai
    filho = MyNode(name='ID', type='ID', parent=pai)
    filho_id = MyNode(name=p[1], type='ID', parent=filho)
    p[1] = filho
    if len(p) > 2:
        p[2].parent = pai


def p_indice(p):
    """indice : indice ABRE_COLCHETE expressao FECHA_COLCHETE
                | ABRE_COLCHETE expressao FECHA_COLCHETE
    """
    pai = MyNode(name='indice', type='INDICE')
    p[0] = pai
    if len(p) == 5:
        p[1].parent = pai   # indice

        filho2 = MyNode(name='abre_colchete', type='ABRE_COLCHETE', parent=pai)
        filho_sym2 = MyNode(name=p[2], type='SIMBOLO', parent=filho2)
        p[2] = filho2

        p[3].parent = pai  # expressao

        filho4 = MyNode(name='fecha_colchete', type='FECHA_COLCHETE', parent=pai)
        filho_sym4 = MyNode(name=p[4], type='SIMBOLO', parent=filho4)
        p[4] = filho4
    else:
        filho1 = MyNode(name='abre_colchete', type='ABRE_COLCHETE', parent=pai)
        filho_sym1 = MyNode(name=p[1], type='SIMBOLO', parent=filho1)
        p[1] = filho1

        p[2].parent = pai  # expressao

        filho3 = MyNode(name='fecha_colchete', type='FECHA_COLCHETE', parent=pai)
        filho_sym3 = MyNode(name=p[3], type='SIMBOLO', parent=filho3)
        p[3] = filho3


def p_indice_error(p):
    """indice : ABRE_COLCHETE error FECHA_COLCHETE
                | indice ABRE_COLCHETE error FECHA_COLCHETE
    """

    # print("Erro na definicao do indice. Expressao ou indice.")
    print(estado.error_handler.newError(estado.check_key, 'ERR-SYN-INDICE'))

    # print("Erro:p[0]:{p0}, p[1]:{p1}, p[2]:{p2}, p[3]:{p3}".format(p0=p[0], p1=p[1], p2=p[2], p3=p[3]))
    error_line = p.lineno(2)
    father = MyNode(name='ERR-SYN-INDICE::{}'.format(error_line), type='ERROR')
    logging.error(
        "Syntax error parsing index rule at line {}".format(error_line))
    p.parser.errok()
    p[0] = father


# Sub-árvore:
#    (tipo)
#      |
#  (FLUTUANTE)
def p_tipo(p):
    """tipo : INTEIRO
        | FLUTUANTE
    """

    pai = MyNode(name='tipo', type='TIPO')
    p[0] = pai
    # p[1] = MyNode(name=p[1], type=p[1].upper(), parent=pai)

    if p[1] == "inteiro":
        filho1 = MyNode(name='INTEIRO', type='INTEIRO', parent=pai)
        filho_sym = MyNode(name=p[1], type=p[1].upper(), parent=filho1)
        p[1] = filho1
    else:
        filho1 = MyNode(name='FLUTUANTE', type='FLUTUANTE', parent=pai)
        filho_sym = MyNode(name=p[1], type=p[1].upper(), parent=filho1)
