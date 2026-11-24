{*Primo*}

inteiro principal()
	inteiro: digitado
	inteiro: i
	flutuante: f
	inteiro: int
	flutuante: resultado

	leia(digitado)
	i := 1
	repita
		f := i/2.0
		int := i/2
		resultado := f - int
		
		se resultado > 0 então
			escreva (i)
		fim
		i := i+1
	até i <= digitado
fim
