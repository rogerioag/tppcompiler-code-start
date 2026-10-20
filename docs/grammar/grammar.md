# Gramática TPP

### (Versão 1.1, Data: 14/10/2026)

## Alterações:

> __Extensões para a Gramática:__
>
> 1. __Atribuição Múltipla__
>
>    Queríamos que fosse possível a _atribuição múltipla_, como existem em linguagens como o `Python`. A atribuição de números, variáveis, expressões ou de retornos de função.
>
>    ```tpp
>    a := 1
>    a := b
>    a,b := c,1
>    a,b := 1,2
>    (a,b) := 1,2
>    a,b := (1,2)
>    (a,b) := (1,2)
>    a,b := c+d,3+4
>    (a,b) := c+d,3+4
>    a,b := (c+d,3+4)
>    (a,b) := (c+d,3+4)
>    a,b := c,d
>    a,b := (c,d)
>    (a,b) := c,d
>    (a,b) := (c,d)
>    a,b := funct(x, y)
>    (a,b) := funct(x, y)
>    ```
>
> 2. __Retorno Múltiplo__
>
>    ```tpp
>    (inteiro, flutuante) funct(inteiro: x, inteiro:y)
>        inteiro: res
>        res := x * 2;
>        retorna(res, x/y)
>    fim
>       
>    inteiro principal()
>        inteiro: a
>        flutuante: b
>       
>        (a,b) := funct(1,2)
>       
>        retorna(0)
>    fim
>    ```
>
> 
>
> 
>
> 3. __Inicialização de arrays__

## Gramática Original (Versão 1.0)

```ebnf
programa ::= lista_declaracoes
lista_declaracoes ::= lista_declaracoes declaracao 
                      | declaracao
declaracao ::= declaracao_variaveis
              | inicializacao_variaveis
              | declaracao_funcao
declaracao_variaveis ::= tipo DOIS_PONTOS lista_variaveis
inicializacao_variaveis ::= atribuicao
lista_variaveis ::= lista_variaveis VIRGULA var
                    | var
var ::= ID 
        | ID indice
indice ::= indice ABRE_COLCHETE expressao FECHA_COLCHETE
          | ABRE_COLCHETE expressao FECHA_COLCHETE
tipo ::= INTEIRO 
         | FLUTUANTE
declaracao_funcao ::= tipo cabecalho 
                      | cabecalho
cabecalho ::= ID ABRE_PARENTESE lista_parametros FECHA_PARENTESE corpo FIM
lista_parametros ::= lista_parametros VIRGULA parametro 
                     | parametro 
                     | vazio
parametro ::= tipo DOIS_PONTOS ID 
              | parametro ABRE_COLCHETE FECHA_COLCHETE
corpo ::= corpo acao | vazio 
acao ::= expressao 
         | declaracao_variaveis
         | se 
         | repita
         | leia 
         | escreva
         | retorna
         | erro
se ::= SE expressao ENTAO corpo FIM
       | SE expressao ENTAO corpo SENAO corpo FIM
repita ::= REPITA corpo ATE expressao
atribuicao ::= var ATRIBUICAO expressao
leia ::= LEIA ABRE_PARENTESE var FECHA_PARENTESE
escreva ::= ESCREVA ABRE_PARENTESE expressao FECHA_PARENTESE
retorna ::= RETORNA ABRE_PARENTESE expressao FECHA_PARENTESE
expressao ::= expressao_logica
              | atribuicao
expressao_logica ::= expressao_simples
                     | expressao_logica operador_logico expressao_simples
expressao_simples ::= expressao_aditiva
                      | expressao_simples operador_relacional expressao_aditiva
expressao_aditiva ::= expressao_multiplicativa
                      | expressao_aditiva operador_soma expressao_multiplicativa
expressao_multiplicativa ::= expressao_unaria
                             | expressao_multiplicativa operador_multiplicacao expressao_unaria
expressao_unaria ::= fator
                     | operador_soma fator
                     | operador_negacao fator
operador_relacional ::= MENOR
                        | MAIOR 
                        | IGUAL 
                        | DIFERENTE 
                        | MENOR_IGUAL 
                        | MAIOR_IGUAL
operador_soma ::= MAIS
                  | MENOS
operador_logico ::= E
                  | OU
operador_negacao ::= NAO
operador_multiplicacao ::= VEZES 
                           | DIVIDE
fator ::= ABRE_PARENTESE expressao FECHA_PARENTESE
          | var
          | chamada_funcao
          | numero
numero ::= NUM_INTEIRO
           | NUM_PONTO_FLUTUANTE
           | NUM_NOTACAO_CIENTIFICA
chamada_funcao ::= ID ABRE_PARENTESE lista_argumentos FECHA_PARENTESE
lista_argumentos  ::= lista_argumentos VIRGULA expressao
                      | expressao
                      | vazio
```



