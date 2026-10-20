from anytree import Node, RenderTree
from anytree.exporter import UniqueDotExporter

# Árvore sintática de "a := b + c - d" (dentro de uma função), conforme a
# gramática TPP v1.1 (docs/grammar/grammar.md):
#   atribuicao ::= lista_expressoes ATRIBUICAO lista_expressoes
# O lado esquerdo é lido como expressão, como no Python; a Análise Semântica
# verifica se o alvo é uma variável. A soma e a subtração estão no mesmo nível
# (expressao_aditiva) e associam à esquerda: (b + c) - d.
# O UniqueDotExporter identifica cada nó pelo objeto, e não pelo nome, por
# isso nós com o mesmo nome (expressao, fator, var...) não são unidos. Os
# sufixos numéricos ficam só nos nomes das variáveis Python.

atribuicao = Node("atribuicao")

# Lado esquerdo: a
lista_expressoes_1 = Node("lista_expressoes", parent=atribuicao)
expressao_1 = Node("expressao", parent=lista_expressoes_1)
expressao_logica_1 = Node("expressao_logica", parent=expressao_1)
expressao_simples_1 = Node("expressao_simples", parent=expressao_logica_1)
expressao_aditiva_1 = Node("expressao_aditiva", parent=expressao_simples_1)
expressao_multiplicativa_1 = Node("expressao_multiplicativa", parent=expressao_aditiva_1)
expressao_unaria_1 = Node("expressao_unaria", parent=expressao_multiplicativa_1)
fator_1 = Node("fator", parent=expressao_unaria_1)
var_1 = Node("var", parent=fator_1)
ID_1 = Node("ID", parent=var_1)
id_a = Node("a", parent=ID_1)

ATRIBUICAO = Node("ATRIBUICAO", parent=atribuicao)
symatrib = Node(":=", parent=ATRIBUICAO)

# Lado direito: (b + c) - d
lista_expressoes_2 = Node("lista_expressoes", parent=atribuicao)
expressao_2 = Node("expressao", parent=lista_expressoes_2)
expressao_logica_2 = Node("expressao_logica", parent=expressao_2)
expressao_simples_2 = Node("expressao_simples", parent=expressao_logica_2)

# expressao_aditiva_2 : expressao_aditiva_3 operador_soma_2 expressao_multiplicativa_4   ((b + c) - d)
expressao_aditiva_2 = Node("expressao_aditiva", parent=expressao_simples_2)

# expressao_aditiva_3 : expressao_aditiva_4 operador_soma_1 expressao_multiplicativa_3   (b + c)
expressao_aditiva_3 = Node("expressao_aditiva", parent=expressao_aditiva_2)

# b
expressao_aditiva_4 = Node("expressao_aditiva", parent=expressao_aditiva_3)
expressao_multiplicativa_2 = Node("expressao_multiplicativa", parent=expressao_aditiva_4)
expressao_unaria_2 = Node("expressao_unaria", parent=expressao_multiplicativa_2)
fator_2 = Node("fator", parent=expressao_unaria_2)
var_2 = Node("var", parent=fator_2)
ID_2 = Node("ID", parent=var_2)
id_b = Node("b", parent=ID_2)

# +
operador_soma_1 = Node("operador_soma", parent=expressao_aditiva_3)
MAIS = Node("MAIS", parent=operador_soma_1)
plus = Node("+", parent=MAIS)

# c
expressao_multiplicativa_3 = Node("expressao_multiplicativa", parent=expressao_aditiva_3)
expressao_unaria_3 = Node("expressao_unaria", parent=expressao_multiplicativa_3)
fator_3 = Node("fator", parent=expressao_unaria_3)
var_3 = Node("var", parent=fator_3)
ID_3 = Node("ID", parent=var_3)
id_c = Node("c", parent=ID_3)

# -
operador_soma_2 = Node("operador_soma", parent=expressao_aditiva_2)
MENOS = Node("MENOS", parent=operador_soma_2)
minus = Node("-", parent=MENOS)

# d
expressao_multiplicativa_4 = Node("expressao_multiplicativa", parent=expressao_aditiva_2)
expressao_unaria_4 = Node("expressao_unaria", parent=expressao_multiplicativa_4)
fator_4 = Node("fator", parent=expressao_unaria_4)
var_4 = Node("var", parent=fator_4)
ID_4 = Node("ID", parent=var_4)
id_d = Node("d", parent=ID_4)

UniqueDotExporter(atribuicao).to_picture("figura-atribuica.png")


# Árvore podada (ASA): a subtração é a raiz da expressão porque (b + c) é
# calculado primeiro.
atribuicao = Node(":=")
id_a = Node("a", parent=atribuicao)

subtracao = Node("-", parent=atribuicao)

soma = Node("+", parent=subtracao)
id_b = Node("b", parent=soma)
id_c = Node("c", parent=soma)

id_d = Node("d", parent=subtracao)

UniqueDotExporter(atribuicao).to_picture("figura-atribuica-asa.png")
