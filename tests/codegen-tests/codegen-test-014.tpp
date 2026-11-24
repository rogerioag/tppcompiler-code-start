{*Repita, Leia, Escreva, Função*}

inteiro soma(inteiro: a, inteiro:b)
    retorna(a + b)
fim

inteiro principal()
    inteiro: a
    inteiro: b
    inteiro: c
    inteiro: i

    i := 0
    c := 0

    repita
        leia(a)
        leia(b)
        se (a <> b) então
            c := soma(a, b)
            escreva(c)
        fim
        i := i + 1
    até i = 5

    retorna(0)
fim
