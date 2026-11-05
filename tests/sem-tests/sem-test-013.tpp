{*Erro: Chamada para a função 'principal' não permitida*}
{*Aviso: Atribuição de tipos distintos. Coerção implícita do valor atribuído '10' do tipo 'inteiro' para 'a' que é 'flutuante'*}
{*Aviso: Atribuição de tipos distintos. Coerção implícita do valor retornado por 'func' é do tipo 'inteiro' para 'a' que é 'flutuante'*}
{*Aviso: Variável 'b' declarada e inicializada, mas não utilizada*}
{*Erro: Função 'principal' deveria retornar 'inteiro', mas retorna 'vazio'*}
{*Erro: Função 'func' deveria retornar 'inteiro', mas retorna 'flutuante'*}

flutuante: a
inteiro: b

inteiro func()
  a := 10
  principal()
  retorna(a)
fim

inteiro principal()
	b := 18
	a := func()
fim
