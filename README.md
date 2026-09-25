# tppcompiler-code-start

Repositório Template para o projeto de desenvolvimento do compilador para a linguagem `TPP`.

## Estrutura do Projeto

```
tppcompiler-code-start/
├── .github/workflows/                      # Workflows do GitHub Actions (CI)
├── docs/                                   # Especificações das fases do compilador
│   ├── LEX-SPECS.md                        # Especificação léxica
│   ├── SYN-SPECS.md                        # Especificação sintática
│   ├── SEM-SPECS.md                        # Especificação semântica
│   └── CODEGEN-SPECS.md                    # Especificação de geração de código
├── src/                                    # Código-fonte do compilador
│   ├── tpp_compiler.py                     # Script principal da CLI
│   ├── myerror.py                          # Gerenciador de erros e mensagens
│   ├── GlobalErrorMessages.properties      # Mensagens de erro globais
│   ├── tpplexer/                           # Módulos e estratégias de análise léxica
│   │   ├── __init__.py                     # Factory get_lexer e exportações
│   │   ├── base.py                         # Classe base abstrata (BaseLexer) e Token
│   │   ├── LogErrorLexer.py                # Tratamento e formatação de erros léxicos
│   │   ├── LexerErrorMessages.properties   # Mensagens de erro léxicas
│   │   ├── ply_lexer/                      # Estratégia PLY (tokens, regexs, methods, ply_lexer)
│   │   ├── mandfa_lexer/                   # Estratégia DFA manual procedural
│   │   ├── symtable_lexer/                 # Estratégias com Tabela de Símbolos
│   │   │   ├── symtable_lexer.py           # Versão pura dirigida a tabela (Table-Driven)
│   │   │   └── symtableman_lexer.py        # Versão híbrida com herança de ManualDFALexer
│   │   └── automatalib_lexer/              # Estratégias com automata-lib
│   │       ├── automatalib_lexer.py        # Versão pura com AFDs formais e Maximal Munch
│   │       └── automatalibman_lexer.py     # Versão híbrida com herança de ManualDFALexer
│   ├── tppparser/                          # Módulos de análise sintática
│   │   └── ParserMessages.properties       # Mensagens de erro sintáticas
│   ├── tppsema/                            # Análise semântica (em desenvolvimento)
│   │   └── SemaErrorMessages.properties    # Mensagens de erro semânticos
│   └── tppcodegen/                         # Geração de código (em desenvolvimento)
│   │   └── CodeGenErrorMessages.properties # Mensagens de erro Geração de Código
├── tests/                                  # Suíte de testes e benchmarks
│   ├── conftest.py                         # Configuração e hook --lexer do Pytest
│   ├── tpplex_test.py                      # Testes funcionais da fase léxica (42 testes)
│   ├── test_perf_large_tokens.py           # Testes de performance e integridade léxica
│   ├── benchmark_lexers.py                 # Script CLI de benchmark e profiling comparativo
│   └── lex-tests/                          # Casos de teste (.tpp) e saídas de referência (.lex.out)
└── requirements.txt                        # Dependências do projeto
```

## Instalação dos Requisitos

Recomenda-se utilizar um ambiente virtual `Python` com a versão 3.10 ou superior.

1. **Criar e ativar o ambiente virtual:**
  ```bash
  [tppcompiler-code-start]$ python3 -m venv .venv
  [tppcompiler-code-start]$ source .venv/bin/activate
  ```

2. **Instalar as dependências do projeto:**

  ```bash
  [tppcompiler-code-start]$ pip install -r requirements.txt
  ```

As dependências principais incluem:
- `ply`: Gerador de analisadores léxicos e sintáticos para Python.
- `pytest`: _Framework_ para execução da suíte de testes automatizados.
- `configparser`: Manipulação de arquivos de configuração e mensagens de erro.

---

## Executar o Compilador (`tpp_compiler`)

O ponto de entrada principal da `CLI` é o _script_ `src/tpp_compiler.py`.

### Sintaxe Básica