## Definição da Gramática para `TPP` (Versão 1.1):

```ebnf
programa ::= lista_declaracoes
lista_declaracoes ::= lista_declaracoes declaracao NEWLINE
                      | declaracao NEWLINE
declaracao ::= declaracao_variaveis
              | inicializacao_variaveis
              | declaracao_funcao
declaracao_variaveis ::= tipo DOIS_PONTOS lista_variaveis
                         | tipo DOIS_PONTOS lista_variaveis ATRIBUICAO lista_expressoes
                         | tipo DOIS_PONTOS lista_variaveis ATRIBUICAO atribuicao_encadeada
atribuicao_encadeada ::= var ATRIBUICAO lista_expressoes
                         | var ATRIBUICAO atribuicao_encadeada
inicializacao_variaveis ::= lista_alvos ATRIBUICAO lista_expressoes
                            | ABRE_PARENTESE lista_alvos FECHA_PARENTESE ATRIBUICAO lista_expressoes
lista_variaveis ::= lista_variaveis VIRGULA var
                    | var
var ::= ID 
        | ID indice
indice ::= indice ABRE_COLCHETE expressao FECHA_COLCHETE
          | ABRE_COLCHETE expressao FECHA_COLCHETE
tipo ::= INTEIRO 
         | FLUTUANTE
declaracao_funcao ::= tipo cabecalho
                      | tipos_retorno cabecalho
                      | cabecalho
tipos_retorno ::= ABRE_PARENTESE lista_tipos FECHA_PARENTESE
lista_tipos ::= lista_tipos VIRGULA tipo
                | tipo
cabecalho ::= ID ABRE_PARENTESE lista_parametros FECHA_PARENTESE NEWLINE bloco FIM
lista_parametros ::= lista_parametros VIRGULA parametro 
                     | parametro 
                     | vazio
parametro ::= tipo DOIS_PONTOS ID 
              | parametro ABRE_COLCHETE FECHA_COLCHETE
bloco ::= corpo
          | corpo acao
corpo ::= corpo acao NEWLINE
          | vazio
acao ::= expressao
         | atribuicao
         | declaracao_variaveis
         | se 
         | repita
         | leia 
         | escreva
         | retorna
         | erro
se ::= SE expressao ENTAO bloco FIM
       | SE expressao ENTAO bloco SENAO bloco FIM
repita ::= REPITA bloco ATE expressao
atribuicao ::= lista_expressoes ATRIBUICAO lista_expressoes
               | lista_expressoes ATRIBUICAO atribuicao
lista_alvos ::= lista_alvos VIRGULA var
                | var
lista_expressoes ::= lista_expressoes VIRGULA expressao
                     | expressao
leia ::= LEIA ABRE_PARENTESE var FECHA_PARENTESE
escreva ::= ESCREVA ABRE_PARENTESE expressao FECHA_PARENTESE
retorna ::= RETORNA ABRE_PARENTESE lista_expressoes FECHA_PARENTESE
expressao ::= expressao_logica
expressao_logica ::= expressao_simples
                     | expressao_logica operador_logico expressao_simples
expressao_simples ::= expressao_aditiva
                      | expressao_simples operador_relacional expressao_aditiva
expressao_aditiva ::= expressao_multiplicativa
                      | expressao_aditiva operador_soma expressao_multiplicativa
expressao_multiplicativa ::= expressao_unaria
                             | expressao_multiplicativa operador_multiplicacao expressao_unaria
expressao_unaria ::= fator
                     | operador_soma fator
                     | operador_negacao fator
operador_relacional ::= MENOR
                        | MAIOR 
                        | IGUAL 
                        | DIFERENTE 
                        | MENOR_IGUAL 
                        | MAIOR_IGUAL
operador_soma ::= MAIS
                  | MENOS
operador_logico ::= E
                  | OU
operador_negacao ::= NAO
operador_multiplicacao ::= VEZES 
                           | DIVIDE
fator ::= ABRE_PARENTESE expressao FECHA_PARENTESE
          | var
          | chamada_funcao
          | numero
          | inicializacao_arranjo
          | tupla
tupla ::= ABRE_PARENTESE lista_expressoes VIRGULA expressao FECHA_PARENTESE
inicializacao_arranjo ::= ABRE_CHAVE lista_expressoes FECHA_CHAVE
numero ::= NUM_INTEIRO
           | NUM_PONTO_FLUTUANTE
           | NUM_NOTACAO_CIENTIFICA
chamada_funcao ::= ID ABRE_PARENTESE lista_argumentos FECHA_PARENTESE
lista_argumentos  ::= lista_argumentos VIRGULA expressao
                      | expressao
                      | vazio
```

