{*Maior do Vetor*}

inteiro maiorvetor(inteiro:v[], inteiro:tam)
	inteiro: maior
	inteiro: i := 0
	maior := v[0]

	repita
		se v[i] > maior então
			maior := v[i]
		fim
		i := i + 1
	até i = tam
	retorna(maior)
fim

inteiro principal()
	inteiro: v[5] := {1,2,3,4,5}
	inteiro: maior := maiorvetor(v,5)
	escreva(maior)
	retorna(0)
fim