```bash
[tppcompiler-code-start]$ python src/tpp_compiler.py --help
usage: tpp_compiler.py [-h] [--lexer {ply,mandfa,symtable,symtableman,automatalib,automatalibman}] [--parser {yacc,topdown}] [--sema {sema}]
                       [--gencode {llvm}] [-k]
                       fonte

Compilador TPP [tppc]

positional arguments:
  fonte                 arquivo-fonte .tpp

options:
  -h, --help            show this help message and exit
  --lexer {ply,mandfa,symtable,symtableman,automatalib,automatalibman}
                        Estratégia Léxica
  --parser {yacc,topdown}
                        Estratégia Sintática
  --sema, --semantic {sema}
                        Estratégia Semântica
  --gencode, --codegen {llvm}
                        Estratégia de Geração de Código
  -k                    Imprimir chaves de Erro.
[tppcompiler-code-start]$  
```

### Parâmetros e Opções

| Parâmetro | Tipo | Padrão | Descrição |
| :--- | :--- | :--- | :--- |
| `fonte` | Posicional | *(obrigatório)* | Caminho para o arquivo-fonte com extensão `.tpp`. |
| `--lexer` | Opção | `ply` | Estratégia de análise léxica: `ply`, `mandfa` (DFA manual), `symtable` / `symtableman` (com Tabela de Símbolos), `automatalibman` (com herança de ManualDFALexer) ou `automatalib` (DFA puro automata-lib com Maximal Munch). |
| `--parser` | Opção | `yacc` | Estratégia de análise sintática: `yacc` _(botton up)_ ou `topdown` (análise descendente). |
| `--sema`, `--semantic` | Opção | `default` | Estratégia de análise semântica. |
| `--gencode`, `--codegen` | Opção | `llvm` | Estratégia de geração de código intermediário/final (ex.: `llvm`, gera `LLVM-IR`). |
| `-k` | Flag | `False` | Imprime apenas as **chaves dos erros** (ex.: `ERR-GLOB-USE`, `ERR-LEX-INV-CHAR`) em vez das mensagens completas formatadas. Útil para testes automatizados. Chaves de erros são semelhantes a _tokens_. |
| `-h`, `--help` | Flag | - | Exibe o menu de ajuda com todas as opções disponíveis. |

### Exemplos de Uso

- **Exibir ajuda completa da CLI:**
```bash
[tppcompiler-code-start]$ python src/tpp_compiler.py --help
```

- **Execução padrão (análise léxica com PLY):**
```bash
[tppcompiler-code-start]$ python src/tpp_compiler.py tests/lex-tests/lex-test-001.tpp
INTEIRO
DOIS_PONTOS
ID
VIRGULA
ID
```

- **Selecionar uma estratégia léxica específica:**

```bash
# Usando PLY
[tppcompiler-code-start]$ python src/tpp_compiler.py tests/lex-tests/lex-test-001.tpp --lexer ply

# Usando o analisador baseado em AFD manual (mandfa)
[tppcompiler-code-start]$ python src/tpp_compiler.py tests/lex-tests/lex-test-001.tpp --lexer mandfa
```

- **Exibir chaves de erro (modo `-k`):**
```bash
# Execução normal sobre o lex-test-002.tpp com erro.
[tppcompiler-code-start]$ python src/tpp_compiler.py tests/lex-tests/lex-test-002.tpp --lexer ply
INTEIRO
DOIS_PONTOS
ID
VIRGULA
ID
Erro[2][1]: Caracter inválido. valor: ç

# Execução com -k para imprimir as chaves de erros.
[tppcompiler-code-start]$ python src/tpp_compiler.py tests/lex-tests/lex-test-002.tpp --lexer ply -k
INTEIRO
DOIS_PONTOS
ID
VIRGULA
ID
ERR-LEX-INV-CHAR
[tppcompiler-code-start]$
```

---

## Executar os Testes

O projeto utiliza o **Pytest** para validação contínua e testes de regressão dos módulos.

### Comandos de Teste

