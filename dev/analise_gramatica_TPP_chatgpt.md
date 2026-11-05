# Análise da gramática da linguagem TPP

## Gramática fornecida

```text
programa ::= lista_declaracoes
lista_declaracoes ::= lista_declaracoes declaracao NEWLINE
                      | declaracao NEWLINE
declaracao ::= declaracao_variaveis
              | inicializacao_variaveis
              | declaracao_funcao
declaracao_variaveis ::= tipo DOIS_PONTOS lista_variaveis
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
          | inicializador_array
          | tupla
tupla ::= ABRE_PARENTESE lista_expressoes VIRGULA expressao FECHA_PARENTESE
inicializador_array ::= ABRE_CHAVE lista_expressoes FECHA_CHAVE
numero ::= NUM_INTEIRO
           | NUM_PONTO_FLUTUANTE
           | NUM_NOTACAO_CIENTIFICA
chamada_funcao ::= ID ABRE_PARENTESE lista_argumentos FECHA_PARENTESE
lista_argumentos ::= lista_argumentos VIRGULA expressao
                     | expressao
                     | vazio
```

## 1. Classificação da gramática

A gramática apresentada é uma **gramática livre de contexto (GLC)**, também chamada de gramática do tipo 2 na hierarquia de Chomsky.

Isso ocorre porque suas produções seguem, em geral, a forma:

\[
A \rightarrow \alpha
\]

Em que \(A\) é um único símbolo não terminal e \(\alpha\) é uma sequência de terminais e não terminais.

A gramática pode servir como base para construir um analisador sintático (*parser*) de uma linguagem imperativa com variáveis, funções, arrays, tuplas, expressões e estruturas de controle.

## 2. Organização sintática da linguagem

Podemos dividir a gramática em seis grupos principais.

| Grupo | Não terminais principais | Finalidade |
|---|---|---|
| Programa | `programa`, `lista_declaracoes` | Define a estrutura global |
| Declarações | `declaracao`, `tipo`, `var` | Declara variáveis e funções |
| Funções | `declaracao_funcao`, `cabecalho`, `parametro` | Define funções e parâmetros |
| Comandos | `acao`, `atribuicao`, `se`, `repita` | Define instruções executáveis |
| Expressões | `expressao`, `expressao_aditiva`, `fator` | Define operações e valores |
| Entrada e saída | `leia`, `escreva`, `retorna` | Define operações de entrada e saída |

Essa organização ajuda a separar os componentes sintáticos durante a implementação do compilador ou interpretador.

## 3. Análise das declarações

### 3.1. Declaração de variáveis

A regra:

```text
declaracao_variaveis ::= tipo DOIS_PONTOS lista_variaveis
```

permite declarações como:

```text
INTEIRO: a
INTEIRO: a, b, c
FLUTUANTE: x, y
```

O não terminal `lista_variaveis` é recursivo à esquerda:

```text
lista_variaveis ::= lista_variaveis VIRGULA var
                    | var
```

Isso permite reconhecer listas de tamanho arbitrário. A recursão à esquerda é adequada para parsers LR, como LALR(1), mas precisa ser eliminada ou tratada especialmente em parsers descendentes recursivos tradicionais, como LL(1).

### 3.2. Variáveis indexadas

As produções:

```text
var ::= ID
        | ID indice

indice ::= indice ABRE_COLCHETE expressao FECHA_COLCHETE
          | ABRE_COLCHETE expressao FECHA_COLCHETE
```

permitem representar variáveis simples e acessos indexados:

```text
a
vetor[i]
matriz[i][j]
tensor[i][j][k]
```

A recursividade de `indice` permite encadear vários índices e usar expressões como `matriz[i + 1][j * 2]`.

Uma alternativa mais explícita seria:

```text
var ::= ID lista_indices
lista_indices ::= lista_indices ABRE_COLCHETE expressao FECHA_COLCHETE
                  | vazio
```

Essa versão expressa diretamente que uma variável é um identificador seguido por zero ou mais índices.

### 3.3. Declarações de funções

A gramática contém:

```text
declaracao_funcao ::= tipo cabecalho
                      | tipos_retorno cabecalho
                      | cabecalho
```

Isso sugere três formas de declaração: funções com um tipo de retorno, funções com vários tipos de retorno e funções sem tipo de retorno explicitamente declarado.

