inteiro: V1[5]

inteiro somavet(inteiro: vet[], inteiro: tam)
	inteiro: result 
	inteiro: i 

	result := 0
	i := 0

	repita
		result := result + vet[i]
		i := i + 1
	até i = tam - 1

	retorna(result)	
fim

inteiro principal ()
	inteiro: x
	
	V1[0] := 1
	V1[1] := 2
	V1[2] := 3
	V1[3] := 4
	V1[4] := 5

	x := somavet(V1,T)

	retorna(0)
fim
