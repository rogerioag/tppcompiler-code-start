{*Para Binário*}

paraBinario(inteiro: n) 
    inteiro: N[32]
  
    inteiro: i
    inteiro: j
    
    i := 0

    repita
        N[i] := n - (n / 2) * 2
        n := n / 2
        i := i + 1
    até n = 0

    j := i -1 

    repita
        escreva(N[j])
        j := j -1 

    até j < 0

fim 
  
inteiro principal() 
    inteiro : num

    leia(num)
    paraBinario(num)
fim