- **Executar todos os testes:** Vai recuperar os arquivos de testes existentes em `tests` e executá-los.
```bash
[tppcompiler-code-start]$ pytest
============================================================== test session starts ==============================================================
platform linux -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0
rootdir: tppcompiler-code-start
plugins: anyio-4.13.0
collected 44 items                                    

tests/test_perf_large_tokens.py ..              [  4%]
tests/tpplex_test.py ..........................................                              [100%]

================================= 44 passed in 14.07s =================================
[tppcompiler-code-start]$ 
```

- **Executar testes com saída detalhada (*verbose*):** Recupera os arquivos de testes existentes em `tests` e os executa com mais detalhes na saída.
```bash
[tppcompiler-code-start]$ pytest -v
================================ test session starts ================================
platform linux -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0 -- /usr/bin/python
cachedir: .pytest_cache
rootdir: tppcompiler-code-start
plugins: anyio-4.13.0
collected 44 items                                    

tests/test_perf_large_tokens.py::test_large_token_sequence_performance[ply] PASSED           [  2%]
tests/test_perf_large_tokens.py::test_token_types_conformance_with_baseline[ply] PASSED      [  4%]
tests/tpplex_test.py::test_execute[ply--k-] PASSED                                           [  6%]
tests/tpplex_test.py::test_execute[ply--k-teste.c] PASSED                                    [  9%]
tests/tpplex_test.py::test_execute[ply--k-notexist.tpp] PASSED                               [ 11%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-001.tpp] PASSED                           [ 13%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-002.tpp] PASSED                           [ 15%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-003.tpp] PASSED                           [ 18%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-004.tpp] PASSED                           [ 20%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-005.tpp] PASSED                           [ 22%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-006.tpp] PASSED                           [ 25%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-007.tpp] PASSED                           [ 27%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-008.tpp] PASSED                           [ 29%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-009.tpp] PASSED                           [ 31%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-010.tpp] PASSED                           [ 34%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-011.tpp] PASSED                           [ 36%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-012.tpp] PASSED                           [ 38%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-013.tpp] PASSED                           [ 40%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-014.tpp] PASSED                           [ 43%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-015.tpp] PASSED                           [ 45%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-016.tpp] PASSED                           [ 47%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-017.tpp] PASSED                           [ 50%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-018.tpp] PASSED                           [ 52%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-019.tpp] PASSED                           [ 54%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-020.tpp] PASSED                           [ 56%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-021.tpp] PASSED                           [ 59%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-022.tpp] PASSED                           [ 61%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-023.tpp] PASSED                           [ 63%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-024.tpp] PASSED                           [ 65%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-025.tpp] PASSED                           [ 68%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-026.tpp] PASSED                           [ 70%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-027.tpp] PASSED                           [ 72%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-028.tpp] PASSED                           [ 75%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-029.tpp] PASSED                           [ 77%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-030.tpp] PASSED                           [ 79%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-031.tpp] PASSED                           [ 81%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-032.tpp] PASSED                           [ 84%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-033.tpp] PASSED                           [ 86%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-034.tpp] PASSED                           [ 88%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-035.tpp] PASSED                           [ 90%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-036.tpp] PASSED                           [ 93%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-037.tpp] PASSED                           [ 95%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-038.tpp] PASSED                           [ 97%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-039.tpp] PASSED                           [100%]

================================ 44 passed in 14.09s ================================
[tppcompiler-code-start]$
```

