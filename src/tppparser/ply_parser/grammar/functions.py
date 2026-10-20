"""
functions.py - Regras de declaração de funções: tipos de retorno, cabeçalho e parâmetros.
"""

from src.tppparser.mytree import MyNode


def p_declaracao_funcao(p):
    """declaracao_funcao : tipo cabecalho
                        | tipos_retorno cabecalho
                        | cabecalho
    """
    pai = MyNode(name='declaracao_funcao', type='DECLARACAO_FUNCAO')
    p[0] = pai
    p[1].parent = pai

    if len(p) == 3:
        p[2].parent = pai


# Sub-árvore:
#            (tipos_retorno)
#          /        |        \
# (ABRE_PARENTESE) (lista_tipos) (FECHA_PARENTESE)

def p_tipos_retorno(p):
    """tipos_retorno : ABRE_PARENTESE lista_tipos FECHA_PARENTESE"""

    pai = MyNode(name='tipos_retorno', type='TIPOS_RETORNO')
    p[0] = pai

    filho1 = MyNode(name='ABRE_PARENTESE', type='ABRE_PARENTESE', parent=pai)
    filho_sym1 = MyNode(name='(', type='SIMBOLO', parent=filho1)
    p[1] = filho1

    p[2].parent = pai  # lista_tipos

    filho3 = MyNode(name='FECHA_PARENTESE', type='FECHA_PARENTESE', parent=pai)
    filho_sym3 = MyNode(name=')', type='SIMBOLO', parent=filho3)
    p[3] = filho3


def p_lista_tipos(p):
    """lista_tipos : lista_tipos VIRGULA tipo
                    | tipo
    """
    pai = MyNode(name='lista_tipos', type='LISTA_TIPOS')
    p[0] = pai
    p[1].parent = pai

    if len(p) > 2:
        filho2 = MyNode(name='VIRGULA', type='VIRGULA', parent=pai)
        filho_sym2 = MyNode(name=',', type='SIMBOLO', parent=filho2)
        p[2] = filho2
        p[3].parent = pai


def p_cabecalho(p):
    """cabecalho : ID ABRE_PARENTESE lista_parametros FECHA_PARENTESE NEWLINE bloco FIM"""

    pai = MyNode(name='cabecalho', type='CABECALHO')
    p[0] = pai

    filho1 = MyNode(name='ID', type='ID', parent=pai)
    filho_id = MyNode(name=p[1], type='ID', parent=filho1)
    p[1] = filho1

    filho2 = MyNode(name='ABRE_PARENTESE', type='ABRE_PARENTESE', parent=pai)
    filho_sym2 = MyNode(name='(', type='SIMBOLO', parent=filho2)
    p[2] = filho2

    p[3].parent = pai  # lista_parametros

    filho4 = MyNode(name='FECHA_PARENTESE', type='FECHA_PARENTESE', parent=pai)
    filho_sym4 = MyNode(name=')', type='SIMBOLO', parent=filho4)
    p[4] = filho4

    p[6].parent = pai  # bloco (corpo)

    filho7 = MyNode(name='FIM', type='FIM', parent=pai)
    filho_id = MyNode(name='fim', type='FIM', parent=filho7)
    p[7] = filho7


def p_cabecalho_error(p):
    """cabecalho : ID ABRE_PARENTESE error FECHA_PARENTESE NEWLINE bloco FIM
                | ID ABRE_PARENTESE lista_parametros FECHA_PARENTESE NEWLINE error FIM
                | error ABRE_PARENTESE lista_parametros FECHA_PARENTESE NEWLINE bloco FIM
    """


def p_lista_parametros(p):
    """lista_parametros : lista_parametros VIRGULA parametro
                    | parametro
                    | vazio
    """

    pai = MyNode(name='lista_parametros', type='LISTA_PARAMETROS')
    p[0] = pai
    p[1].parent = pai

    if len(p) > 2:
        filho2 = MyNode(name='virgula', type='VIRGULA', parent=pai)
        filho_sym2 = MyNode(name=',', type='SIMBOLO', parent=filho2)
        p[2] = filho2
        p[3].parent = pai


def p_parametro(p):
    """parametro : tipo DOIS_PONTOS ID
                | parametro ABRE_COLCHETE FECHA_COLCHETE
    """

    pai = MyNode(name='parametro', type='PARAMETRO')
    p[0] = pai
    p[1].parent = pai

    if p[2] == ':':
        filho2 = MyNode(name='DOIS_PONTOS', type='DOIS_PONTOS', parent=pai)
        filho_sym2 = MyNode(name=':', type='SIMBOLO', parent=filho2)
        p[2] = filho2

        filho3 = MyNode(name='id', type='ID', parent=pai)
        filho_id = MyNode(name=p[3], type='ID', parent=filho3)
    else:
        filho2 = MyNode(name='abre_colchete', type='ABRE_COLCHETE', parent=pai)
        filho_sym2 = MyNode(name='[', type='SIMBOLO', parent=filho2)
        p[2] = filho2

        filho3 = MyNode(name='fecha_colchete', type='FECHA_COLCHETE', parent=pai)
        filho_sym3 = MyNode(name=']', type='SIMBOLO', parent=filho3)
        p[3] = filho3


def p_parametro_error(p):
    """parametro : tipo error ID
                | error ID
                | parametro error FECHA_COLCHETE
                | parametro ABRE_COLCHETE error
    """