## Extensões: atribuição múltipla, retorno múltiplo, inicialização de arranjos e NEWLINE

- **Retorno múltiplo:** a função declara os tipos de retorno entre parênteses (`tipos_retorno`) e `retorna` aceita uma lista de expressões.
- **Atribuição múltipla:** a atribuição aceita listas nos dois lados do `:=` e deixou de ser uma `expressao`: passou a ser apenas um comando (`acao`).
- **Atribuição encadeada:** dentro das funções, `atribuicao` lê o lado esquerdo como `lista_expressoes`, como faz o Python, e a análise semântica verifica se cada alvo é uma `var`. Se os alvos fossem `lista_alvos`, em `a := b, ...` o parser não conseguiria decidir se `b` é um alvo ou um valor (a gramática deixaria de ser LALR(1)). Assim, `a := b := 0` e `a, b := c, d := 1, 2` são aceitos.
- **Escopo global:** `inicializacao_variaveis` usa `lista_alvos` (opcionalmente entre parênteses) e não permite encadeamento. Com expressões no lado esquerdo, `f()` seria ambíguo entre uma chamada e o cabeçalho de uma função sem parâmetros.
- **Alvos entre parênteses:** como no Python, `(a, b) := b, a` é uma `tupla` no lado esquerdo e `(a) := 1` é só uma expressão entre parênteses. A tupla pode aparecer em qualquer expressão; a análise semântica deve rejeitá-la fora do lado esquerdo de uma atribuição.
- **NEWLINE:** os comandos terminam com o token `NEWLINE`, que **não é produzido pelos analisadores léxicos**: o `NewlineFilter`, entre o `lexer` e o `parser`, insere o `NEWLINE` numa quebra de linha (como a inserção automática de `;` da linguagem `Go`) quando o último _token_ da linha é `ID`, número, `)`, `]`, `}` ou `fim` e a quebra não está dentro de `()`, `[]` ou `{}`. Depois de `então`, `senão`, `repita`, `até`, operadores e `,`, a quebra de linha é continuação. O último comando de um `bloco` pode dispensar o `NEWLINE` (`se x > y então x := y fim`). Sem o `NEWLINE`, `x := y` seguido de `(a, b) := 1, 2` na linha de baixo seria lido como a chamada `y(a, b)`; com ele, a gramática não tem conflitos LALR(1).
  - Um comando por linha (exceto o último de um bloco, que pode ficar na linha do `fim`/`senão`/`até`).
  - Uma expressão só pode continuar na linha seguinte depois de um operador ou `,`, ou dentro de `()`, `[]` e `{}`: `x := a +` / `b` é uma atribuição; `x := a` / `+ b` são dois comandos.
  - `se condição` deve ter o `então` na mesma linha.
