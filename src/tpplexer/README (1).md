# analise-lexica-code-start

O projeto **`analise-lexica-code-start`** é a estrutura e código inicial de referência para a fase de **Análise Léxica (Scanner)** de um compilador da linguagem didática `TPP`, o projeto é desenvolvido em `Python` usando a biblioteca `PLY`  (`ply.lex`).

## Análise Léxica

A __Análise Léxica__ é a fase do compilador que lê o código-fonte do arquivo de entrada como um fluxo de caracteres, e nesse processo de varredura reconhece os _tokens_ ou marcas da linguagem. As denominações Sistema de Varredura, Analisador Léxico e _Scanner_ são equivalentes.

Devem ser reconhecidas as marcas presentes na linguagem `TPP`, como `se`, `então`, `repita`, `até` que são palavras chave, palavras reservadas. Como palavras reservadas temos `se`, `então`, `senão`, `fim`, `repita`, `flutuante`, `retorna`, `até`, `leia`, `escreva`, `inteiro`.

Tipos numéricos inteiros (`NUM_INTEIRO`), ponto flutuante (`NUM_PONTO_FLUTUANTE`) e notação científica (`NUM_NOTACAO_CIENTIFICA`).

Operadores e Símbolos, aritméticos (`+`, `-`, `*`, `/`), lógicos (`&&`, `||`, `!`), relacionais (`<>`, `<=`, `>=`, `<`, `>`, `=`), atribuição (`:=`), e delimitadores (`(`, `)`, `[`, `]`, `,`, `:`).

O tratamento de comentários e linhas. Comentários utilizam o formato `{ ... }`,  o que estiver interno às marcações de comentário são ignorados no fluxo de _tokens_, mas a contagem de linhas (`lineno`) é atualizada levando em conta quebras de linha dentro do bloco de comentário.

Além dessas classes de _token_, precisam ser reconhecidos os nomes de variáveis e funções que são os _identificadores_.

O processo de reconhecimento das marcas (_tokens_), a identificação de padrões pode ser feito de duas formas: utilizando-se __expressões regulares__ ou implementando o analisador com a teoria de __autômatos finitos__.

Neste projeto serão utilizadas _expressões regulares_ na __especificação léxica__, os padrões de reconhecimentos das marcas.

Para um código simples em `TPP` igual o Código 1.

```C
{ Programa simples. }

inteiro principal()
  retorna(0)
fim
```
__Código 1:__ _Programa em `TPP`_

A lista de marcas que precisam ser identificadas é:

```
INTEIRO
ID
ABRE_PARENTESE
FECHA_PARENTESE
RETORNA
ABRE_PARENTESE
NUM_INTEIRO
FECHA_PARENTESE
FIM
```

## Visão Geral da Estrutura

| Arquivo / Diretório        | Descrição                                                    |
| :------------------------- | :----------------------------------------------------------- |
| `tpplex.py`                | **Módulo Principal:** Implementa a especificação das ERs (Expressões Regulares), tokens, tratamento de comentários, ignorados, exceções e CLI da análise léxica. |
| `myerror.py`               | **Gestor de Erros:** Classe `MyError` que formata e traduz códigos de erros com base em um arquivo de propriedades. |
| `ErrorMessages.properties` | Arquivo de mensagens padronizadas de erro (suporta chave `-k` para retornar apenas o identificador da mensagem). |
| `tpplex_test.py`           | **Testes Automatizados:** Suíte de testes em `pytest` que executa o lexer em lote contra a pasta `tests/`. |
| `tests/`                   | Conjunto de 38 casos de teste com arquivos `.tpp` e suas saídas esperadas `.lex.out`. |

## Preparação do Ambiente

Para a implementação da fase de __Análise Léxica__ é necessário instalar ferramentas, como o `PLY`. Os pré-requisitos podem ser instalados utilizando o arquivo de `requirements.txt`.

```bash
$ pip install  -r requirements.txt
```

```bash
$ cat requirements.txt
pytest
ply
configparser
logging
```

O `PLY` é uma implementação do `lex` e `yacc` para Python. O módulo `ply.lex` implementa o componente de análise léxica do `PLY`, o nome `yacc` significa _"Yet Another Compiler Compiler"_ e é emprestado da ferramenta Unix.

O `PLY` é implementado inteiramente em `Python` e usa o algoritmo `LR-parsing` o que é razoavelmente eficiente.

