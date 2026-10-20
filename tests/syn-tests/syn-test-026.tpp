inteiro: a

(inteiro, flutuante) funct(inteiro: x, inteiro: y)
    inteiro: res
    res := x + 1
    retorna(res, x/y)
fim

inteiro principal()
    inteiro: a
    flutuante: b

    (a,b) := funct(1,2)

    retorna(0)
fim