A gramática permite vários tipos de retorno por meio de `tipos_retorno`, mas não estabelece regras de compatibilidade entre os valores retornados e os tipos declarados. Isso pertence à análise semântica.

## 4. Análise dos parâmetros de funções

A produção apresentada é:

```text
parametro ::= tipo DOIS_PONTOS ID
              | parametro ABRE_COLCHETE FECHA_COLCHETE
```

A primeira alternativa define um parâmetro tipado, como `INTEIRO: n`. A segunda permite adicionar pares de colchetes vazios, potencialmente representando arrays, como `INTEIRO: vetor[]` ou `INTEIRO: matriz[][]`.

Uma alternativa mais explícita seria:

```text
parametro ::= tipo DOIS_PONTOS ID dimensoes
dimensoes ::= dimensoes ABRE_COLCHETE FECHA_COLCHETE
              | vazio
```

Essa reformulação separa o tipo básico do número de dimensões.

## 5. Análise dos blocos e comandos

### 5.1. Estrutura dos blocos

As regras relevantes são:

```text
bloco ::= corpo
          | corpo acao

corpo ::= corpo acao NEWLINE
          | vazio
```

A produção de `corpo` permite zero ou mais comandos terminados por `NEWLINE`. Entretanto, `bloco` permite acrescentar uma ação depois do corpo, sem exigir um `NEWLINE` explícito entre ela e o restante da estrutura.

Isso pode ser intencional se `FIM`, `SENAO` e `ATE` forem delimitadores reconhecidos pelo parser, mas torna a estrutura de término dos blocos menos uniforme.

Uma versão conceitualmente mais simples seria:

```text
bloco ::= lista_acoes
lista_acoes ::= lista_acoes acao NEWLINE
                | vazio
```

Essa proposta precisa ser ajustada se a linguagem permitir comandos finais sem quebra de linha ou se `SENAO`, `FIM` e `ATE` tiverem regras específicas de delimitação.

### 5.2. Estrutura condicional

A gramática define:

```text
se ::= SE expressao ENTAO bloco FIM
       | SE expressao ENTAO bloco SENAO bloco FIM
```

Ela permite condicionais com e sem alternativa. O uso explícito de `FIM` evita a ambiguidade clássica do *dangling else* — determinar a qual `SE` pertence um `SENAO` — desde que a estrutura dos blocos seja reconhecida de maneira consistente.

### 5.3. Laço de repetição

A regra:

```text
repita ::= REPITA bloco ATE expressao
```

representa um laço cuja condição é verificada ao final da execução do bloco, semelhante a um laço *repeat-until*. Em geral, esse tipo de laço executa o corpo pelo menos uma vez. A semântica exata depende de `ATE` indicar encerramento ou continuação.

## 6. Análise das expressões e precedência de operadores

A hierarquia das produções é:

1. `expressao_logica`: operadores `E` e `OU`.
2. `expressao_simples`: operadores relacionais.
3. `expressao_aditiva`: adição e subtração.
4. `expressao_multiplicativa`: multiplicação e divisão.
5. `expressao_unaria`: sinais unários e negação lógica.
6. `fator`: literais, variáveis, chamadas, tuplas e arrays.

Essa hierarquia define uma precedência relativa: quanto mais próximo de `fator`, maior a precedência das operações representadas nesse nível.

Por exemplo, `a + b * c` é estruturado como `a + (b * c)`, porque a multiplicação pertence a um nível mais interno que a adição.

Da mesma forma, `a < b + c` é estruturado como `a < (b + c)`.

### 6.1. Associatividade

As produções de adição e multiplicação usam recursão à esquerda. Assim:

```text
a - b - c
```

é estruturado como:

```text
(a - b) - c
```

E:

```text
a / b / c
```

é estruturado como:

```text
(a / b) / c
```

Isso é apropriado para operadores aritméticos normalmente definidos como associativos à esquerda.

### 6.2. Problema na expressão unária

A gramática apresenta:

```text
expressao_unaria ::= fator
                     | operador_soma fator
                     | operador_negacao fator
```

Como as alternativas de sinal unário e negação são seguidas diretamente por `fator`, a gramática não permite, em geral, encadear operadores unários. Por exemplo, `--x` e `NAO NAO condicao` não são reconhecidos por essa estrutura.

