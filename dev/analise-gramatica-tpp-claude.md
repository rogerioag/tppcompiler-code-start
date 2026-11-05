# Análise da gramática da linguagem TPP

*Conversa de 15/10/2026*

---

## Pergunta

Analise a gramática da linguagem TPP:

```
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
lista_argumentos  ::= lista_argumentos VIRGULA expressao
                      | expressao
                      | vazio
```

---

## Resposta

A gramática está bem estruturada no geral. A hierarquia de expressões é clássica e as recursões à esquerda servem bem a um gerador LR (PLY/yacc/bison). Pela análise, ela não tem ambiguidades nem conflitos LALR(1) óbvios: os pontos de decisão se resolvem com um token de lookahead. Os problemas reais estão em **linguagem aceita a mais ou a menos** e em algumas **inconsistências de projeto**. A análise não foi verificada com um gerador; vale confirmar com `bison -v` ou com o `parser.out` do PLY.

### 1. Problemas que aceitam programas inválidos

**`vazio` dentro de listas recursivas gera vírgula inicial.** Com `lista_parametros ::= lista_parametros VIRGULA parametro | ... | vazio`, a derivação `lista_parametros → vazio`, seguida de `, parametro`, aceita `f(, inteiro: a)`. O mesmo vale para `lista_argumentos`, que aceita `f(, x)`. A correção usual é separar o caso opcional:

```
cabecalho        ::= ID ABRE_PARENTESE parametros_opt FECHA_PARENTESE NEWLINE bloco FIM
parametros_opt   ::= lista_parametros | vazio
lista_parametros ::= lista_parametros VIRGULA parametro | parametro
```

Faça o mesmo com `argumentos_opt` / `lista_argumentos`.

**Lado esquerdo da atribuição é qualquer expressão.** `atribuicao ::= lista_expressoes ATRIBUICAO ...` aceita `1 + 2 := x` e `f(a) := 3`. Isso é uma escolha comum, que torna o parser mais simples, mas obriga uma verificação semântica de *l-value*. Também é inconsistente com o nível global, onde `inicializacao_variaveis` restringe o alvo a `lista_alvos`, ou seja, apenas `var`.

### 2. Problemas que rejeitam programas válidos

**Quebras de linha após `então`, `senão` e `repita`.** `corpo ::= corpo acao NEWLINE | vazio` exige uma ação antes de cada NEWLINE. O código típico é:

```
se a > b então
  x := 1
fim
```

Ele gera os tokens `SE expr ENTAO NEWLINE ID ...`, e esse NEWLINE logo após `ENTAO` não tem produção. O mesmo vale para `SENAO`, para `REPITA`, para linhas em branco ou só de comentário dentro de funções, e para linhas em branco entre declarações globais. Também falha um arquivo que não termine com NEWLINE. Ou o léxico colapsa e suprime esses NEWLINEs, o que é frágil, ou a gramática os absorve:

```
corpo ::= corpo acao NEWLINE
        | corpo NEWLINE
        | vazio
lista_declaracoes ::= lista_declaracoes declaracao NEWLINE
                    | lista_declaracoes NEWLINE
                    | declaracao NEWLINE
```

**`retorna` vazio.** Funções sem tipo (`declaracao_funcao ::= cabecalho`) são procedimentos, mas `retorna ( lista_expressoes )` não permite `retorna()`.

**`leia` e `escreva` têm aridade 1.** `leia(a, b)` e `escreva(x, y)` não são aceitos. Isso pode ser intencional.

### 3. Precedência e associatividade

| Nível (menor → maior) | Operadores | Associatividade |
|---|---|---|
| lógico | `e`, `ou` | esquerda, **mesmo nível** |
| relacional | `< > = <> <= >=` | esquerda (encadeável) |
| aditivo | `+ -` | esquerda |
| multiplicativo | `* /` | esquerda |
| unário | `+ - não` (sobre `fator`) | não recursivo |

Pontos a notar:

- **`e` e `ou` têm a mesma precedência**, então `a ou b e c` vira `(a ou b) e c`. Na maioria das linguagens, `e` liga mais forte. Para seguir a convenção, separe em dois níveis (`expressao_ou → expressao_e → expressao_simples`).
- **Relacionais encadeáveis:** `a < b < c` é sintaticamente válido, o que exige uma decisão semântica (erro de tipo ou comparação de booleano).
- **`não` só se aplica a `fator`**, então `não a > b` vira `(não a) > b`. É preciso escrever `não (a > b)`. Isso é coerente com C, mas vale documentar.
- **Unários não aninham:** `- -x` e `não não x` são rejeitados. Para aceitá-los, use `expressao_unaria ::= fator | operador_soma expressao_unaria | operador_negacao expressao_unaria`.

### 4. Pontos de decisão LR(1), que funcionam mas merecem atenção

- **Nível global:** depois de `tipo`, o token `:` leva a declaração e `ID` leva a função. Depois de `ID`, o token `(` leva a `cabecalho`; `[`, `,` ou `:=` levam a `var`. Depois de `(`, `ID` leva a `lista_alvos` e `INTEIRO`/`FLUTUANTE` levam a `tipos_retorno`. Tudo se resolve com um lookahead.
- **`acao ::= expressao` vs. `atribuicao`:** após `expressao`, NEWLINE/FIM reduz para `acao`, enquanto `,` ou `:=` reduz para `lista_expressoes`. Isso é OK.
- **Atribuição encadeada** (`a := b := c`): fica associativa à direita, sem conflito, porque `:=` não está no FOLLOW de `atribuicao`.
- **`tupla` vs. `( expressao )`:** decidido pela vírgula. `tupla` é apenas uma `lista_expressoes` com 2 ou mais elementos entre parênteses. Por isso `(a, b) := f()` funciona dentro de funções via `fator → tupla`, e no nível global via a segunda forma de `inicializacao_variaveis`. São duas rotas diferentes para a mesma coisa.
- **`bloco ::= corpo | corpo acao`:** a última ação pode vir sem NEWLINE antes de `FIM`, `SENAO` ou `ATE`. Funciona, mas se for adotado `corpo NEWLINE` (seção 2), essa alternativa passa a ser pouco necessária.

### 5. Questões semânticas que a gramática deixa abertas

- Tamanhos em `var ::= ID indice` são `expressao` arbitrárias em declarações. É preciso verificar se são constantes inteiras.
- `retorna` com múltiplos valores precisa ser confrontado com `tipos_retorno` (quantidade e tipos).
- O lado direito e o esquerdo de atribuições múltiplas precisam ter a mesma aridade, inclusive quando o lado direito é uma chamada que retorna tupla.
- Não é possível indexar o resultado de uma chamada (`f(x)[1]`) nem declarar um array vazio (`{}`). Ambos são aceitáveis, mas é bom saber.

### 6. Detalhe de implementação

`acao ::= erro`: em PLY/yacc, o token de recuperação se chama `error`. Se `erro` for um não-terminal ou token próprio, a recuperação de erros não acontece automaticamente. Normalmente se escreve algo como `acao ::= error NEWLINE` para ressincronizar no fim da linha.
