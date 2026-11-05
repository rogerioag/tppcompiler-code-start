# Extensões da Gramática TPP (v1.1): Atribuição e Retorno Múltiplos, Arrays, NEWLINE e Divisão do Parser

**Data:** 13 a 15 de Outubro de 2026  
**Projeto:** `tppcompiler-code-start` / Compilador TPP  
**Ambiente:** Linux / Python 3.14 / PLY 3.11 / anytree / Pytest  

---

## Sumário
1. [Visão Geral e Objetivos da Sessão](#1-visão-geral-e-objetivos-da-sessão)
2. [Leitura da Conversa com o Gemini](#2-leitura-da-conversa-com-o-gemini)
3. [Método de Verificação da Gramática](#3-método-de-verificação-da-gramática)
4. [Comentários `{* *}` e Tokens `ABRE_CHAVE`/`FECHA_CHAVE`](#4-comentários---e-tokens-abre_chavefecha_chave)
5. [Atribuição Múltipla, Retorno Múltiplo e Inicialização de Arrays](#5-atribuição-múltipla-retorno-múltiplo-e-inicialização-de-arrays)
6. [Atribuição Encadeada no Estilo do Python](#6-atribuição-encadeada-no-estilo-do-python)
7. [Parênteses nos Alvos, Tuplas e o Token `NEWLINE`](#7-parênteses-nos-alvos-tuplas-e-o-token-newline)
8. [Etapas da CLI do Compilador](#8-etapas-da-cli-do-compilador)
9. [Padrão dos Nós da Árvore Sintática](#9-padrão-dos-nós-da-árvore-sintática)
10. [Registro de Mudanças na `grammar.md`](#10-registro-de-mudanças-na-grammarmd)
11. [`tppparser_test.py` no Formato do `tpplex_test.py`](#11-tppparser_testpy-no-formato-do-tpplex_testpy)
12. [Verificação dos 17 Casos de Atribuição Múltipla](#12-verificação-dos-17-casos-de-atribuição-múltipla)
13. [Avaliação das Análises do Gemini, ChatGPT e Claude](#13-avaliação-das-análises-do-gemini-chatgpt-e-claude)
14. [Divisão do `ply_parser` em Módulos por Categoria](#14-divisão-do-ply_parser-em-módulos-por-categoria)
15. [Arquivos Criados e Alterados](#15-arquivos-criados-e-alterados)
16. [Pendências e Decisões em Aberto](#16-pendências-e-decisões-em-aberto)

---

## 1. Visão Geral e Objetivos da Sessão

A sessão partiu de uma conversa com o Gemini sobre a BNF do TPP e evoluiu para a versão 1.1 da gramática. Os objetivos foram:

- permitir **atribuição múltipla** (`a, b := 1, 2`, `(a, b) := f(x)`), **retorno múltiplo** (`(inteiro, flutuante) f(...)` e `retorna(a, b)`) e **inicialização de arrays** (`A := {1, 2, 3}`);
- manter a gramática **LALR(1)** e verificar cada decisão com o gerador do PLY, e não só por inspeção;
- ajustar a CLI para executar apenas as etapas pedidas;
- reorganizar o parser em módulos por categoria, como no `cmmcompiler`.

Toda alteração foi validada comparando a saída de todos os `.tpp` de teste (`tests/lex-tests` e `tests/syn-tests`) antes e depois, com os 6 analisadores léxicos.

---

## 2. Leitura da Conversa com o Gemini

O link compartilhado (`https://share.gemini.google/fv1R13E9cMIO`) carrega a conversa por JavaScript, então o conteúdo foi obtido pelo endpoint interno do Gemini (`batchexecute`, RPC `ujx1Bf`). A transcrição foi salva em [conversa_gemini_bnf_exemplos_e_retorno_multiplo.md](conversa_gemini_bnf_exemplos_e_retorno_multiplo.md).

A conversa tratava de exemplos de código a partir da BNF, de retorno múltiplo (na gramática e em LLVM IR, com `insertvalue`/`extractvalue`) e de atribuição múltipla com parênteses opcionais. Problemas encontrados nas respostas do Gemini:

- usou `=` para atribuição e `==` para igualdade; no TPP, `ATRIBUICAO` é `:=` e `IGUAL` é `=`;
- o laço `REPITA … ATE i > 1` do fatorial termina na primeira iteração (o correto seria `ATE i <= 1`);
- não apontou os conflitos de parser causados pela falta de separador entre comandos.

---

## 3. Método de Verificação da Gramática

Para não depender de inspeção, foi usado um verificador (script temporário) que lê o bloco EBNF da `grammar.md`, aplica variantes das regras e gera as tabelas LALR(1) com o PLY, contando os conflitos shift/reduce (S/R) e reduce/reduce (R/R). O parser real (`ply_parser.py`) também foi medido, com as regras de recuperação de erro (`error`).

| Situação | Gramática pura | `ply_parser.py` (com regras `error`) |
|---|---|---|
| Gramática original (v1.0) | 5 S/R, 0 R/R | 47 S/R, 0 R/R |
| Primeira versão das extensões (seção 5) | 5 S/R, 0 R/R | 51 S/R, 0 R/R |
| Versão final com `NEWLINE` (seção 7) | **0 S/R, 0 R/R** | **13 S/R, 0 R/R** |

Os 5 conflitos da v1.0 vinham da falta de separador entre comandos: `MAIS`/`MENOS` binário ou unário no início de um comando, e `ID (` como variável seguida de parênteses ou chamada de função. Os 13 que restam no parser vêm todos das regras `p_cabecalho_error`, `p_se_error` e `p_repita_error`.

---

## 4. Comentários `{* *}` e Tokens `ABRE_CHAVE`/`FECHA_CHAVE`

No lexer original, `{ … }` era comentário, então `A := {1,2,3}` seria descartado. Decisão: **`{ }` para inicializar arrays e `{* *}` para comentários**.

- **Lexers alterados:** os 4 que têm código próprio (`ply`, `mandfa`, `symtable`, `automatalib`); `symtableman` e `automatalibman` herdam do `mandfa`.
- **Tokens novos:** `ABRE_CHAVE` (`{`) e `FECHA_CHAVE` (`}`).
- **Comentário:** `* }` com espaço não fecha o comentário; `{*` sem `*}` continua gerando `ERR-LEX-UNC-COMMENT`; a contagem de linhas é mantida.
- **Testes:** os comentários de todos os `.tpp` de `tests/` e do gerador do benchmark (`tests/benchmark_lexers.py`) foram convertidos para `{* *}`.
- **Documentação:** [docs/LEX-SPECS.md](docs/LEX-SPECS.md) e `src/tpplexer/README (1).md`.

**Validação:** as 384 saídas (6 lexers × 64 arquivos) ficaram idênticas às de antes da troca.

Observação: em `lex-test-021.tpp`, a linha `inteiro v[5] := {1,2,3,4,5}` era uma tentativa de inicializar array que o lexer antigo tratava como comentário. A conversão automática a transformou em `{*1,2,3,4,5*}`, preservando a saída esperada do lexer.

---

## 5. Atribuição Múltipla, Retorno Múltiplo e Inicialização de Arrays

Primeira versão das extensões, testada variante por variante:

| Variante | S/R | R/R |
|---|---|---|
| Gramática original | 5 | 0 |
| + retorno múltiplo | 5 | 0 |
| + atribuição múltipla, com `atribuicao` ainda dentro de `expressao` | 6 | **1** |
| + atribuição múltipla, com `atribuicao` só como comando | 5 | 0 |
| + parênteses nos alvos, `(a, b) := …` | 5 | **1** |
| + array com `{ … }` | 5 | 0 |
| + array com `[ … ]` | **8** | 0 |

Decisões:

- **`atribuicao` deixou de ser `expressao`** e passou a ser um comando (`acao`).
- **Arrays com `{ }`:** `[ ]` geraria 3 conflitos novos (`x := a` seguido de `[1,2]` seria lido como indexação de `a`).
- **Regras novas:** `tipos_retorno`, `lista_tipos`, `lista_alvos`, `lista_expressoes` e `inicializador_array`.

---

## 6. Atribuição Encadeada no Estilo do Python

A primeira versão rejeitava `a[i] := b := 0`, usado em `syn-test-015.tpp`. As formas de encadeamento com `lista_alvos` no lado esquerdo geraram conflitos:

| Variante | S/R | R/R |
|---|---|---|
| `lista_alvos ATRIBUICAO lista_expressoes \| lista_alvos ATRIBUICAO atribuicao` | 5 | **1** |
| `… \| var ATRIBUICAO atribuicao` | **7** | 0 |
| cadeia de alvos à esquerda | 5 | **1** |

A causa: em `a := b, …`, com a `,` à frente, o parser não sabe se `b` é mais um alvo ou um valor.

**Como o Python resolve**, verificado no Python 3.14: o encadeamento faz parte da regra do comando (`(target_list "=")+ expressão`); o lado esquerdo é lido como uma expressão comum e depois validado. Por isso `f() = 1` dá `SyntaxError: cannot assign to function call`. O lado direito é avaliado uma vez só e os alvos recebem o valor da esquerda para a direita (`i = a[i] = 1` grava em `a[1]`).

**Solução adotada:**

```ebnf
inicializacao_variaveis ::= lista_alvos ATRIBUICAO lista_expressoes        { escopo global }
atribuicao ::= lista_expressoes ATRIBUICAO lista_expressoes                { dentro das funções }
             | lista_expressoes ATRIBUICAO atribuicao
```

- **Dentro das funções**, o lado esquerdo é `lista_expressoes` e a análise semântica verifica se cada alvo é uma `var`. Com isso, `a := b := 0` e `a, b := c, d := 1, 2` são aceitos.
- **No escopo global**, os alvos continuam sendo `lista_alvos`, sem encadeamento. Com expressões no lado esquerdo, `f()` no topo do arquivo seria ambíguo entre uma chamada e o cabeçalho de uma função sem parâmetros (2 R/R).

---

## 7. Parênteses nos Alvos, Tuplas e o Token `NEWLINE`

### 7.1. Parênteses no estilo do Python

No Python, `(a, b) = 1, 2` não tem regra especial: `(a, b)` é uma tupla, que depois é convertida em alvo. No TPP, isso foi feito com uma regra `tupla` no `fator`:

| Variante | S/R | R/R |
|---|---|---|
| Gramática atual | 5 | 0 |
| `tupla ::= ( lista_expressoes , expressao )` no `fator` | 5 | 0 |
| tupla + `( lista_alvos )` no escopo global | 5 | 0 |
| parênteses só na `atribuicao`, sem tupla | **6** | 0 |

O problema restante era silencioso: sem separador entre comandos, `x := y` seguido de `(a, b) := 1, 2` na linha de baixo seria lido como `x := y(a, b) := 1, 2`.

### 7.2. `NEWLINE` como terminador

Um levantamento nos programas de teste mostrou que eles são organizados por linha: cada comando termina no fim da linha. A única exceção relevante é `se res = 0 então primo := 0 fim` (`lex-test-028.tpp`).

| Variante (com tupla e parênteses) | S/R | R/R |
|---|---|---|
| sem `NEWLINE` | 5 | 0 |
| `NEWLINE` opcional, como separador | 5 | 0 |
| `NEWLINE` obrigatório no fim de cada comando | **0** | **0** |
| obrigatório, mas dispensável no último comando antes de `fim`/`senão`/`até` | **0** | **0** |

Foi adotada a última, no estilo da inserção automática de `;` do Go, e não no estilo do Python:

- **`NewlineFilter`**, entre o lexer e o parser, insere `NEWLINE` numa quebra de linha quando o último token da linha é `ID`, número, `)`, `]`, `}` ou `fim` e a quebra não está dentro de `()`, `[]` ou `{}`. Também insere um `NEWLINE` no fim da entrada.
- **Os lexers não mudaram:** `NEWLINE` é um token só do parser, então os `.lex.out` e a especificação léxica continuam válidos.
- **Regra `bloco ::= corpo | corpo acao`:** permite que o último comando de um bloco dispense o `NEWLINE`. Na árvore, o `bloco` não aparece: ele devolve um nó `corpo`.

Consequências para quem escreve TPP:

- um comando por linha, exceto o último de um bloco;
- uma expressão só continua na linha seguinte depois de um operador ou `,`, ou dentro de `()`, `[]` e `{}`;
- `se condição` precisa ter o `então` na mesma linha.

**Validação:** nenhum programa válido dos testes foi rejeitado por causa do `NEWLINE`. Os 43 arquivos rejeitados foram examinados pela linha do primeiro erro, e todos têm erros reais (`se` sem `então`, `retorna j`, `até n == 0`, falta de `fim` etc.).

---

## 8. Etapas da CLI do Compilador

A CLI ([src/tpp_compiler.py](src/tpp_compiler.py)) executava o parser mesmo com `--lexer`. Agora ela executa até a etapa mais avançada pedida:

| Comando | O que executa |
|---|---|
| `tpp_compiler.py arq.tpp` ou `--lexer X arq.tpp` | só a análise léxica (imprime os tokens) |
| `--parser Y` | léxica e sintática |
| `--sema Z` | léxica, sintática e semântica |
| `--gencode W` | todas as etapas |

- **Estratégias:** cada opção passada substitui a padrão (`ply`, `yacc`, `sema`, `llvm`). Com `--parser yacc --lexer mandfa`, o parser usa o lexer `mandfa`; antes, ele usava sempre o PLY.
- **Tokens:** a partir do `--parser`, não são impressos; o parser pede os tokens ao lexer conforme precisa.
- **Mensagens de uso e de arquivo:** com `--parser`, usam as chaves `ERR-SYN-*`; nos outros casos, `ERR-GLOB-*`.
- **`--sema` e `--gencode`:** ainda não implementados; executam as etapas anteriores e avisam no stderr.

**Validação:** os testes do lexer passam (252, com os 6 lexers), e o parser dá a mesma saída com qualquer um dos 6 lexers.

---

## 9. Padrão dos Nós da Árvore Sintática

As regras novas seguem o padrão do `ply_parser`:

- cada não-terminal vira um nó com `name` igual ao nome da regra e `type` em maiúsculas;
- cada terminal vira um nó com o nome do token e um filho `SIMBOLO` com o lexema, e o resultado é atribuído de volta a `p[i]`;
- os filhos são ligados na ordem da produção.

Foi corrigido um desvio no `p_inicializacao_variaveis`, que não atribuía o nó `ATRIBUICAO` de volta a `p[2]`/`p[4]`.

Formas importantes para a análise semântica:

- `atribuicao`: `(lista_expressoes, ATRIBUICAO, lista_expressoes)`, ou `(lista_expressoes, ATRIBUICAO, atribuicao)` no encadeamento, que aninha à direita;
- `tupla`: `(ABRE_PARENTESE, lista_expressoes, VIRGULA, expressao, FECHA_PARENTESE)`; o último elemento fica fora da lista.

---

## 10. Registro de Mudanças na `grammar.md`

A `grammar.md` (agora em [docs/grammar/grammar.md](docs/grammar/grammar.md)) recebeu a seção "Registro de mudanças em relação à gramática original", com:

- tokens novos (`ABRE_CHAVE`, `FECHA_CHAVE`, `NEWLINE`);
- 7 regras novas e 12 regras alteradas, em blocos `diff` (nenhuma removida); a lista foi conferida por script contra a gramática original;
- uma tabela de programas que mudam de comportamento, conferida no parser;
- os conflitos LALR(1) e as mudanças na árvore sintática.

---

## 11. `tppparser_test.py` no Formato do `tpplex_test.py`

O [tests/tppparser_test.py](tests/tppparser_test.py) não era coletado. Correções:

- opção `--parser` no [tests/conftest.py](tests/conftest.py) (`yacc`, `topdown` ou `all`; padrão `yacc`);
- a lista de estratégias de `all` usava os nomes dos lexers; agora tem só `yacc`;
- a função de teste recebia `lexer_type`; agora recebe `parser_type`;
- os casos passam a vir de `tests/syn-tests/`, com o comando `python src/tpp_compiler.py --parser <estratégia> -k <arquivo>`.

**Resultado:** 12 passam e 16 falham. As falhas vêm das saídas esperadas, e não do formato do teste: o `PLYParser.parse` só imprime `WAR-SYN-ANA-SUCCESS` com `-t`, e alguns `.syn.out` esperam mensagens que a recuperação de erros atual não produz.

---

## 12. Verificação dos 17 Casos de Atribuição Múltipla

Os 17 casos da seção "Alterações" da `grammar.md` (`a := 1`, `a,b := c,1`, `(a,b) := (c+d,3+4)`, `(a,b) := funct(x, y)` etc.) foram testados dentro de uma função e no escopo global. **Todos são aceitos nos dois contextos.**

Formas com o mesmo significado geram árvores diferentes:

| Caso | Dentro de função | No escopo global |
|---|---|---|
| `(a,b) := 1,2` | 1 alvo (`tupla(a, b)`), 2 valores | 2 alvos, 2 valores |
| `a,b := (1,2)` | 2 alvos, 1 valor (`tupla(1, 2)`) | 2 alvos, 1 valor |
| `a,b := funct(x, y)` | 2 alvos, 1 valor (chamada) | 2 alvos, 1 valor (chamada) |

A análise semântica deve normalizar antes de comparar: desmontar uma `tupla` que seja o único elemento de um lado; usar o número de retornos declarados quando o lado direito for uma única chamada; e exigir que cada alvo seja uma `var`.

---

## 13. Avaliação das Análises do Gemini, ChatGPT e Claude

As três análises em `docs/grammar/` foram feitas só por inspeção. Cada afirmação foi testada no parser real, e cada alteração proposta, no gerador LALR. O exemplo de retorno múltiplo da seção "Alterações" da `grammar.md` foi desconsiderado, a pedido.

**Confirmadas:**

| Afirmação | Quem | A correção gera conflito? |
|---|---|---|
| vírgula inicial aceita: `f(, inteiro: a)` e `g(, x)` (vem da v1.0) | Claude | `parametros_opt`/`argumentos_opt`: 0 |
| `E` e `OU` com a mesma precedência: `a \|\| b && c` → `((a \|\| b) && c)` | as três | dois níveis: 0 |
| unários não se encadeiam: `- -y` e `!!y` rejeitados | Claude, ChatGPT | `expressao_unaria` recursiva: 0 |
| `acao ::= erro` não existe no parser (em PLY o token é `error`) | Claude | — |
| `vazio` não definido na EBNF | ChatGPT | — |
| `retorna()`, `leia(a, b)`, `escreva(x, y)` rejeitados (decisão de projeto) | Claude, ChatGPT | aceitá-los: 0 |

**Erradas:**

- **ChatGPT, `lista_alvos` no lado esquerdo:** com encadeamento, 1 R/R; sem encadeamento, perde `(a,b) := …` nas funções, e acrescentar `( lista_alvos )` gera 2 R/R.
- **Claude, `NEWLINE` após `então`, linhas em branco e arquivo sem quebra final rejeitados:** falso; todos são aceitos, porque o `NewlineFilter` não gera esses `NEWLINE`. A regra do filtro só está descrita em prosa, o que explica a conclusão.
- **ChatGPT, "uniformizar" `bloco`/`corpo`:** a versão simplificada rejeitaria `se x então y := 1 fim`.
- **Gemini:** usa `!=` (o TPP usa `<>`) e diz que o unário é associativo à direita (não é recursivo, então não tem associatividade).

**Nenhuma percebeu:** `x := a -1.5e3` é rejeitado, porque o lexer reconhece `-1.5e3` como um único número com sinal (com espaço, `a - 1.5e3`, funciona).

---

## 14. Divisão do `ply_parser` em Módulos por Categoria

Seguindo a ideia do `cmmcompiler` (`rea-comp04-compiladores/cmmcompiler/parser/grammar/`), o `ply_parser.py` de cerca de 1200 linhas foi dividido. Diferenças em relação ao `cmmcompiler`, que deixou várias regras no `__init__.py`: a divisão foi completa, e **cada regra de erro ficou junto da regra principal**, por decisão tomada durante a sessão.

```
src/tppparser/ply_parser/
  __init__.py          descreve o pacote
  ply_parser.py        tokens + NEWLINE, p_error e PLYParser (monta o parser com yacc.yacc())
  newline_filter.py    NewlineFilter
  estado.py            error_handler, source_file, check_key, check_gentree, root
  grammar/
    __init__.py        só os "from .x import *"
    program.py         programa, lista_declaracoes, declaracao, vazio
    declarations.py    declaracao_variaveis, inicializacao_variaveis, lista_variaveis, lista_alvos, var, indice + erro, tipo
    functions.py       declaracao_funcao, tipos_retorno, lista_tipos, cabecalho + erro, lista_parametros, parametro + erro
    commands.py        bloco, corpo, acao, se + erro, repita + erro, atribuicao, leia + erro, escreva, retorna
    expressions.py     expressao … expressao_unaria, lista_expressoes, fator + erro, tupla, inicializador_array, numero, chamada_funcao, lista_argumentos + erro
    operators.py       os 5 tipos de operador
```

Cuidados específicos do PLY:

- **Estado compartilhado:** as regras leem e escrevem pelo módulo `estado` (`estado.check_key`, `estado.root`), porque um `from estado import check_key` copiaria o valor do momento do import. O `parser.errok()` virou `p.parser.errok()`, que o PLY 3.11 entrega a cada regra.
- **Ordem das regras:** o PLY ordena as funções `p_*` pelo número da linha, que se repete entre os arquivos. Isso não altera o parser enquanto houver `start='programa'` explícito e nenhum conflito reduce/reduce.

As 52 regras foram recortadas por script, junto com os comentários de sub-árvore; só as referências ao estado compartilhado mudaram.

Depois da divisão:

- **Montagem do parser na classe:** o `yacc.yacc()` saiu do nível do módulo e foi para `PLYParser._monta_parser()`, que monta o parser na primeira instância e o reutiliza nas seguintes, porque as tabelas são as mesmas para todas. Cada montagem custa cerca de 19 ms, e o import de `src.tppparser` deixou de montar o parser (antes, até o modo `--lexer` da CLI pagava esse custo). O `src/tppparser/__init__.py` deixou de exportar a variável global `parser`.
- **Execução direta removida:** o `main()` antigo, que permitia rodar o `ply_parser.py` sozinho, foi apagado. Junto saíram o ajuste de `sys.path`, `from sys import argv, exit` e o import do `PLYLexer`, que só ele usava. O parser é usado pela CLI (`src/tpp_compiler.py --parser`) ou pelo `get_parser`.

**Validação:**

| Comparação | Resultado |
|---|---|
| Produções geradas pelo PLY | idênticas (115) |
| Conflitos | idênticos (13 S/R, 0 R/R) |
| Árvore completa dos 64 `.tpp` de teste | idênticas |
| Saída do `--parser` com os 6 lexers (384 execuções) | idênticas |
| `test_extensoes_gramatica.py --lexer all` | 18 passam |
| `tppparser_test.py` | 12 passam, 16 falham (como antes) |

---

## 15. Arquivos Criados e Alterados

**Criados:**

- [conversa_gemini_bnf_exemplos_e_retorno_multiplo.md](conversa_gemini_bnf_exemplos_e_retorno_multiplo.md)
- [tests/test_extensoes_gramatica.py](tests/test_extensoes_gramatica.py): comentários e chaves nos 6 lexers; extensões, tuplas e `NEWLINE` no parser
- `src/tppparser/ply_parser/`: `__init__.py`, `estado.py`, `newline_filter.py` e o pacote `grammar/`

**Alterados:**

- lexers: `ply_lexer/methods.py`, `ply_lexer/regexs.py`, `ply_lexer/tokens.py`, `mandfa_lexer.py`, `symtable_lexer.py`, `automatalib_lexer.py`
- parser: [src/tppparser/ply_parser/ply_parser.py](src/tppparser/ply_parser/ply_parser.py) e [src/tppparser/\_\_init\_\_.py](src/tppparser/__init__.py)
- CLI: [src/tpp_compiler.py](src/tpp_compiler.py)
- testes: [tests/tppparser_test.py](tests/tppparser_test.py), [tests/conftest.py](tests/conftest.py), `tests/benchmark_lexers.py` e os `.tpp` de `tests/` (comentários `{* *}`)
- documentação: [docs/grammar/grammar.md](docs/grammar/grammar.md), [docs/LEX-SPECS.md](docs/LEX-SPECS.md), `src/tpplexer/README (1).md`

Nenhum commit foi feito durante a sessão.

---

## 16. Pendências e Decisões em Aberto

1. **Regras `error` sem ação:** `p_cabecalho_error`, `p_se_error`, `p_repita_error` etc. devolvem `None` e causam tracebacks depois de reportar o erro (`syn-test-008`, `lex-test-015`, `lex-test-026`, entre outros). Correção sugerida: devolver um nó `ERROR`, como o `p_indice_error`.
2. **Sucesso sem `-t`:** o `PLYParser.parse` só imprime `WAR-SYN-ANA-SUCCESS` com a árvore ligada; sem `-t`, um programa válido imprime `ERR-SYN-IRRECUPERAVEL`. Os `.syn.out` também divergem entre si na ordem das mensagens.
3. **Vírgula inicial** (`f(, x)`): corrigir com `parametros_opt`/`argumentos_opt` (0 conflitos).
4. **`acao ::= erro`:** tirar da EBNF ou implementar `acao ::= error NEWLINE`.
5. **Documentação da gramática:** definir `vazio ::= ε` e formalizar a regra de inserção do `NEWLINE`.
6. **Para decidir:** precedência de `E` sobre `OU` e unários encadeados (0 conflitos, mas mudam o significado de programas existentes); `retorna()` em procedimentos; listas em `leia`/`escreva`.
7. **Análise semântica:**
   - validar os alvos de atribuição (`var` ou tupla de `var`);
   - rejeitar tuplas fora do lado esquerdo;
   - conferir a aridade das atribuições múltiplas e do `retorna` com os `tipos_retorno`;
   - avisar quando um comando for uma expressão que não é chamada de função (`x := a` seguido de `+ b`);
   - definir a ordem de avaliação do encadeamento.
