from anytree import Node, RenderTree
from anytree.exporter import DotExporter

atribuicao = Node("atribuicao")
var_1 = Node("var_1", parent=atribuicao)

ID_1 = Node("ID_1", parent=var_1)

id_a = Node("a", parent=ID_1)

symatrib = Node(":=", parent=atribuicao)
expressao = Node("expressao", parent=atribuicao)

expressao_logica = Node("expressao_logica", parent=expressao)

expressao_simples = Node("expressao_simples", parent=expressao_logica)

expressao_aditiva = Node("expressao_aditiva", parent=expressao_simples)


expressao_aditiva_2 = Node("expressao_aditiva_2", parent=expressao_aditiva)
operador_soma = Node("operador_soma", parent=expressao_aditiva)
expressao_multiplicativa_2 = Node("expressao_multiplicativa_2", parent=expressao_aditiva)

expressao_multiplicativa_1 = Node("expressao_multiplicativa_1", parent=expressao_aditiva_2)

expressao_unaria_1 = Node("expresssao_unaria_1", parent=expressao_multiplicativa_1)

fator_1 = Node("fator_1", parent=expressao_unaria_1)

var_2 = Node("var_2", parent=fator_1)

ID_2 = Node("ID_2", parent=var_2)

id_b = Node("b", parent=ID_2)

plus = Node("+", parent=operador_soma)


expressao_unaria_2 = Node("expresssao_unaria_2", parent=expressao_multiplicativa_2)

fator_2 = Node("fator_2", parent=expressao_unaria_2)

var_3 = Node("var_3", parent=fator_2)

ID_3 = Node("ID_3", parent=var_3)

id_c = Node("c", parent=ID_3)

DotExporter(atribuicao).to_picture("figura-atribuica.png")


atribuicao = Node(":=")
id_a = Node("a", parent=atribuicao)

expressao = Node("+", parent=atribuicao)

id_b = Node("b", parent=expressao)

id_c = Node("c", parent=expressao)

DotExporter(atribuicao).to_picture("figura-atribuica-asa.png")