Uma alternativa mais flexível é:

```text
expressao_unaria ::= fator
                     | operador_soma expressao_unaria
                     | operador_negacao expressao_unaria
```

Isso permite encadeamento de operadores unários. A aceitação de sequências específicas ainda depende das regras léxicas e das restrições semânticas.

### 6.3. Precedência entre `E` e `OU`

A gramática usa um único não terminal para ambos:

```text
expressao_logica ::= expressao_simples
                     | expressao_logica operador_logico expressao_simples

operador_logico ::= E
                    | OU
```

Isso atribui a `E` e `OU` o mesmo nível sintático de precedência. Uma expressão como:

```text
a OU b E c
```

será estruturada à esquerda, de forma equivalente a:

```text
(a OU b) E c
```

Se a intenção for que `E` tenha precedência maior que `OU`, será necessário separar os níveis:

```text
expressao_logica ::= expressao_logica OU expressao_conjuncao
                     | expressao_conjuncao

expressao_conjuncao ::= expressao_conjuncao E expressao_simples
                        | expressao_simples
```

Essa alteração é importante porque a precedência afeta o significado das expressões.

## 7. Problemas e inconsistências encontrados

| Problema | Consequência | Recomendação |
|---|---|---|
| Atribuição usa `lista_expressoes` à esquerda | Permite expressões que não são variáveis como destinos de atribuição | Usar `lista_alvos ATRIBUICAO lista_expressoes` |
| `expressao_unaria` termina em `fator` | Limita o encadeamento de operadores unários | Permitir recursão sobre `expressao_unaria` |
| `E` e `OU` têm a mesma precedência | Pode produzir agrupamentos diferentes dos pretendidos | Separar conjunção e disjunção em níveis distintos, se necessário |
| `tupla` exige uma vírgula e pelo menos dois elementos | Não permite tuplas unitárias nem vazias | Confirmar se essa restrição é intencional |
| `leia` recebe apenas um `var` | Não permite uma lista de variáveis em uma única chamada | Usar `lista_alvos`, se a linguagem exigir leitura múltipla |
| `escreva` recebe apenas uma expressão | Não permite vários argumentos de saída | Usar `lista_expressoes`, se desejado |
| `cabecalho` exige `lista_parametros` | A produção precisa que `vazio` seja reconhecido dentro dessa lista | Definir formalmente `vazio` como produção ε |
| `bloco` e `corpo` têm regras distintas para comandos finais | Pode dificultar a previsibilidade dos terminadores | Uniformizar a estrutura dos blocos |

### 7.1. O problema mais importante: atribuição

A regra atual é:

```text
atribuicao ::= lista_expressoes ATRIBUICAO lista_expressoes
               | lista_expressoes ATRIBUICAO atribuicao
```

Ela permite construções potencialmente inválidas como:

```text
a + b := c
```

Isso acontece porque `lista_expressoes` pode conter qualquer expressão, inclusive uma expressão aritmética, e não apenas identificadores ou acessos indexados.

Além disso, a recursão à direita permite atribuições encadeadas, como `a := b := c`. A aceitação dessa forma pode ser intencional, mas deve estar definida na especificação da linguagem.

Uma versão mais consistente seria:

```text
atribuicao ::= lista_alvos ATRIBUICAO lista_expressoes
               | lista_alvos ATRIBUICAO atribuicao
```

Assim, os destinos da atribuição são limitados a variáveis. Ainda é necessário definir se a quantidade de alvos deve coincidir com a quantidade de expressões e como funciona a atribuição múltipla.

### 7.2. O símbolo `vazio`

A gramática usa `vazio` em `lista_parametros`, `corpo` e `lista_argumentos`. É necessário definir se `vazio` representa a cadeia vazia, normalmente escrita como ε, ou se representa um token real.

Se for a cadeia vazia, as regras podem ser escritas com `ε`. Isso permite funções sem parâmetros e blocos vazios. A distinção é fundamental para a implementação do analisador sintático.

## 8. Possíveis ambiguidades

Uma gramática livre de contexto não é necessariamente ambígua. Algumas produções da TPP merecem análise específica.

### 8.1. Atribuições encadeadas

A produção recursiva à direita de `atribuicao` define uma estrutura associativa à direita para atribuições encadeadas. O problema principal não é necessariamente uma ambiguidade, mas a permissividade do lado esquerdo.

