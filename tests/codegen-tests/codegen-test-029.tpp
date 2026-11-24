{*Busca Linear*}

inteiro: A[20]

inteiro busca(inteiro: n)
	
	inteiro: retorno
	inteiro: i

	retorno := 0
	i := 0

	repita 
		se A[i] = n então
			retorno := 1
		fim		
		i := i + 1
	até i = 20

	retorna(retorno)
fim

inteiro principal()

	inteiro: i
	inteiro: n

	i := 0

	repita 
		A[i] := i
		i := i + 1
	até i = 20

	leia(n)
	escreva(busca(n))
	retorna(0)
fim
