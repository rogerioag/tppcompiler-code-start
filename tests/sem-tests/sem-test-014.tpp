{*Aviso: Função 'func' declarada, mas não utilizada*}
{*Aviso: Coerção implícita do valor atribuído para 'a', 'inteiro' para 'flutuante'*}
{*Erro: Função 'func' deveria retornar 'inteiro', mas retorna 'flutuante'*}
{*Aviso: Variável 'b' declarada e inicializada, mas não utilizada*}
{*Aviso: Chamada recursiva para 'principal'*}
{*Erro: Função 'principal' deveria retornar 'inteiro', mas retorna 'vazio'*}

flutuante: a
inteiro: b

inteiro func()
  a := 10
  retorna(a)
fim

inteiro principal()
	b := 18
	principal()
fim