- **Declaração com inicialização:** `declaracao_variaveis` aceita um `:=` depois da lista de variáveis, para escalares e arranjos (`inteiro: a := 1`, `inteiro: a, b := 1, 2`, `inteiro: v[5] := {1, 2, 3, 4, 5}`). Com `atribuicao_encadeada`, `inteiro: a := b := 1` declara só `a`; `b` precisa já ter sido declarada, e as duas recebem `1`. Cada elo do encadeamento tem uma única `var` como alvo: com uma lista de alvos, em `inteiro: a := b, ...` o parser não conseguiria decidir se `b` é um alvo ou um valor (conflito reduce/reduce). Por isso `inteiro: a, b := c, d := 1, 2` e `inteiro: a := f() := 1` são erros de sintaxe.
- **Inicialização de arranjos:** `inicializacao_arranjo` usa os tokens `ABRE_CHAVE` (`{`) e `FECHA_CHAVE` (`}`). Por isso os comentários passaram de `{ ... }` para `{* ... *}`. Arranjos multidimensionais usam inicializadores aninhados.

```tpp
{* Exemplo *}
inteiro: A[6], M[2][2]
A := {1, 2, 3, 4, 5, 6}
M := {{1, 2}, {3, 4}}
```

+ __Inicialização parcial (elementos restantes viram `0`):__ Como na linguagem `C` a linguagem deve permitir inicialização parcial dos elementos de arranjos.

```
inteiro: v[5] := {1, 2} {* Equivale a {1, 2, 0, 0, 0} *}
v[4] := {1, 2} {* Equivale a V[4] := 1 *}
```

```tpp
(inteiro, flutuante) divmod(inteiro: a, inteiro: b)
  retorna(a / b, a - (a / b) * b)
fim

inteiro principal()
  inteiro: q, r
  q, r := divmod(10, 3)
  q, r := r, q
  q := r := 0
  (q, r) := r, q
  se q > r então q := r fim
  retorna(0)
fim
```

Ficam para a análise semântica: cada alvo de `atribuicao` deve ser uma `var` (rejeitar `f() := 1` ou `1 := x`); o número de alvos deve ser igual ao número de valores (ou ao número de retornos, se o lado direito for uma única chamada de função); `retorna(...)` deve ser compatível com os tipos declarados da função; e o inicializador não pode exceder as dimensões do array. Em `atribuicao_encadeada`, cada alvo precisa já ter sido declarado e ser compatível com o tipo do valor.

## Registro de mudanças em relação à gramática original

### Tokens

| Token | Lexema | Produzido por | Motivo |
|---|---|---|---|
| `ABRE_CHAVE` | `{` | analisadores léxicos (todos) | inicialização de arrays |
| `FECHA_CHAVE` | `}` | analisadores léxicos (todos) | inicialização de arrays |
| `NEWLINE` | quebra de linha | `NewlineFilter`, entre o lexer e o parser | terminador de comando |

Os **comentários** passaram de `{ ... }` para `{* ... *}`, porque `{` e `}` viraram _tokens_. Um `{*` sem o `*}` correspondente continua gerando `ERR-LEX-UNC-COMMENT`.

### Regras novas

