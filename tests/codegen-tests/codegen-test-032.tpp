{*Quicksort: Gabriela Paola Sereniski*}

inteiro partition(inteiro: v[], inteiro: e, inteiro: d)
	inteiro: pivo, i, j
	inteiro: aux
    pivo := v[e]
	i := e-1
    j := d+1
	
	repita
		repita
			i := i + 1

		até v[i] = pivo
		
		repita
			j := j + 1
		até v[j] = pivo 
		
		
        se i >= j então
			retorna(j)
        fim
		
        aux := v[i]
        v[i] := v[j]
        v[j] := aux
	até 1 <> 1
fim

quick (inteiro: v[], inteiro: e, inteiro: d)
    inteiro: p
    se e < d então
        p := partition(v, e, d)
        quick(v, e, p)
        quick(v, p+1, d)
    fim
fim

inteiro principal()
    {* inteiro: v[10] := {5, 3, 2, 4, 7, 1, 0, 6, 9, 8} *}

    inteiro: i
    inteiro: v[10]
    v[0] := 5
    v[1] := 3
    v[2] := 2
    v[3] := 4
    v[4] := 7
    v[5] := 1
    v[6] := 0
    v[7] := 6
    v[8] := 9
    v[9] := 8
    
    quick(v, 0, 9)
    
    i := 0

    repita 
        escreva(v[i])
        i := i + 1
    até i = 10

    retorna(0)
fim
