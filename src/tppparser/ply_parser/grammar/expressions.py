"""
expressions.py - Regras das expressões, do fator e das listas de expressões e argumentos.
"""

import logging

from src.tppparser.ply_parser import estado
from src.tppparser.mytree import MyNode


def p_expressao(p):
    """expressao : expressao_logica"""
    pai = MyNode(name='expressao', type='EXPRESSAO')
    p[0] = pai
    p[1].parent = pai


def p_expressao_logica(p):
    """expressao_logica : expressao_simples
                    | expressao_logica operador_logico expressao_simples
    """
    pai = MyNode(name='expressao_logica', type='EXPRESSAO_LOGICA')
    p[0] = pai
    p[1].parent = pai

    if len(p) > 2:
        p[2].parent = pai
        p[3].parent = pai


def p_expressao_simples(p):
    """expressao_simples : expressao_aditiva
                        | expressao_simples operador_relacional expressao_aditiva
    """

    pai = MyNode(name='expressao_simples', type='EXPRESSAO_SIMPLES')
    p[0] = pai
    p[1].parent = pai

    if len(p) > 2:
        p[2].parent = pai
        p[3].parent = pai


def p_expressao_aditiva(p):
    """expressao_aditiva : expressao_multiplicativa
                        | expressao_aditiva operador_soma expressao_multiplicativa
    """

    pai = MyNode(name='expressao_aditiva', type='EXPRESSAO_ADITIVA')
    p[0] = pai
    p[1].parent = pai

    if len(p) > 2:
        p[2].parent = pai
        p[3].parent = pai


def p_expressao_multiplicativa(p):
    """expressao_multiplicativa : expressao_unaria
                               | expressao_multiplicativa operador_multiplicacao expressao_unaria
        """

    pai = MyNode(name='expressao_multiplicativa',
                 type='EXPRESSAO_MULTIPLICATIVA')
    p[0] = pai
    p[1].parent = pai

    if len(p) > 2:
        p[2].parent = pai
        p[3].parent = pai


def p_expressao_unaria(p):
    """expressao_unaria : fator
                        | operador_soma fator
                        | operador_negacao fator
        """
    pai = MyNode(name='expressao_unaria', type='EXPRESSAO_UNARIA')
    p[0] = pai
    p[1].parent = pai

    if p[1] == '!':
        filho1 = MyNode(name='operador_negacao',
                        type='OPERADOR_NEGACAO', parent=pai)
        filho_sym1 = MyNode(name=p[1], type='SIMBOLO', parent=filho1)
        p[1] = filho1
    else:
        p[1].parent = pai

    if len(p) > 2:
        p[2].parent = pai


def p_lista_expressoes(p):
    """lista_expressoes : lista_expressoes VIRGULA expressao
                        | expressao
    """
    pai = MyNode(name='lista_expressoes', type='LISTA_EXPRESSOES')
    p[0] = pai
    p[1].parent = pai

    if len(p) > 2:
        filho2 = MyNode(name='VIRGULA', type='VIRGULA', parent=pai)
        filho_sym2 = MyNode(name=',', type='SIMBOLO', parent=filho2)
        p[2] = filho2
        p[3].parent = pai


def p_fator(p):
    """fator : ABRE_PARENTESE expressao FECHA_PARENTESE
            | var
            | chamada_funcao
            | numero
            | inicializacao_arranjo
            | tupla
        """
    pai = MyNode(name='fator', type='FATOR')
    p[0] = pai
    if len(p) > 2:
        filho1 = MyNode(name='ABRE_PARENTESE', type='ABRE_PARENTESE', parent=pai)
        filho_sym1 = MyNode(name=p[1], type='SIMBOLO', parent=filho1)
        p[1] = filho1

        p[2].parent = pai

        filho3 = MyNode(name='FECHA_PARENTESE', type='FECHA_PARENTESE', parent=pai)
        filho_sym3 = MyNode(name=p[3], type='SIMBOLO', parent=filho3)
        p[3] = filho3
    else:
        p[1].parent = pai


def p_fator_error(p):
    """fator : ABRE_PARENTESE error FECHA_PARENTESE
        """


# Sub-árvore:
#                  (tupla)
#          /          |          \       \         \
# (ABRE_PARENTESE) (lista_expressoes) (VIRGULA) (expressao) (FECHA_PARENTESE)
#
# Como no Python, a tupla permite alvos entre parênteses: (a, b) := b, a.
# A análise semântica deve rejeitar tuplas fora do lado esquerdo de uma atribuição.