| Regra | Para quê |
|---|---|
| `tipos_retorno ::= ABRE_PARENTESE lista_tipos FECHA_PARENTESE` | tipos de retorno múltiplo: `(inteiro, flutuante) f(...)` |
| `lista_tipos ::= lista_tipos VIRGULA tipo \| tipo` | lista de tipos de `tipos_retorno` |
| `lista_alvos ::= lista_alvos VIRGULA var \| var` | alvos da atribuição no escopo global |
| `lista_expressoes ::= lista_expressoes VIRGULA expressao \| expressao` | alvos e valores da atribuição, valores do `retorna` e elementos do `inicializacao_arranjo` e da `tupla` |
| `tupla ::= ABRE_PARENTESE lista_expressoes VIRGULA expressao FECHA_PARENTESE` | alvos entre parênteses: `(a, b) := b, a` |
| `inicializacao_arranjo ::= ABRE_CHAVE lista_expressoes FECHA_CHAVE` | `A := {1, 2, 3}` e `M := {{1, 2}, {3, 4}}` |
| `bloco ::= corpo \| corpo acao` | permite que o último comando de um bloco dispense o `NEWLINE` |
| `atribuicao_encadeada ::= var ATRIBUICAO lista_expressoes \| var ATRIBUICAO atribuicao_encadeada` | encadeamento na declaração: `inteiro: a := b := 1` |

### Regras Alteradas

```diff
  lista_declaracoes ::=
-     lista_declaracoes declaracao
-     | declaracao
+     lista_declaracoes declaracao NEWLINE
+     | declaracao NEWLINE

  declaracao_variaveis ::=
      tipo DOIS_PONTOS lista_variaveis
+     | tipo DOIS_PONTOS lista_variaveis ATRIBUICAO lista_expressoes
+     | tipo DOIS_PONTOS lista_variaveis ATRIBUICAO atribuicao_encadeada

  inicializacao_variaveis ::=
-     atribuicao
+     lista_alvos ATRIBUICAO lista_expressoes
+     | ABRE_PARENTESE lista_alvos FECHA_PARENTESE ATRIBUICAO lista_expressoes

  declaracao_funcao ::=
      tipo cabecalho
+     | tipos_retorno cabecalho
      | cabecalho

  cabecalho ::=
-     ID ABRE_PARENTESE lista_parametros FECHA_PARENTESE corpo FIM
+     ID ABRE_PARENTESE lista_parametros FECHA_PARENTESE NEWLINE bloco FIM

  corpo ::=
-     corpo acao
+     corpo acao NEWLINE
      | vazio

  acao ::=
      expressao
+     | atribuicao
      | declaracao_variaveis | se | repita | leia | escreva | retorna | erro

  se ::=
-     SE expressao ENTAO corpo FIM
-     | SE expressao ENTAO corpo SENAO corpo FIM
+     SE expressao ENTAO bloco FIM
+     | SE expressao ENTAO bloco SENAO bloco FIM

  repita ::=
-     REPITA corpo ATE expressao
+     REPITA bloco ATE expressao

  atribuicao ::=
-     var ATRIBUICAO expressao
+     lista_expressoes ATRIBUICAO lista_expressoes
+     | lista_expressoes ATRIBUICAO atribuicao

  retorna ::=
-     RETORNA ABRE_PARENTESE expressao FECHA_PARENTESE
+     RETORNA ABRE_PARENTESE lista_expressoes FECHA_PARENTESE

  expressao ::=
      expressao_logica
-     | atribuicao

  fator ::=
      ABRE_PARENTESE expressao FECHA_PARENTESE | var | chamada_funcao | numero
+     | inicializacao_arranjo
+     | tupla
```

Nenhuma regra foi removida. Não mudaram: `programa`, `declaracao`, `lista_variaveis`, `var`, `indice`, `tipo`, `lista_parametros`, `parametro`, `leia`, `escreva`, as expressões (`expressao_logica` a `expressao_unaria`), os operadores, `numero`, `chamada_funcao` e `lista_argumentos`.

### Programas que mudam de comportamento

