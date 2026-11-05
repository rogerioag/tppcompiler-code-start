{*Aviso: Coerção implícita do valor de 'b', 'inteiro' para 'flutuante'*}
{*Aviso: Coerção implícita do valor de 'a', 'flutuante' para 'inteiro'*}
{*Erro: Função 'principal' deveria retornar 'inteiro', mas retorna 'vazio'*}

flutuante: a
inteiro: b

inteiro principal()
	b := 18
	a := 1.0

	a := b
	b := a
fim