### 8.2. Expressões lógicas

Como `E` e `OU` compartilham o mesmo nível de precedência, a gramática determina uma associação à esquerda, mas não representa uma precedência distinta entre os dois operadores. Isso é uma questão de especificação sintática e semântica, mesmo que a gramática seja não ambígua nesse trecho.

### 8.3. Chamadas de função e variáveis

As regras:

```text
fator ::= ABRE_PARENTESE expressao FECHA_PARENTESE
          | var
          | chamada_funcao
          | numero
          | inicializador_array
          | tupla
```

e:

```text
chamada_funcao ::= ID ABRE_PARENTESE lista_argumentos FECHA_PARENTESE
```

podem ser distinguidas pelo token seguinte ao identificador: um colchete indica indexação, enquanto um parêntese indica uma chamada. Isso tende a ser tratável pelo parser, desde que os tokens e as produções estejam definidos corretamente.

**Conclusão sobre ambiguidades:** não é possível afirmar que toda a gramática é não ambígua apenas pela inspeção dos trechos. Uma verificação rigorosa exigiria analisar os conjuntos FIRST/FOLLOW ou os estados do parser, dependendo da estratégia de análise sintática adotada.

## 9. Recursão à esquerda e implementação do parser

A gramática utiliza recursão à esquerda em produções como:

```text
lista_declaracoes ::= lista_declaracoes declaracao NEWLINE
```

```text
lista_variaveis ::= lista_variaveis VIRGULA var
```

```text
expressao_aditiva ::= expressao_aditiva operador_soma expressao_multiplicativa
```

```text
expressao_multiplicativa ::= expressao_multiplicativa operador_multiplicacao expressao_unaria
```

Isso não é necessariamente um defeito. A adequação depende do tipo de parser utilizado.

| Tipo de parser | Compatibilidade com recursão à esquerda |
|---|---|
| LR(0) | Pode suportá-la, dependendo da gramática |
| SLR(1) | Pode suportá-la, dependendo da gramática |
| LALR(1) | Geralmente apropriado para esse estilo de gramática |
| LR(1) | Pode suportá-la, dependendo da gramática |
| LL(1) | Não aceita diretamente recursão à esquerda |
| Descendente recursivo tradicional | Precisa eliminar ou tratar a recursão à esquerda |

Se a implementação for feita com ferramentas como Yacc ou Bison, a recursão à esquerda é normalmente natural para listas e expressões. Se for utilizado um parser LL(1) ou descendente recursivo sem tratamento específico, serão necessárias transformações.

## 10. Recomendações de melhoria

Antes de implementar o parser, recomenda-se priorizar estas alterações:

1. **Corrigir a atribuição:** substituir `lista_expressoes` por `lista_alvos` no lado esquerdo.
2. **Revisar os operadores unários:** permitir recursão em `expressao_unaria`.
3. **Definir a precedência lógica:** decidir explicitamente se `E` precede `OU`.
4. **Uniformizar os blocos:** estabelecer uma convenção consistente para `NEWLINE`, `FIM` e `ATE`.
5. **Formalizar ε:** especificar claramente que `vazio` representa a cadeia vazia, caso essa seja a intenção.
6. **Definir as regras de tuplas e entrada/saída:** confirmar se tuplas unitárias, leitura de várias variáveis e escrita de várias expressões são permitidas.
7. **Separar sintaxe e semântica:** verificar tipos, declaração de identificadores, número de valores retornados e compatibilidade das atribuições em uma etapa semântica posterior.

## Conclusão

A gramática da TPP apresenta uma estrutura geral coerente para uma linguagem imperativa e utiliza adequadamente a recursão para representar listas, expressões e comandos. Sua hierarquia de expressões é uma boa base para estabelecer precedência de operadores.

Os pontos mais relevantes a revisar são a permissividade da atribuição, a precedência lógica, o tratamento de operadores unários e a uniformidade dos blocos. A escolha do algoritmo de análise sintática também é determinante, especialmente devido à presença de recursão à esquerda.

Com esses ajustes, a gramática poderá servir como uma especificação mais precisa para o desenvolvimento de um analisador sintático e para as etapas posteriores de um compilador ou interpretador da linguagem TPP.