* Site: [PLY](https://www.dabeaz.com/ply/) 
* Artigo: [_Prototyping Interpreters using Python Lex-Yacc_ by Shannon Behrens, March 01, 2004](https://www.drdobbs.com/web-development/prototyping-interpreters-using-python-le/184405580)
* [Documentação do PLY](https://www.dabeaz.com/ply/ply.html)
* Github: [PLY 4.0](https://github.com/dabeaz/ply)

## Validação e Testes Automatizados

No projeto estão disponibilizados arquivos de exemplos em `TPP` para testes. Os testes estão no diretório `tests` do raiz do projeto.
Para executar o analisador léxico `tpplex.py` com um arquivo específico basta chamar a implementação passando o arquivo de entrada como parâmetro.

```bash
$ python tpplex.py arquivo.tpp
```

Utilizando o teste com um código simples:

```C
{ Programa simples. }

inteiro principal()
  retorna(0)
fim
```
Executa o _scanner_ e imprime a lista de nomes de _tokens_ correspondentes.

```bash
$ python tpplex.py tests/lex-test-006.tpp
INTEIRO
ID
ABRE_PARENTESE
FECHA_PARENTESE
RETORNA
ABRE_PARENTESE
NUM_INTEIRO
FECHA_PARENTESE
FIM
```

Se o existir algum erro no código fonte.

```C
{ Programa simples. }

inteiro principal()
  retorna(0)
  ç
fim
```

A execução do `tpplex.py` vai mostrar a mensagem de erro junto com a lista de _tokens_.

```bash
$ python tpplex.py tests/lex-test-006.tpp
INTEIRO
ID
ABRE_PARENTESE
FECHA_PARENTESE
RETORNA
ABRE_PARENTESE
NUM_INTEIRO
FECHA_PARENTESE
Erro[3][3]: Caracter inválido. valor: 
FIM
$ 
```

Para que somente chaves de erros sejam impressas e para que testes com erros possam ser executados, a implementação do analisador léxico pode ser chamada com o parâmetro `-k`  que imprime somente as _chaves de erros_ ou _códigos de erros_, caso existam.

```bash
$ python tpplex.py -k tests/lex-test-006.tpp
INTEIRO
ID
ABRE_PARENTESE
FECHA_PARENTESE
RETORNA
ABRE_PARENTESE
NUM_INTEIRO
FECHA_PARENTESE
ERR-LEX-INV-CHAR
FIM
$ 
```

No lugar da mensagem de erro foi impressa a chave `ERR-LEX-INV-CHAR` que evita que os testes não funcionem por mensagens de erros diferentes de cada implementação.

Todos os testes podem ser executados via `pytest`. A suíte de testes em `tpplex_test.py` testa dinamicamente todos os arquivos na pasta `tests/` além de situações de teste de erros de entrada, como arquivo inexistente e extensão incorreta.

```bash
[analise-lexica-code-start]$ pytest -v
==================================================== test session starts =====================================================
platform linux -- Python 3.14.7, pytest-9.0.3, pluggy-1.6.0 -- /usr/bin/python
cachedir: .pytest_cache
rootdir: analise-lexica-code-start
plugins: anyio-4.13.0
collected 42 items                                                                                                           

tpplex_test.py::test_execute[--k] PASSED                                                                               [  2%]
tpplex_test.py::test_execute[teste.c--k] PASSED                                                                        [  4%]
tpplex_test.py::test_execute[notexist.tpp--k] PASSED                                                                   [  7%]
tpplex_test.py::test_execute[lex-test-001.tpp--k] PASSED                                                               [  9%]
tpplex_test.py::test_execute[lex-test-002.tpp--k] PASSED                                                               [ 11%]
tpplex_test.py::test_execute[lex-test-003.tpp--k] PASSED                                                               [ 14%]
tpplex_test.py::test_execute[lex-test-004.tpp--k] PASSED                                                               [ 16%]
tpplex_test.py::test_execute[lex-test-005.tpp--k] PASSED                                                               [ 19%]
tpplex_test.py::test_execute[lex-test-006.tpp--k] PASSED                                                               [ 21%]
tpplex_test.py::test_execute[lex-test-007.tpp--k] PASSED                                                               [ 23%]
tpplex_test.py::test_execute[lex-test-008.tpp--k] PASSED                                                               [ 26%]
tpplex_test.py::test_execute[lex-test-009.tpp--k] PASSED                                                               [ 28%]
tpplex_test.py::test_execute[lex-test-010.tpp--k] PASSED                                                               [ 30%]
tpplex_test.py::test_execute[lex-test-011.tpp--k] PASSED                                                               [ 33%]
tpplex_test.py::test_execute[lex-test-012.tpp--k] PASSED                                                               [ 35%]
tpplex_test.py::test_execute[lex-test-013.tpp--k] PASSED                                                               [ 38%]
tpplex_test.py::test_execute[lex-test-014.tpp--k] PASSED                                                               [ 40%]
tpplex_test.py::test_execute[lex-test-015.tpp--k] PASSED                                                               [ 42%]
tpplex_test.py::test_execute[lex-test-016.tpp--k] PASSED                                                               [ 45%]
tpplex_test.py::test_execute[lex-test-017.tpp--k] PASSED                                                               [ 47%]
tpplex_test.py::test_execute[lex-test-018.tpp--k] PASSED                                                               [ 50%]
tpplex_test.py::test_execute[lex-test-019.tpp--k] PASSED                                                               [ 52%]
tpplex_test.py::test_execute[lex-test-020.tpp--k] PASSED                                                               [ 54%]
tpplex_test.py::test_execute[lex-test-021.tpp--k] PASSED                                                               [ 57%]
tpplex_test.py::test_execute[lex-test-022.tpp--k] PASSED                                                               [ 59%]
tpplex_test.py::test_execute[lex-test-023.tpp--k] PASSED                                                               [ 61%]
tpplex_test.py::test_execute[lex-test-024.tpp--k] PASSED                                                               [ 64%]
tpplex_test.py::test_execute[lex-test-025.tpp--k] PASSED                                                               [ 66%]
tpplex_test.py::test_execute[lex-test-026.tpp--k] PASSED                                                               [ 69%]
tpplex_test.py::test_execute[lex-test-027.tpp--k] PASSED                                                               [ 71%]
tpplex_test.py::test_execute[lex-test-028.tpp--k] PASSED                                                               [ 73%]
tpplex_test.py::test_execute[lex-test-029.tpp--k] PASSED                                                               [ 76%]
tpplex_test.py::test_execute[lex-test-030.tpp--k] PASSED                                                               [ 78%]
tpplex_test.py::test_execute[lex-test-031.tpp--k] PASSED                                                               [ 80%]
tpplex_test.py::test_execute[lex-test-032.tpp--k] PASSED                                                               [ 83%]
tpplex_test.py::test_execute[lex-test-033.tpp--k] PASSED                                                               [ 85%]
tpplex_test.py::test_execute[lex-test-034.tpp--k] PASSED                                                               [ 88%]
tpplex_test.py::test_execute[lex-test-035.tpp--k] PASSED                                                               [ 90%]
tpplex_test.py::test_execute[lex-test-036.tpp--k] PASSED                                                               [ 92%]
tpplex_test.py::test_execute[lex-test-037.tpp--k] PASSED                                                               [ 95%]
tpplex_test.py::test_execute[lex-test-038.tpp--k] PASSED                                                               [ 97%]
tpplex_test.py::test_execute[lex-test-039.tpp--k] PASSED                                                               [100%]

===================================================== 42 passed in 2.45s =====================================================
[analise-lexica-code-start]$
```

**Resultado:** **42 testes executados e 100% aprovados** (39 casos de programas TPP + 3 casos de tratamento de erro de entrada).

## Tratamento de Comentário não fechado

Existe uma outra abordagem para tratamento de comentário não fechado, utilizando estados exclusivos no `PLY` (Exclusive States). Essa abordagem é mais adequada para o tratamento de comentários, pois permite que o lexer processe o conteúdo do comentário de forma diferente do código.

Declara-se um estado exclusivo no início do arquivo:

```python
states = (
    ('comentario', 'exclusive'),
)
```

Define-se a transição para o estado comentário:

```python
# Quando encontra '{' no estado normal (INITIAL), entra no estado 'comentario'
def t_INITIAL_comentario(t):
    r'\{'
    t.lexer.start_line = t.lexer.lineno
    t.lexer.start_column = define_column(t.lexer.lexdata, t.lexpos)
    t.lexer.begin('comentario')
```

Dentro do estado 'comentário', ignora tudo exceto quebras de linha e '}':

```python
# Dentro do estado 'comentário', ignora tudo exceto quebras de linha e '}'
def t_comentario_conteudo(t):
    r'[^}\n]+'
    pass

def t_comentario_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ao encontrar '}', retorna ao estado normal
def t_comentario_fechar(t):
    r'\}'
    t.lexer.begin('INITIAL')

# Erro ou EOF dentro do estado comentario
def t_comentario_error(t):
    # Tratamento de caractere dentro do comentário
    t.lexer.skip(1)
```

Se a análise terminar (EOF) enquanto o `lexer` ainda estiver no estado _comentario_, significa que o comentário não foi fechado.


## Leitura Recomendada

1. __Capítulo 2:__ _Varredura_

    LOUDEN, Kenneth C. Compiladores: princípios e práticas. São Paulo, SP: Thomson, c2004. xiv, 569 p. ISBN 8522104220.

2. __Capítulo 3:__ _Análise Léxica_

    AHO, Alfred V. et al. Compiladores: princípios, técnicas e ferramentas. 2. ed. São Paulo, SP: Pearson Addison-Wesley, 2008. x, 634 p. ISBN 9788588639249.
    
------