{*Aviso: Variável 'b' declarada e inicializada, mas não utilizada*}
{*Aviso: Variável 'c' declarada e não inicializada*}
{*Aviso: Variável 'a' declarada e inicializada, mas não utilizada*}
{*Aviso: Atribuição de tipos distintos. Coerção implícita do valor de 'b' é do tipo 'inteiro' para 'c' que é 'flutuante'*}
{*Aviso: Atribuição de tipos distintos. Coerção implícita do valor retornado por 'func' é do tipo 'inteiro' para 'a' que é 'flutuante'*}
{*Erro: Função 'principal' deveria retornar 'inteiro', mas retorna 'vazio'*}

inteiro func(inteiro: x, inteiro: y)
	retorna (x + y)
fim

inteiro principal()
	flutuante: a
	flutuante: c
	inteiro: b

	b := c

	a := func(10,5)
fim
