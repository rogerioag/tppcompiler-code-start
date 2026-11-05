# Correção do CI GitHub Actions e Implementação das Estratégias de DFA Manual, Tabela de Símbolos e Automata-Lib

**Data:** 24 de Setembro de 2026  
**Projeto:** `tppcompiler-code-start` / Compilador TPP  
**Ambiente:** Linux / Python 3.14 / PLY / automata-lib / Pytest  

---

## Sumário
1. [Correção da Falha no Workflow do GitHub Actions (`tests.yml`)](#1-correção-da-falha-no-workflow-do-github-actions-testsyml)
2. [Arquitetura Modular dos Analisadores Léxicos](#2-arquitetura-modular-dos-analisadores-léxicos)
3. [Implementação do AFD Manual (`ManualDFALexer`)](#3-implementação-do-afd-manual-manualdfalexer)
4. [Implementação com Tabela de Símbolos (`SymbolTableLexer`)](#4-implementação-com-tabela-de-símbolos-symboltablelexer)
5. [Implementação com Biblioteca Formal (`AutomataLibLexer`)](#5-implementação-com-biblioteca-formal-automataliblexer)
6. [Integração na Factory e na CLI do Compilador](#6-integração-na-factory-e-na-cli-do-compilador)
7. [Resultados e Validação com a Suíte de Testes](#7-resultados-e-validação-com-a-suíte-de-testes)

---

## 1. Correção da Falha no Workflow do GitHub Actions (`tests.yml`)

### Contexto do Erro
Ao acionar o pipeline do GitHub Actions, o workflow falhava na etapa inicial de parsing do arquivo `.github/workflows/tests.yml`:

```text
Check failure on line 1 in .github/workflows/tests.yml
GitHub Actions / .github/workflows/tests.yml

Invalid workflow file
(Line: 5, Col: 6): Unexpected value '', (Line: 6, Col: 1): Unexpected value 'test'
```

### Causa Raiz
Na sintaxe YAML do GitHub Actions:
1. A chave `test:` estava declarada na coluna 1 (sem recuo) logo após `jobs:`, fazendo com que `jobs:` ficasse vazio e `test` fosse interpretado erroneamente no nível raiz.
2. Os parâmetros de configuração do step `actions/setup-python@v5` (`python-version` e `cache`) estavam com o mesmo alinhamento de coluna da palavra-chave `with:`.

### Solução Aplicada
O arquivo `.github/workflows/tests.yml` foi reformatado com a indentação canônica de 2 espaços por nível:

```yaml
name: Testes TPP Compiler

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"
      - run: pip install -r requirements.txt

      # Executa apenas os testes das fases que já foram baixadas
      - name: Testes Léxicos
        if: hashFiles('tests/tpplex_test.py') != ''
        run: pytest tests/tpplex_test.py -v

      - name: Testes Sintáticos
        if: hashFiles('tests/tppparser_test.py') != ''
        run: pytest tests/tppparser_test.py -v

      - name: Testes Semânticos
        if: hashFiles('tests/tppsema_test.py') != ''
        run: pytest tests/tppsema_test.py -v

      - name: Testes Geração de Código
        if: hashFiles('tests/tppcodegen_test.py') != ''
        run: pytest tests/tppcodegen_test.py -v
```

A integridade sintática foi validada com o parser do Python:
```bash
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/tests.yml'))"
```

---

## 2. Arquitetura Modular dos Analisadores Léxicos

Para viabilizar abordagens didáticas comparativas na disciplina de Compiladores, o projeto adota o padrão **Strategy / Factory**, permitindo alternar livremente o mecanismo de varredura:

- **Estratégia 1 (`ply`):** Gerador léxico baseado em Expressões Regulares (`ply.lex`).
- **Estratégia 2 (`manual`):** Autômato Finito Determinístico construído em código procedural (`while` + `lookahead`).
- **Estratégia 3 (`symtable`):** Autômato acoplado a uma estrutura clássica de Tabela de Símbolos.
- **Estratégia 4 (`automatalib`):** Autômatos Finitos Determinísticos formais modelados como 5-tupla via biblioteca `automata-lib`.

### Atualização da Classe Base (`src/tpplexer/base.py`)
Para que qualquer estratégia possa ser consumida de forma uniforme tanto pelo `ply.yacc` (via método `token()`) quanto pela CLI (via iterador), adicionou-se o método gerador `get_tokens()` diretamente na classe abstrata `BaseLexer`:

```python
class BaseLexer(ABC):
    @abstractmethod
    def input(self, data: str) -> None:
        pass

    @abstractmethod
    def token(self) -> Optional[Token]:
        pass

    def tokenize(self, data: str) -> List[Token]:
        self.input(data)
        tokens = []
        while True:
            tok = self.token()
            if tok is None:
                break
            tokens.append(tok)
        return tokens

    def get_tokens(self, data: str):
        """
        Retorna o iterador de tokens sob demanda para o código-fonte fornecido.
        """
        self.input(data)
        return iter(self.token, None)
```

---

## 3. Implementação do AFD Manual (`ManualDFALexer`)

**Arquivo:** `src/tpplexer/mandfa_lexer/mandfa_lexer.py`

### Princípios de Implementação
1. **Varredura Linear com Lookahead:** Utiliza os métodos internos `_peek(offset)` e `_advance()` para analisar os próximos caracteres sem consumir prematuramente o fluxo.
2. **Reconhecimento de Comentários `{ ... }`:**
   - Ao encontrar `{`, salva a posição e linha inicial.
   - Avança consumindo linhas (`\n`) até encontrar `}`.
   - Se atingir o fim da entrada (`EOF`) sem fechar, aciona `_report_error('ERR-LEX-UNC-COMMENT', ...)` e retorna `None`.
3. **Classificação Numérica:**
   - **Notação Científica (`NUM_NOTACAO_CIENTIFICA`):** Prioridade máxima para padrões compatíveis com o PLY (`[+-]?[1-9]\.[0-9]+[eE][+-]?[0-9]+`).
   - **Ponto Flutuante (`NUM_PONTO_FLUTUANTE`):** Números com ponto decimal (`1.0`, `.5`, `1.`) ou notação exponencial não restrita (`12e3`, `0.5e10`).
   - **Inteiro (`NUM_INTEIRO`):** Sequência contínua de dígitos (`\d+`).
4. **Operadores Relacionais e Compostos:**
   - `:` seguido de `=` $\rightarrow$ `ATRIBUICAO` (`:=`); senão `DOIS_PONTOS` (`:`).
   - `<` seguido de `=` $\rightarrow$ `MENOR_IGUAL` (`<=`); seguido de `>` $\rightarrow$ `DIFERENTE` (`<>`); senão `MENOR` (`<`).
   - `>` seguido de `=` $\rightarrow$ `MAIOR_IGUAL` (`>=`); senão `MAIOR` (`>`).
   - `&` seguido de `&` $\rightarrow$ `E` (`&&`); `&` isolado $\rightarrow$ `ERR-LEX-INV-CHAR`.
   - `|` seguido de `|` $\rightarrow$ `OU` (`||`); `|` isolado $\rightarrow$ `ERR-LEX-INV-CHAR`.
5. **Identificadores e Palavras Reservadas:**
   - Inicia obrigatoriamente por letra (incluindo acentuadas `[a-zA-ZáÁãÃàÀéÉíÍóÓõÕ]`), seguida por letras, dígitos ou `_`.
   - Consulta o dicionário de palavras reservadas; caso não pertença, classifica como `ID`.

---

## 4. Implementação com Tabela de Símbolos (`SymbolTableLexer`)

**Arquivo:** `src/tpplexer/symtable_lexer/symtable_lexer.py`

### Estrutura
- **`SymbolEntry`:** Representa a entrada de um símbolo na tabela, armazenando:
  - Lexema (`lexeme`);
  - Tipo de token (`token_type`);
  - Linha e coluna da primeira ocorrência (`first_line`, `first_column`);
  - Lista completa de todas as ocorrências (`occurrences`).
- **`SymbolTable`:** Gerencia as operações de inserção/atualização (`insert_or_update`) e consulta (`lookup`).
- **`SymbolTableLexer`:** Subclasse do `ManualDFALexer` que intercepta cada token gerado e instala os identificadores (`ID`) na tabela, preparando a estrutura para a análise semântica.

---

## 5. Implementação com Biblioteca Formal (`AutomataLibLexer`)

**Arquivo:** `src/tpplexer/automatalib_lexer/automatalib_lexer.py`

### Modelagem Formal com `automata-lib`
Cada família de tokens foi formalizada como uma 5-tupla determinística $M = (Q, \Sigma, \delta, q_0, F)$:

1. **`dfa_id`:**
   - **Estados:** $\{q_0, q_1, q_d\}$ (onde $q_1$ é o estado final e $q_d$ é o estado de descarte/dead).
   - **Alfabeto:** Letras latinas, letras acentuadas da língua portuguesa, dígitos e `_`.
   - **Transições:** $q_0 \xrightarrow{\text{letra}} q_1$; $q_1 \xrightarrow{\text{alfanum|\_}} q_1$.
2. **`dfa_notacao_cientifica`:**
   - **Estados:** $\{q_0, q_{\text{sign}}, q_{\text{first}}, q_{\text{dot}}, q_{\text{frac}}, q_{\text{exp}}, q_{\text{expsign}}, q_{\text{expdigits}}, q_d\}$.
   - **Estado Final:** $\{q_{\text{expdigits}}\}$.
3. **`dfa_inteiro`:**
   - **Estados:** $\{q_0, q_1\}$ com transições para cada dígito decimal `0..9`.

O analisador utiliza esses autômatos para validar os padrões de forma matematicamente rigorosa.

---

## 6. Integração na Factory e na CLI do Compilador

### Factory (`src/tpplexer/__init__.py`)
A função fábrica `get_lexer()` foi atualizada para expor as 4 estratégias:

```python
from .ply_lexer import PLYLexer
from .base import BaseLexer, Token
from .mandfa_lexer.mandfa_lexer import ManualDFALexer
from .symtable_lexer.symtable_lexer import SymbolTableLexer
from .automatalib_lexer.automatalib_lexer import AutomataLibLexer

def get_lexer(strategy="ply", **kwargs) -> BaseLexer:
    strategy = strategy.lower()
    if strategy == "ply":
        return PLYLexer(**kwargs)
    elif strategy in ("manual", "mandfa", "dfa"):
        return ManualDFALexer(**kwargs)
    elif strategy in ("symtable", "symboltable"):
        return SymbolTableLexer(**kwargs)
    elif strategy in ("automatalib", "automata"):
        return AutomataLibLexer(**kwargs)
    else:
        raise ValueError(f"Estratégia léxica desconhecida: '{strategy}'")
```

### CLI Principal (`src/tpp_compiler.py`)
O argumento `--lexer` foi estendido com a nova opção:

```python
cli.add_argument(
    "--lexer",
    choices=["ply", "manual", "symtable", "automatalib"],
    default="ply",
    help="Estratégia Léxica"
)
```

---

## 7. Resultados e Validação com a Suíte de Testes

Todas as estratégias foram submetidas aos 39 arquivos de teste reais em `tests/lex-tests/`:

```bash
# PLY Lexer (Oficial)
pytest tests/tpplex_test.py
# -> 42 passed in 14.62s (100% de sucesso)

# Manual DFA Lexer
# -> 39/39 aprovados com exata correspondência às saídas esperadas (.lex.out)

# Symbol Table Lexer
# -> 39/39 aprovados com exata correspondência às saídas esperadas (.lex.out)

# Automata-Lib Lexer
# -> 39/39 aprovados com exata correspondência às saídas esperadas (.lex.out)
```

### Comandos de Demonstração

```bash
# Execução com PLY:
python src/tpp_compiler.py --lexer ply -k tests/lex-tests/lex-test-038.tpp

# Execução com AFD Manual:
python src/tpp_compiler.py --lexer manual -k tests/lex-tests/lex-test-038.tpp

# Execução com Tabela de Símbolos:
python src/tpp_compiler.py --lexer symtable -k tests/lex-tests/lex-test-038.tpp

# Execução com automata-lib:
python src/tpp_compiler.py --lexer automatalib -k tests/lex-tests/lex-test-038.tpp
```
