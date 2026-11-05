{*Erro: Variável 'c' não declarada*}


{*
WAR-SEM-ATR-DIFF-TYPES-IMP-COERC-OF-EXP=Atribuição de tipos distintos. Coerção implícita do valor de '{}' que é do tipo '{}' para '{}' que é '{}'.
WAR-SEM-ATR-DIFF-TYPES-IMP-COERC-OF-RET-VAL=Atribuição de tipos distintos. Coerção implícita do valor retornado por '{}' que é do tipo '{}' para '{}' que é '{}'.
WAR-SEM-ATR-DIFF-TYPES-IMP-COERC-OF-NUM=


Atribuição de tipos distintos. Coerção implícita do valor de 'b' que é do tipo 'inteiro' para 'a' que é 'flutuante'.
*}

{*Aviso: Coerção implícita do valor de 'b', 'inteiro' para 'flutuante'*}
{*Aviso: Coerção implícita do valor de 'expressao', 'inteiro' para 'flutuante'*}
{*Aviso: Atribuição de tipos distintos. Coerção implícita do valor atribuído '15' que é do tipo 'inteiro' para 'a' que é 'flutuante'*}
{*Aviso: Coerção implícita do valor retornado por 'func', 'inteiro' para 'flutuante'*}
{*Aviso: Variável 'a' declarada e inicializada, mas não utilizada*}
{*Erro: Função 'principal' deveria retornar 'inteiro', mas retorna 'vazio'*}

{*função func retorna c que não foi declarada, considerar vazio?*}

flutuante: a
inteiro: b

inteiro func()
  retorna(c)
fim

inteiro principal()
	b := 18
	a := b

	a := b + 25

	a := 15

	a := func()
fim
