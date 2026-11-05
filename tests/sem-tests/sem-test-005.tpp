{*Erro: Chamada à função 'func' com número de parâmetros menor que o declarado.*}
{*Erro: Chamada à função 'func' com número de parâmetros maior que o declarado.*}
{*Aviso: Chamada à função 'func' com Coerção Implícita do valor do argumento '10.5' tipo 'flutuante' diferente do parâmetro declarado 'inteiro'.*}
{*Aviso: Chamada à função 'func' com Coerção Implícita do valor do argumento '10.5' tipo 'flutuante' diferente do parâmetro declarado 'inteiro'.*}
{*Aviso: Chamada à função 'func' com Coerção Implícita do valor do argumento 'b' tipo 'flutuante' diferente do parâmetro declarado 'inteiro'.*}
{*Aviso: Variável 'a' declarada e inicializada, mas não utilizada*}
{*Erro: Função 'principal' deveria retornar 'inteiro', mas retorna 'vazio'*}

inteiro func(inteiro: x, inteiro: y)
	retorna(x + y)
fim

inteiro principal()
	inteiro: a
	flutuante: b
	b := 10.5

	a := func(10)
	a := func(10,20,30)
	a := func(10.5,20)
	a := func(10.5,b)
fim