- **Executar apenas os testes da fase Léxica:** Testes definidos no `tpplex_test.py`, por padrão será executado a versão do analisador feita com `ply`.
```bash
[tppcompiler-code-start]$ pytest tests/tpplex_test.py -v
================================ test session starts ================================
platform linux -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0 -- /usr/bin/python
cachedir: .pytest_cache
rootdir: tppcompiler-code-start
plugins: anyio-4.13.0
collected 42 items                                    

tests/tpplex_test.py::test_execute[ply--k-] PASSED                                           [  2%]
tests/tpplex_test.py::test_execute[ply--k-teste.c] PASSED                                    [  4%]
tests/tpplex_test.py::test_execute[ply--k-notexist.tpp] PASSED                               [  7%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-001.tpp] PASSED                           [  9%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-002.tpp] PASSED                           [ 11%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-003.tpp] PASSED                           [ 14%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-004.tpp] PASSED                           [ 16%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-005.tpp] PASSED                           [ 19%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-006.tpp] PASSED                           [ 21%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-007.tpp] PASSED                           [ 23%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-008.tpp] PASSED                           [ 26%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-009.tpp] PASSED                           [ 28%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-010.tpp] PASSED                           [ 30%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-011.tpp] PASSED                           [ 33%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-012.tpp] PASSED                           [ 35%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-013.tpp] PASSED                           [ 38%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-014.tpp] PASSED                           [ 40%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-015.tpp] PASSED                           [ 42%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-016.tpp] PASSED                           [ 45%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-017.tpp] PASSED                           [ 47%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-018.tpp] PASSED                           [ 50%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-019.tpp] PASSED                           [ 52%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-020.tpp] PASSED                           [ 54%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-021.tpp] PASSED                           [ 57%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-022.tpp] PASSED                           [ 59%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-023.tpp] PASSED                           [ 61%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-024.tpp] PASSED                           [ 64%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-025.tpp] PASSED                           [ 66%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-026.tpp] PASSED                           [ 69%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-027.tpp] PASSED                           [ 71%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-028.tpp] PASSED                           [ 73%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-029.tpp] PASSED                           [ 76%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-030.tpp] PASSED                           [ 78%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-031.tpp] PASSED                           [ 80%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-032.tpp] PASSED                           [ 83%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-033.tpp] PASSED                           [ 85%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-034.tpp] PASSED                           [ 88%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-035.tpp] PASSED                           [ 90%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-036.tpp] PASSED                           [ 92%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-037.tpp] PASSED                           [ 95%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-038.tpp] PASSED                           [ 97%]
tests/tpplex_test.py::test_execute[ply--k-lex-test-039.tpp] PASSED                           [100%]

============================================================== 42 passed in 13.70s ==============================================================
[rag@backporting tppcompiler-code-start]$ 

```

- **Filtrar testes por estratégia específica (usando a opção `--lexer`):** Cada uma das estratégias de análise léxica, isto é, cada versão de implementação pode ser testada em específico sendo passada na opção `--lexer`.

```bash
# Executar apenas testes de um lexer específico via flag customizada:
[tppcompiler-code-start]$ pytest --lexer=ply -v
[tppcompiler-code-start]$ pytest --lexer=mandfa -v
[tppcompiler-code-start]$ pytest --lexer=symtable -v
[tppcompiler-code-start]$ pytest --lexer=symtableman -v
[tppcompiler-code-start]$ pytest --lexer=automatalibman -v
[tppcompiler-code-start]$ pytest --lexer=automatalib -v
```

- **Executar Benchmark de Performance com Grande Sequência de Tokens:** Testes de desempenho.
```bash
# Executa o benchmark para todas as estratégias com ~115.000 tokens (3 rodadas):
[tppcompiler-code-start]$ python tests/benchmark_lexers.py

# Benchmark com saída em tabela Markdown:
[tppcompiler-code-start]$ python tests/benchmark_lexers.py --blocks=1000 --markdown

# Benchmark filtrado por estratégias específicas:
[tppcompiler-code-start]$ python tests/benchmark_lexers.py --lexers=ply,symtable,automatalib --blocks=2000
```

- **Executar Teste de Performance e Integridade no Pytest:**
```bash
# Valida conformidade e tempo de execução com >36.000 tokens:
[tppcompiler-code-start]$ pytest tests/test_perf_large_tokens.py --lexer=all -v -s
[tppcompiler-code-start]$ pytest tests/test_perf_large_tokens.py --lexer=symtable -v -s
```


[Análise Léxica](docs/LEX-SPECS.md)
[Análise Sintática](docs/SYN-SPECS.md)
[Análise Semântica](docs/SEM-SPECS.md)
[Geração de Código](docs/CODEGEN-SPECS.md)