def p_tupla(p):
    """tupla : ABRE_PARENTESE lista_expressoes VIRGULA expressao FECHA_PARENTESE"""

    pai = MyNode(name='tupla', type='TUPLA')
    p[0] = pai

    filho1 = MyNode(name='ABRE_PARENTESE', type='ABRE_PARENTESE', parent=pai)
    filho_sym1 = MyNode(name='(', type='SIMBOLO', parent=filho1)
    p[1] = filho1

    p[2].parent = pai  # lista_expressoes

    filho3 = MyNode(name='VIRGULA', type='VIRGULA', parent=pai)
    filho_sym3 = MyNode(name=',', type='SIMBOLO', parent=filho3)
    p[3] = filho3

    p[4].parent = pai  # expressao

    filho5 = MyNode(name='FECHA_PARENTESE', type='FECHA_PARENTESE', parent=pai)
    filho_sym5 = MyNode(name=')', type='SIMBOLO', parent=filho5)
    p[5] = filho5


# Sub-árvore:
#            (inicializacao_arranjo)
#          /          |           \
# (ABRE_CHAVE) (lista_expressoes) (FECHA_CHAVE)

def p_inicializacao_arranjo(p):
    """inicializacao_arranjo : ABRE_CHAVE lista_expressoes FECHA_CHAVE"""

    pai = MyNode(name='inicializacao_arranjo', type='INICIALIZACAO_ARRANJO')
    p[0] = pai

    filho1 = MyNode(name='ABRE_CHAVE', type='ABRE_CHAVE', parent=pai)
    filho_sym1 = MyNode(name='{', type='SIMBOLO', parent=filho1)
    p[1] = filho1

    p[2].parent = pai  # lista_expressoes

    filho3 = MyNode(name='FECHA_CHAVE', type='FECHA_CHAVE', parent=pai)
    filho_sym3 = MyNode(name='}', type='SIMBOLO', parent=filho3)
    p[3] = filho3


def p_numero(p):
    """numero : NUM_INTEIRO
                | NUM_PONTO_FLUTUANTE
                | NUM_NOTACAO_CIENTIFICA
    """

    pai = MyNode(name='numero', type='NUMERO')
    p[0] = pai

    if str(p[1]).find('.') == -1:
        aux = MyNode(name='NUM_INTEIRO', type='NUM_INTEIRO', parent=pai)
        aux_val = MyNode(name=p[1], type='VALOR', parent=aux)
        p[1] = aux
    elif str(p[1]).find('e') >= 0:
        aux = MyNode(name='NUM_NOTACAO_CIENTIFICA',
                     type='NUM_NOTACAO_CIENTIFICA', parent=pai)
        aux_val = MyNode(name=p[1], type='VALOR', parent=aux)
        p[1] = aux
    else:
        aux = MyNode(name='NUM_PONTO_FLUTUANTE',
                     type='NUM_PONTO_FLUTUANTE', parent=pai)
        aux_val = MyNode(name=p[1], type='VALOR', parent=aux)
        p[1] = aux


def p_chamada_funcao(p):
    """chamada_funcao : ID ABRE_PARENTESE lista_argumentos FECHA_PARENTESE"""

    pai = MyNode(name='chamada_funcao', type='CHAMADA_FUNCAO')
    p[0] = pai
    if len(p) > 2:
        filho1 = MyNode(name='ID', type='ID', parent=pai)
        filho_id = MyNode(name=p[1], type='ID', parent=filho1)
        p[1] = filho1

        filho2 = MyNode(name='ABRE_PARENTESE', type='ABRE_PARENTESE', parent=pai)
        filho_sym = MyNode(name=p[2], type='SIMBOLO', parent=filho2)
        p[2] = filho2

        p[3].parent = pai

        filho4 = MyNode(name='FECHA_PARENTESE', type='FECHA_PARENTESE', parent=pai)
        filho_sym = MyNode(name=p[4], type='SIMBOLO', parent=filho4)
        p[4] = filho4
    else:
        p[1].parent = pai


def p_lista_argumentos(p):
    """lista_argumentos : lista_argumentos VIRGULA expressao
                    | expressao
                    | vazio
        """
    pai = MyNode(name='lista_argumentos', type='LISTA_ARGUMENTOS')
    p[0] = pai

    if len(p) > 2:
        p[1].parent = pai

        filho2 = MyNode(name='VIRGULA', type='VIRGULA', parent=pai)
        filho_sym = MyNode(name=p[2], type='SIMBOLO', parent=filho2)
        p[2] = filho2

        p[3].parent = pai
    else:
        p[1].parent = pai


def p_lista_argumentos_error(p):
    """lista_argumentos : error VIRGULA expressao
        """
    print(estado.error_handler.newError(estado.check_key, 'ERR-SYN-LISTA-ARGUMENTOS'))
    
    error_line = p.lineno(2)
    father = MyNode(name='ERR-SYN-LISTA-ARGUMENTOS::{}'.format(error_line), type='ERROR')
    logging.error(
        "Syntax error parsing index rule at line {}".format(error_line))
    p.parser.errok()
    p[0] = father