| Código | Antes | Agora |
|---|---|---|
| `{ comentário }` | comentário | tokens `ABRE_CHAVE`, ..., `FECHA_CHAVE`: escrever `{* comentário *}` |
| `x := y := 0` no escopo global | aceito | erro de sintaxe (dentro de funções continua aceito) |
| `x := 1 y := 2` na mesma linha | aceito | erro de sintaxe: um comando por linha |
| `se x > 0` e `então` na linha seguinte | aceito | erro de sintaxe: `então` na linha do `se` |
| `x := a` e `+ b` na linha seguinte | uma atribuição (`x := a + b`) | dois comandos: quebrar a linha depois do operador |
| `x := y` e `(a) := 1` na linha seguinte | erro de sintaxe: lido como `x := y(a) := 1` | dois comandos |
| `f() := 1`, `1 := x` dentro de funções | erro de sintaxe | aceito pelo parser; deve ser rejeitado na análise semântica |
| `inteiro: v[5] := {1, 2}`, `inteiro: a := b := 1` | erro de sintaxe | declaração com inicialização |

### Conflitos LALR(1)

| | Gramática original | Gramática nova |
|---|---|---|
| Gramática deste arquivo (sem regras `error`) | 5 shift/reduce, 0 reduce/reduce | **0** shift/reduce, **0** reduce/reduce |
| `ply_parser.py` (com regras `error` de recuperação) | 47 shift/reduce, 0 reduce/reduce | 13 shift/reduce, 0 reduce/reduce |

Os 5 conflitos da gramática original vinham da falta de separador entre comandos (`MAIS`/`MENOS` binário ou unário no início de um comando; `ID (` como variável seguida de parênteses ou chamada de função) e foram eliminados pelo `NEWLINE`. Os 13 que restam no `ply_parser.py` vêm todos das regras `p_cabecalho_error`, `p_se_error` e `p_repita_error`.

### Árvore sintática

- `atribuicao`: os filhos passaram de `(var, ATRIBUICAO, expressao)` para `(lista_expressoes, ATRIBUICAO, lista_expressoes)`, ou `(lista_expressoes, ATRIBUICAO, atribuicao)` no encadeamento, que aninha à direita.
- `inicializacao_variaveis`: deixou de ter um filho `atribuicao`; os filhos são `(lista_alvos, ATRIBUICAO, lista_expressoes)`, com `ABRE_PARENTESE` e `FECHA_PARENTESE` em volta de `lista_alvos` quando houver parênteses.
- `retorna`: o filho `expressao` virou `lista_expressoes`, mesmo com um único valor.
- `declaracao_funcao`: pode ter `tipos_retorno` no lugar de `tipo`.
- `fator`: pode ter `tupla` ou `inicializacao_arranjo` como filho.
- `declaracao_variaveis`: com inicialização, ganha os filhos `ATRIBUICAO` e `lista_expressoes` ou `atribuicao_encadeada`. Os filhos de `atribuicao_encadeada` são `(lista_alvos, ATRIBUICAO, lista_expressoes)`, ou `(lista_alvos, ATRIBUICAO, atribuicao_encadeada)` em cada elo seguinte; a `lista_alvos` tem uma única `var`.
- `bloco` e `NEWLINE` não aparecem na árvore: o `bloco` devolve um nó `corpo`, e a árvore continua tendo só nós `corpo`.

### Termos

O termo **`AugAssign`** refere-se a **atribuição aumentada** (*augmented assignment*), um conceito de programação (presente em linguagens como Python) que combina uma operação aritmética ou bit a bit com uma atribuição. [[1](https://hackage.haskell.org/package/hpython/docs/Language-Python-Syntax-AugAssign.html), [2](https://pylint.readthedocs.io/projects/astroid/en/v4.0.2/api/nodes/astroid.nodes.AugAssign.html)]

Exemplos comuns

- `x += 5` (equivalente a `x = x + 5`)
- `y -= 2` (equivalente a `y = y - 2`)
- `z *= 3` (equivalente a `z = z * 3`)
- `w <<= 8` (equivalente a `w = w << 8`) [[1](https://hackage.haskell.org/package/hpython/docs/Language-Python-Syntax-AugAssign.html)]
