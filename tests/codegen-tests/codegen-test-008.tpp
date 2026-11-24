{*Repita*}

inteiro: n
inteiro: soma

inteiro principal()
	n := 10
	soma := 0
	repita
		soma := soma + n
		n := n - 1
	até n = 0

	retorna(soma)
fim
