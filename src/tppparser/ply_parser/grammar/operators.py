"""
operators.py - Regras dos operadores relacionais, aditivos, lógicos, de negação e multiplicativos.
"""

from src.tppparser.mytree import MyNode


def p_operador_relacional(p):
    """operador_relacional : MENOR
                            | MAIOR
                            | IGUAL
                            | DIFERENTE 
                            | MENOR_IGUAL
                            | MAIOR_IGUAL
    """
    pai = MyNode(name='operador_relacional', type='OPERADOR_RELACIONAL')
    p[0] = pai

    if p[1] == "<":
        filho = MyNode(name='MENOR', type='MENOR', parent=pai)
        filho_sym = MyNode(name=p[1], type='SIMBOLO', parent=filho)
    elif p[1] == ">":
        filho = MyNode(name='MAIOR', type='MAIOR', parent=pai)
        filho_sym = MyNode(name=p[1], type='SIMBOLO', parent=filho)
    elif p[1] == "=":
        filho = MyNode(name='IGUAL', type='IGUAL', parent=pai)
        filho_sym = MyNode(name=p[1], type='SIMBOLO', parent=filho)
    elif p[1] == "<>":
        filho = MyNode(name='DIFERENTE', type='DIFERENTE', parent=pai)
        filho_sym = MyNode(name=p[1], type='SIMBOLO', parent=filho)
    elif p[1] == "<=":
        filho = MyNode(name='MENOR_IGUAL', type='MENOR_IGUAL', parent=pai)
        filho_sym = MyNode(name=p[1], type='SIMBOLO', parent=filho)
    elif p[1] == ">=":
        filho = MyNode(name='MAIOR_IGUAL', type='MAIOR_IGUAL', parent=pai)
        filho_sym = MyNode(name=p[1], type='SIMBOLO', parent=filho)
    else:
        print('Erro operador relacional')

    p[1] = filho


def p_operador_soma(p):
    """operador_soma : MAIS
                    | MENOS
    """
    if p[1] == "+":
        mais = MyNode(name='MAIS', type='MAIS')
        mais_lexema = MyNode(name='+', type='SIMBOLO', parent=mais)
        p[0] = MyNode(name='operador_soma',
                      type='OPERADOR_SOMA', children=[mais])
    else:
       menos = MyNode(name='MENOS', type='MENOS')
       menos_lexema = MyNode(name='-', type='SIMBOLO', parent=menos)
       p[0] = MyNode(name='operador_soma',
                     type='OPERADOR_SOMA', children=[menos])


def p_operador_logico(p):
    """operador_logico : E
                    | OU
    """
    if p[1] == "&&":
        filho = MyNode(name='E', type='E')
        filho_lexema = MyNode(name=p[1], type='SIMBOLO', parent=filho)
        p[0] = MyNode(name='operador_logico',
                      type='OPERADOR_LOGICO', children=[filho])
    else:
        filho = MyNode(name='OU', type='OU')
        filho_lexema = MyNode(name=p[1], type='SIMBOLO', parent=filho)
        p[0] = MyNode(name='operador_logico',
                      type='OPERADOR_SOMA', children=[filho])


def p_operador_negacao(p):
    """operador_negacao : NAO"""

    if p[1] == "!":
        filho = MyNode(name='NAO', type='NAO')
        negacao_lexema = MyNode(name=p[1], type='SIMBOLO', parent=filho)
        p[0] = MyNode(name='operador_negacao',
                      type='OPERADOR_NEGACAO', children=[filho])


def p_operador_multiplicacao(p):
    """operador_multiplicacao : VEZES
                            | DIVIDE
        """
    if p[1] == "*":
        filho = MyNode(name='VEZES', type='VEZES')
        vezes_lexema = MyNode(name=p[1], type='SIMBOLO', parent=filho)
        p[0] = MyNode(name='operador_multiplicacao',
                      type='OPERADOR_MULTIPLICACAO', children=[filho])
    else:
       divide = MyNode(name='DIVIDE', type='DIVIDE')
       divide_lexema = MyNode(name=p[1], type='SIMBOLO', parent=divide)
       p[0] = MyNode(name='operador_multiplicacao',
                     type='OPERADOR_MULTIPLICACAO', children=[divide])
