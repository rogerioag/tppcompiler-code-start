# Registro de Análise da Gramática TPP

## 1. Entrada do Usuário (Gramática TPP)

```bnf
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

## 2. Análise da Gramática da Linguagem TPP

A gramática apresentada define a linguagem **TPP** (*Tpp Programming Language*), uma linguagem imperativa, procedural e fortemente estruturada, comumente utilizada no ensino de Compiladores e Teoria das Linguagens Formais no Brasil.

---

### 1. Classificação e Tipo de Analisador Sintático

* **Gramática Livre de Contexto (GLC / Tipo 2):** A gramática é estruturada em Notação Backus-Naur (BNF).
* **Recursão à Esquerda:** Quase todas as produções encadeadas (como `lista_declaracoes`, `lista_variaveis`, `expressao_logica`, `expressao_aditiva`) usam recursão à esquerda.
* **Compatibilidade:** Adequada para analisadores sintáticos ascendentes (*Bottom-Up*), especificamente geradores da família **LR / LALR(1)** (como Yacc, Bison e PLY/Python Lex-Yacc). Para uso em analisadores descendentes (*Top-Down* / LL(1) ou Recursivo Descendente), é necessário refatorar a gramática para eliminar a recursão à esquerda e realizar a fatoração.

---

### 2. Estrutura Global e Declarativa

#### Programa e Bloco Principal
* Um **`programa`** é constituído por uma lista de declarações globais separadas por quebra de linha (`NEWLINE`).
* As declarações globais podem ser:
  1. Declaração de variáveis (`tipo : lista_variaveis`).
  2. Inicialização direta de variáveis (`lista_alvos := lista_expressoes`).
  3. Declaração de funções.

#### Tipos e Variáveis
* **Tipos Suportados:** `INTEIRO` e `FLUTUANTE`.
* **Variáveis e Vetores:** Suporta variáveis escalares (`ID`) e arrays multidimensionais (`ID[exp][exp]...`), construídos recursivamente pela regra `indice`.
* **Atribuição e Tuplas:** Permite atribuições simples e múltiplas em paralelo (`a, b := 1, 2` ou `(a, b) := 1, 2`).

---

### 3. Funções e Procedimentos

* **Tipos de Retorno:**
  * **Retorno Simples:** `inteiro func(...)`
  * **Retorno Múltiplo / Tupla de Tipos:** `(inteiro, flutuante) func(...)`
  * **Procedimento (Void):** Cabeçalho direto sem tipo prefixado (`func(...)`).
* **Parâmetros:** Aceita múltiplos parâmetros tipados (`inteiro: x`), parâmetros de array/matriz (`inteiro: arr[][]`), ou lista vazia (`vazio`).
* **Delimitação do Corpo:** A função inicia após o `NEWLINE` do cabeçalho e encerra estritamente na palavra reservada `FIM`.

---

### 4. Hierarquia de Operadores e Precedência

A precedência dos operadores é definida pela profundidade na árvore de derivação, da menor para a maior precedência:

| Nível de Precedência | Categoria | Operadores | Associatividade |
| :--- | :--- | :--- | :--- |
| **1 (Mais baixa)** | Lógica | `E`, `OU` | À esquerda |
| **2** | Relacional | `<`, `>`, `=`, `!=`, `<=`, `>=` | À esquerda |
| **3** | Aditiva | `+`, `-` | À esquerda |
| **4** | Multiplicativa | `*`, `/` | À esquerda |
| **5** | Unária | `+` (unário), `-` (unário), `NAO` | À direita |
| **6 (Mais alta)** | Primária / Fator | Identificadores, Números, Chamadas de Função, `(expressao)`, Tuplas, `{arrays}` | N/A |

---

### 5. Estruturas de Controle e I/O

* **Condicional (`se`):**
  * `SE expressao ENTAO bloco FIM`
  * `SE expressao ENTAO bloco SENAO bloco FIM`
  * *Resolução do Dangling Else:* A sintaxe elimina o problema do "else ambíguo" ao exigir explicitamente o token `FIM` para delimitar cada bloco `se`.
* **Laço de Repetição (`repita`):**
  * `REPITA bloco ATE expressao` (estrutura *do-while* / *repeat-until*).
* **Entrada e Saída / Retorno:**
  * `leia(var)`
  * `escreva(expressao)`
  * `retorna(lista_expressoes)`

---

### 6. Peculiaridades e Pontos de Atenção na Gramática

* **Igualdade de Precedência Lógica (`E` e `OU`):**
  A regra `expressao_logica ::= expressao_logica operador_logico expressao_simples` coloca os operadores `E` e `OU` no mesmo nível de precedência. Em linguagens convencionais (como C, Java ou Python), o `E` possui precedência maior que o `OU`.
* **Diferenciação entre Expressão Parentesiada e Tupla:**
  A gramática evita ambiguidade entre `(exp)` e uma tupla `(exp1, exp2)` exigindo explicitamente uma vírgula na produção da tupla:
  `tupla ::= ABRE_PARENTESE lista_expressoes VIRGULA expressao FECHA_PARENTESE`. Isso garante que uma tupla tenha no mínimo dois elementos.
* **Flexibilidade na Atribuição Encadeada:**
  A regra `atribuicao ::= lista_expressoes ATRIBUICAO atribuicao` permite encadeamentos do tipo `a := b := 10`.
* **Tratamento do Token `vazio`:**
  O não-terminal `vazio` funciona como a produção nula ($\epsilon$), representando ausência de elementos em listas de parâmetros, argumentos ou no início de corpos de blocos.