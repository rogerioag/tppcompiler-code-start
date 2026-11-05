# Parametrização do Pytest e Evolução das Estratégias Léxicas: Automata-Lib e Tabela de Símbolos

**Data:** 25 de Setembro de 2026  
**Projeto:** `tppcompiler-code-start` / Compilador TPP  
**Ambiente:** Linux / Python 3.14 / automata-lib / PLY / Pytest  

---

## Sumário
1. [Visão Geral e Objetivos da Sessão](#1-visão-geral-e-objetivos-da-sessão)
2. [Estratégias Léxicas Disponíveis no Compilador](#2-estratégias-léxicas-disponíveis-no-compilador)
3. [Parametrização do Pytest via CLI (`--lexer`)](#3-parametrização-do-pytest-via-cli---lexer)
4. [Geração Dinâmica de Casos de Teste (`pytest_generate_tests`)](#4-geração-dinâmica-de-casos-de-teste-pytest_generate_tests)
5. [Execução Direta do Script de Testes via Python](#5-execução-direta-do-script-de-testes-via-python)
6. [Estratégia Automata-Lib: Híbrida (`AutomataLibManLexer`) vs. Pura (`AutomataLibLexer`)](#6-estratégia-automata-lib-híbrida-automatalibmanlexer-vs-pura-automataliblexer)
   - 6.1. [Versão Híbrida (`automatalibman_lexer.py`)](#61-versão-híbrida-automatalibman_lexerpy)
   - 6.2. [Versão Pura com Maximal Munch (`automatalib_lexer.py`)](#62-versão-pura-com-maximal-munch-automatalib_lexerpy)
7. [Estratégia Tabela de Símbolos: Híbrida (`SymbolTableManLexer`) vs. Pura Table-Driven (`SymbolTableLexer`)](#7-estratégia-tabela-de-símbolos-híbrida-symboltablemanlexer-vs-pura-table-driven-symboltablelexer)
   - 7.1. [O Conceito Central do Analisador Orientado a Tabela](#71-o-conceito-central-do-analisador-orientado-a-tabela)
   - 7.2. [Versão Híbrida (`symtableman_lexer.py`)](#72-versão-híbrida-symtableman_lexerpy)
   - 7.3. [Versão Pura Table-Driven (`symtable_lexer.py`)](#73-versão-pura-table-driven-symtable_lexerpy)
8. [Integração com a Fábrica Léxica e CLI do Compilador](#8-integração-com-a-fábrica-léxica-e-cli-do-compilador)
9. [Resultados e Validação Experimental da Suíte de Testes](#9-resultados-e-validação-experimental-da-suíte-de-testes)
10. [Conclusão e Registro das Decisões](#10-conclusão-e-registro-das-decisões)
11. [Benchmark de Performance com Grande Sequência de Tokens](#11-benchmark-de-performance-com-grande-sequência-de-tokens)
    - 11.1. [Script de Benchmark CLI (`tests/benchmark_lexers.py`)](#111-script-de-benchmark-cli-testsbenchmark_lexerspy)
    - 11.2. [Resultados Experimentais Reais (182.500 e 36.500 tokens)](#112-resultados-experimentais-reais-182500-e-36500-tokens)
    - 11.3. [Teste de Performance e Conformidade no Pytest (`tests/test_perf_large_tokens.py`)](#113-teste-de-performance-e-conformidade-no-pytest-teststest_perf_large_tokenspy)
12. [Validação Completa da Suíte de Testes do Projeto (44 Testes)](#12-validação-completa-da-suíte-de-testes-do-projeto-44-testes)

---

## 1. Visão Geral e Objetivos da Sessão

Durante esta sessão, foram abordados três grandes eixos de evolução da infraestrutura do compilador TPP:

1. **Parametrização do Pytest:** Capacidade de selecionar e filtrar facilmente a estratégia léxica a ser testada tanto via linha de comando (`pytest --lexer=<tipo>`) quanto executando diretamente o arquivo de teste com o interpretador Python.
2. **Implementação Pura com Automata-Lib:** Desenvolvimento de um analisador léxico formal completo utilizando autômatos finitos determinísticos da biblioteca `automata-lib` e algoritmo de maior casamento (*Maximal Munch*), sem qualquer herança do analisador manual procedural (`ManualDFALexer`).
3. **Implementação Pura Orientada a Tabela de Símbolos (*Table-Driven*):** Separação do analisador de tabela de símbolos em duas variantes bem definidas:
   - Uma versão híbrida com herança de `ManualDFALexer`.
   - Uma versão pura e independente onde a **Tabela de Símbolos** é o motor central de mapeamento léxico, pré-populada com palavras reservadas, operadores e pontuações, gerenciando dinamicamente identificadores de usuário.

---

## 2. Estratégias Léxicas Disponíveis no Compilador

O compilador TPP conta com **6 estratégias léxicas** intercambiáveis, todas aderentes à interface base [BaseLexer](file:///run/media/rag/DADOS/repositorios/Dropbox/dados/rogerio/projetos/projetos.github/tppcompiler-code-start/src/tpplexer/base_lexer.py):

| Estratégia (`--lexer`) | Classe | Arquivo | Paradigma |
|---|---|---|---|
| `ply` | [PLYLexer](file:///run/media/rag/DADOS/repositorios/Dropbox/dados/rogerio/projetos/projetos.github/tppcompiler-code-start/src/tpplexer/ply_lexer/ply_lexer.py) | [ply_lexer.py](file:///run/media/rag/DADOS/repositorios/Dropbox/dados/rogerio/projetos/projetos.github/tppcompiler-code-start/src/tpplexer/ply_lexer/ply_lexer.py) | Gerador de analisador léxico com expressões regulares (Lex/Yacc em Python) |
| `mandfa` / `manual` | [ManualDFALexer](file:///run/media/rag/DADOS/repositorios/Dropbox/dados/rogerio/projetos/projetos.github/tppcompiler-code-start/src/tpplexer/mandfa_lexer/mandfa_lexer.py) | [mandfa_lexer.py](file:///run/media/rag/DADOS/repositorios/Dropbox/dados/rogerio/projetos/projetos.github/tppcompiler-code-start/src/tpplexer/mandfa_lexer/mandfa_lexer.py) | Autômato finito determinístico implementado de forma procedural em Python |
| `automatalibman` | [AutomataLibManLexer](file:///run/media/rag/DADOS/repositorios/Dropbox/dados/rogerio/projetos/projetos.github/tppcompiler-code-start/src/tpplexer/automatalib_lexer/automatalibman_lexer.py) | [automatalibman_lexer.py](file:///run/media/rag/DADOS/repositorios/Dropbox/dados/rogerio/projetos/projetos.github/tppcompiler-code-start/src/tpplexer/automatalib_lexer/automatalibman_lexer.py) | Implementação híbrida com `automata-lib` com herança da implementação manual de `DFA` `ManualDFALexer`: Herda de `ManualDFALexer` e usa `DFA` do `automata-lib` como validador de padrões. |
| `automatalib` | [AutomataLibLexer](file:///run/media/rag/DADOS/repositorios/Dropbox/dados/rogerio/projetos/projetos.github/tppcompiler-code-start/src/tpplexer/automatalib_lexer/automatalib_lexer.py) | [automatalib_lexer.py](file:///run/media/rag/DADOS/repositorios/Dropbox/dados/rogerio/projetos/projetos.github/tppcompiler-code-start/src/tpplexer/automatalib_lexer/automatalib_lexer.py) | Implementação pura com `automata-lib`: Herda de `BaseLexer`, constrói 5-tuplas de AFDs formais com `automata-lib` e consome via *Maximal Munch* |
| `symtableman` | [SymbolTableManLexer](file:///run/media/rag/DADOS/repositorios/Dropbox/dados/rogerio/projetos/projetos.github/tppcompiler-code-start/src/tpplexer/symtable_lexer/symtableman_lexer.py) | [symtableman_lexer.py](file:///run/media/rag/DADOS/repositorios/Dropbox/dados/rogerio/projetos/projetos.github/tppcompiler-code-start/src/tpplexer/symtable_lexer/symtableman_lexer.py) | Implementação híbrida com `SymbolTable` com herança da implementação manual de `DFA` `ManualDFALexer`: Herda de `ManualDFALexer` e acopla a `SymbolTable` para catalogar identificadores. |
| `symtable` | [SymbolTableLexer](file:///run/media/rag/DADOS/repositorios/Dropbox/dados/rogerio/projetos/projetos.github/tppcompiler-code-start/src/tpplexer/symtable_lexer/symtable_lexer.py) | [symtable_lexer.py](file:///run/media/rag/DADOS/repositorios/Dropbox/dados/rogerio/projetos/projetos.github/tppcompiler-code-start/src/tpplexer/symtable_lexer/symtable_lexer.py) | Implementação dirigida a tabela (`Table-Driven`): Implementa a `symtable` herdando de `BaseLexer`, símbolos fixos pré-instalados na tabela, _lookup_ direto e inserção de IDs. |



---

## 3. Parametrização do Pytest via CLI (`--lexer`)

Para permitir testar estratégias individuais ou todas de uma só vez sem alterar código-fonte, foi registrado um argumento customizado no Pytest no arquivo [tests/conftest.py](file:///run/media/rag/DADOS/repositorios/Dropbox/dados/rogerio/projetos/projetos.github/tppcompiler-code-start/tests/conftest.py) por meio do hook `pytest_addoption`:

```python
def pytest_addoption(parser):
    """Adiciona opções de linha de comando personalizadas para o pytest."""
    parser.addoption(
        "--lexer",
        action="store",
        default="ply",
        choices=["all", "ply", "mandfa", "symtable", "symtableman", "automatalib", "automatalibman"],
        help="Especifica qual lexer testar: ply, mandfa, symtable, symtableman, automatalib, automatalibman ou all (padrão: ply)",
    )
```

Essa opção integra-se perfeitamente com a infraestrutura nativa do Pytest, aceitando sintaxes como:
```bash
pytest tests/tpplex_test.py --lexer=automatalib
pytest tests/tpplex_test.py --lexer=symtable
pytest tests/tpplex_test.py --lexer=all
```

---

## 4. Geração Dinâmica de Casos de Teste (`pytest_generate_tests`)

Anteriormente, para alternar o lexer em [tests/tpplex_test.py](file:///run/media/rag/DADOS/repositorios/Dropbox/dados/rogerio/projetos/projetos.github/tppcompiler-code-start/tests/tpplex_test.py), era necessário comentar ou descomentar listas de tuplas estáticas. 

A solução adotada utiliza o hook `pytest_generate_tests(metafunc)`, que lê a opção `--lexer` em tempo de configuração e gera **apenas os casos de teste correspondentes ao(s) lexer(s) selecionado(s)**:

```python
def pytest_generate_tests(metafunc):
    """Gera dinamicamente os casos de teste com base na opção --lexer."""
    if "lexer_type" in metafunc.fixturenames and "key_option" in metafunc.fixturenames and "input_file" in metafunc.fixturenames:
        lexer_opt = metafunc.config.getoption("lexer")
        
        if lexer_opt == "all":
            lexers = ["ply", "mandfa", "symtable", "symtableman", "automatalib", "automatalibman"]
        else:
            lexers = [lexer_opt]
        
        cases = []
        for lexer in lexers:
            cases.append((lexer, "-k", ""))
            cases.append((lexer, "-k", "teste.c"))
            cases.append((lexer, "-k", "notexist.tpp"))
        
        files = sorted(fnmatch.filter(os.listdir('tests/lex-tests/'), '*.tpp'))
        for file in files:
            for lexer in lexers:
                cases.append((lexer, "-k", file))

        metafunc.parametrize("lexer_type, key_option, input_file", cases)
```

### Vantagens:
- **Execução limpa:** Não há testes ignorados (*deselected* ou *skipped*). Se `--lexer=symtable` for passado, exatamente 42 testes são instanciados e executados.
- **Isolamento de memória:** A lista de casos `cases = []` é local ao escopo do hook, prevenindo acúmulo duplicado entre fixtures.

---

## 5. Execução Direta do Script de Testes via Python

Para permitir que desenvolvedores rodem os testes chamando diretamente o script `python tests/tpplex_test.py`, foi adicionado o ponto de entrada `__main__`:

```python
if __name__ == "__main__":
    import sys
    sys.exit(pytest.main(sys.argv[1:] + [__file__]))
```

Dessa forma, qualquer argumento passado na linha de comando é repassado ao `pytest`:
```bash
python tests/tpplex_test.py --lexer=automatalib -v
python tests/tpplex_test.py --lexer=symtable -q
```

---

## 6. Estratégia Automata-Lib: Híbrida (`AutomataLibManLexer`) vs. Pura (`AutomataLibLexer`)

A implementação baseada na biblioteca formal `automata-lib` foi bifurcada em dois arquivos com objetivos didáticos e arquiteturais distintos:

### 6.1. Versão Híbrida (`automatalibman_lexer.py`)
- **Arquivo:** [src/tpplexer/automatalib_lexer/automatalibman_lexer.py](file:///run/media/rag/DADOS/repositorios/Dropbox/dados/rogerio/projetos/projetos.github/tppcompiler-code-start/src/tpplexer/automatalib_lexer/automatalibman_lexer.py)
- **Classe:** `class AutomataLibManLexer(ManualDFALexer)`
- **Conceito:** Herda a máquina de varredura manual de `ManualDFALexer` e substitui os métodos de validação (`is_valid_identifier`, `is_scientific_notation`) por instâncias de `DFA` do `automata-lib`.

### 6.2. Versão Pura com Maximal Munch (`automatalib_lexer.py`)
- **Arquivo:** [src/tpplexer/automatalib_lexer/automatalib_lexer.py](file:///run/media/rag/DADOS/repositorios/Dropbox/dados/rogerio/projetos/projetos.github/tppcompiler-code-start/src/tpplexer/automatalib_lexer/automatalib_lexer.py)
- **Classe:** `class AutomataLibLexer(BaseLexer)`
- **Conceito:** Implementação 100% formal baseada na teoria dos autômatos finitos.

#### Características da Abordagem Pura:
1. **Modelagem Matemática de AFDs**: Cada classe léxica é definida formalmente por sua 5-tupla $M = (Q, \Sigma, \delta, q_0, F)$:
   - `_build_dfa_id()`: Aceita identificadores no padrão TPP com suporte a caracteres acentuados.
   - `_build_dfa_inteiro()`: Numerais inteiros.
   - `_build_dfa_flutuante()`: Numerais decimais com ponto e/ou expoente.
   - `_build_dfa_notacao_cientifica()`: Padrão estrito de notação científica.
   - `_build_dfa_literal()`: Operadores relacionais (`<=`, `>=`, `<>`, `:=`), aritméticos, lógicos e delimitadores.
2. **Simulador de Transição com Casamento Mais Longo (*Maximal Munch*)**:
   - O método `_match_dfa_longest(dfa, start_pos)` alimenta a função $\delta(q, c)$ caractere por caractere a partir da posição atual do cursor.
   - Se o autômato atinge um estado de aceitação em uma posição $p$, essa posição é registrada como candidato. O autômato continua avançando enquanto houver transições válidas.
   - Todos os autômatos competem em paralelo; o autômato que aceitar o maior número de caracteres ganha a posse do lexema.
   - Em caso de empate no comprimento, prevalece a ordem de precedência das regras.
   - Tratamento de caracteres inválidos: dispara o erro padrão `ERR-LEX-INV-CHAR` com recuperação léxica e avanço do cursor.

---

## 7. Estratégia Tabela de Símbolos: Híbrida (`SymbolTableManLexer`) vs. Pura Table-Driven (`SymbolTableLexer`)

### 7.1. O Conceito Central do Analisador Orientado a Tabela
Nos compiladores clássicos, o analisador léxico orientado a tabela (*Table-Driven Scanner*) utiliza a **Tabela de Símbolos** não apenas como repositório posterior para a análise semântica, mas como **estrutura primária de reconhecimento e emissão de tokens**:
- Todas as palavras-chave fixas da linguagem (`se`, `entao`, `retorna`, `flutuante`, etc.) e operadores/delimitadores são pré-instalados na tabela durante a inicialização.
- Ao encontrar um lexema alfanumérico na entrada, o scanner consulta a tabela (`lookup`):
  - Se o lexema já existe na tabela com um token específico (ex: `se` -> `SE`), esse token é retornado imediatamente.
  - Se o lexema não existe na tabela, trata-se de um novo identificador definido pelo usuário: ele é instalado na tabela como símbolo de categoria `ID` e a classe de token `ID` é retornada.
  - Em leituras subsequentes do mesmo identificador, ele já estará na tabela e será reconhecido imediatamente.

### 7.2. Versão Híbrida (`symtableman_lexer.py`)
- **Arquivo:** [src/tpplexer/symtable_lexer/symtableman_lexer.py](file:///run/media/rag/DADOS/repositorios/Dropbox/dados/rogerio/projetos/projetos.github/tppcompiler-code-start/src/tpplexer/symtable_lexer/symtableman_lexer.py)
- **Classe:** `class SymbolTableManLexer(ManualDFALexer)`
- **Conceito:** Herda diretamente de `ManualDFALexer`. O fluxo procedural do `ManualDFALexer` extrai o token e o `SymbolTableManLexer` apenas intercepta os tokens de identificador para cadastrá-los na tabela.

### 7.3. Versão Pura Table-Driven (`symtable_lexer.py`)
- **Arquivo:** [src/tpplexer/symtable_lexer/symtable_lexer.py](file:///run/media/rag/DADOS/repositorios/Dropbox/dados/rogerio/projetos/projetos.github/tppcompiler-code-start/src/tpplexer/symtable_lexer/symtable_lexer.py)
- **Classe:** `class SymbolTableLexer(BaseLexer)`
- **Conceito:** Independente de `ManualDFALexer`. O método `token()` implementa diretamente a lógica guiada pela tabela:

```python
class SymbolTableLexer(BaseLexer):
    def __init__(self, error_handler=None):
        super().__init__(error_handler=error_handler)
        self.symbol_table = SymbolTable()
        self._init_symbol_table()

    def _init_symbol_table(self):
        """Pré-instala palavras-chave e símbolos fixos na tabela de símbolos."""
        # Palavras reservadas
        for lexeme, token_type in KEYWORDS.items():
            self.symbol_table.insert(
                lexeme,
                token_type=token_type,
                category=SymbolCategory.KEYWORD,
                is_builtin=True,
            )
        # Operadores e pontuação
        for lexeme, token_type in FIXED_SYMBOLS.items():
            self.symbol_table.insert(
                lexeme,
                token_type=token_type,
                category=SymbolCategory.OPERATOR if token_type in OPERATOR_TOKENS else SymbolCategory.DELIMITER,
                is_builtin=True,
            )
```

#### Fluxo do Reconhecimento no `token()`:
1. **Espaços e Comentários:** Ignora espaços e consome comentários no padrão `{ ... }`.
2. **Termos Alfanuméricos:** Lê a sequência de letras, dígitos e acentos. Consulta `self.symbol_table.lookup(lexeme)`:
   - Se encontrado: emite o token pré-cadastrado (palavra-chave ou identificador já conhecido).
   - Se não encontrado: valida o formato de identificador, instala na tabela com `insert(lexeme, token_type="ID", category=SymbolCategory.IDENTIFIER)` e devolve o token `ID`.
3. **Numerais:** Números com ponto decimal e notação científica são processados por métodos numéricos dedicados (`_read_number`).
4. **Operadores e Pontuações:** Verifica operadores compostos de 2 caracteres (`:=`, `<=`, `>=`, `<>`) e simples de 1 caractere consultando diretamente `self.symbol_table.lookup(op_candidate)`.
5. **Ciclo de Vida Limpo:** Ao carregar um novo código-fonte (`input()`), o método `self.symbol_table.reset_user_symbols()` é invocado, expurgando identificadores do arquivo anterior e preservando os símbolos fixos embutidos.

---

## 8. Integração com a Fábrica Léxica e CLI do Compilador

### Fábrica Léxica ([src/tpplexer/\_\_init\_\_.py](file:///run/media/rag/DADOS/repositorios/Dropbox/dados/rogerio/projetos/projetos.github/tppcompiler-code-start/src/tpplexer/__init__.py))
Centraliza a criação dos analisadores conforme a chave informada:

```python
def get_lexer(lexer_type="ply", error_handler=None):
    lexer_type = lexer_type.lower()
    if lexer_type == "ply":
        return PLYLexer(error_handler=error_handler)
    elif lexer_type in ("mandfa", "manual"):
        return ManualDFALexer(error_handler=error_handler)
    elif lexer_type == "symtableman":
        return SymbolTableManLexer(error_handler=error_handler)
    elif lexer_type == "symtable":
        return SymbolTableLexer(error_handler=error_handler)
    elif lexer_type == "automatalibman":
        return AutomataLibManLexer(error_handler=error_handler)
    elif lexer_type == "automatalib":
        return AutomataLibLexer(error_handler=error_handler)
    else:
        raise ValueError(f"Lexer desconhecido: '{lexer_type}'")
```

### CLI do Compilador ([src/tpp_compiler.py](file:///run/media/rag/DADOS/repositorios/Dropbox/dados/rogerio/projetos/projetos.github/tppcompiler-code-start/src/tpp_compiler.py))
Configuração com validação de opções:

```python
cli.add_argument(
    "--lexer",
    choices=["ply", "mandfa", "symtable", "symtableman", "automatalib", "automatalibman"],
    default="ply",
    help="Estratégia Léxica (ply, mandfa, symtable, symtableman, automatalib, automatalibman)",
)
```

Exemplo de uso na linha de comando:
```bash
python src/tpp_compiler.py tests/lex-tests/bubble_sort.tpp --lexer=automatalib
python src/tpp_compiler.py tests/lex-tests/bubble_sort.tpp --lexer=symtable
```

---

## 9. Resultados e Validação Experimental da Suíte de Testes

A suíte completa de testes léxicos ([tests/tpplex_test.py](file:///run/media/rag/DADOS/repositorios/Dropbox/dados/rogerio/projetos/projetos.github/tppcompiler-code-start/tests/tpplex_test.py)), composta por 42 cenários (incluindo testes de robustez a arquivos inexistentes, entradas vazias e todos os programas de teste em `tests/lex-tests/*.tpp`), foi executada individualmente para cada analisador:

| Estratégia | Comando de Teste | Resultado | Tempo |
|---|---|---|---|
| `ply` | `pytest tests/tpplex_test.py --lexer=ply -q` | **42 passed (100%)** | ~14.2s |
| `mandfa` | `pytest tests/tpplex_test.py --lexer=mandfa -q` | **42 passed (100%)** | ~14.1s |
| `automatalibman` | `pytest tests/tpplex_test.py --lexer=automatalibman -q` | **42 passed (100%)** | ~14.2s |
| `automatalib` | `pytest tests/tpplex_test.py --lexer=automatalib -q` | **42 passed (100%)** | ~14.6s |
| `symtableman` | `pytest tests/tpplex_test.py --lexer=symtableman -q` | **42 passed (100%)** | ~14.4s |
| `symtable` | `pytest tests/tpplex_test.py --lexer=symtable -q` | **42 passed (100%)** | ~14.5s |

### Execução de Todos os Analisadores em Lote:
```bash
pytest tests/tpplex_test.py --lexer=all -q
# Total: 252 testes executados (42 testes x 6 estratégias) -> 252 passed (100%)
```

---

## 10. Conclusão e Registro das Decisões

1. **Padronização dos Nomes de Arquivos e Classes:**
   - Analisadores com herança de `ManualDFALexer` utilizam o sufixo `*man`:
     - `automatalibman_lexer.py` contendo `AutomataLibManLexer`.
     - `symtableman_lexer.py` contendo `SymbolTableManLexer`.
   - Analisadores autônomos/puros utilizam o nome direto do módulo:
     - `automatalib_lexer.py` contendo `AutomataLibLexer`.
     - `symtable_lexer.py` contendo `SymbolTableLexer`.

2. **Aderência Arquitetural do `SymbolTableLexer`:**
   - A versão pura atende estritamente à definição clássica da literatura: a tabela de símbolos é consultada para decidir a classe do lexema (`lookup`), instalando novos identificadores (`insert`) de forma transparente e emitindo o token correto.

3. **Flexibilidade e Confiabilidade:**
   - A suíte de testes agora permite avaliar o comportamento de qualquer estratégia com um único argumento de linha de comando (`--lexer=<tipo>`), garantindo paridade total entre todos os analisadores desenvolvidos.

---

## 11. Benchmark de Performance com Grande Sequência de Tokens

Para avaliar a taxa de transferência (*throughput* em tokens/segundo) e o tempo de execução comparativo entre as 6 implementações de analisador léxico, foram implementadas duas ferramentas complementares:

### 11.1. Script de Benchmark CLI ([tests/benchmark_lexers.py](file:///run/media/rag/DADOS/repositorios/Dropbox/dados/rogerio/projetos/projetos.github/tppcompiler-code-start/tests/benchmark_lexers.py))
- Gera um programa TPP sintético e equilibrado (palavras-chave, identificadores, números inteiros, flutuantes e notação científica, operadores e comentários).
- Permite parametrizar quantidade de blocos (`--blocks`), repetições com warm-up (`--rounds`), subconjunto de lexers (`--lexers`) e saída em tabela Markdown (`--markdown`).
- Valida conformidade garantindo que todas as estratégias reconheçam rigorosamente a mesma contagem de tokens.

### 11.2. Resultados Experimentais Reais

#### Carga Massiva: 2.500 Blocos (~182.500 Tokens / 52.500 Linhas)
Executado com o comando:
```bash
python tests/benchmark_lexers.py
```

```text
[+] Gerando código de entrada TPP com 2500 blocos estruturados...
    Tamanho do fonte: 1635.3 KB (~52500 linhas)

[+] Iniciando medições (3 rodadas por estratégia com warm-up)...
    -> Testando 'ply'... concluído: 182500 tokens em 0.4590s (397,638 tok/s)
    -> Testando 'mandfa'... concluído: 182500 tokens em 1.0810s (168,823 tok/s)
    -> Testando 'symtable'... concluído: 182500 tokens em 1.0632s (171,659 tok/s)
    -> Testando 'symtableman'... concluído: 182500 tokens em 1.0588s (172,368 tok/s)
    -> Testando 'automatalib'... concluído: 182500 tokens em 0.9311s (196,010 tok/s)
    -> Testando 'automatalibman'... concluído: 182500 tokens em 0.9542s (191,253 tok/s)

[✓] Conformidade verificada: todas as estratégias reconheceram exatamente 182.500 tokens.
```

| Estratégia | Tokens | Tempo Médio (s) | Tempo Mín (s) | Vazão (tokens/s) | Relativo (vs PLY) |
|---|---|---|---|---|---|
| `ply` | 182.500 | 0.4590s | 0.4555s | 397.638 tok/s | 1.00x (baseline) |
| `automatalib` | 182.500 | 0.9311s | 0.9239s | 196.010 tok/s | 0.49x |
| `automatalibman` | 182.500 | 0.9542s | 0.9326s | 191.253 tok/s | 0.48x |
| `symtableman` | 182.500 | 1.0588s | 1.0250s | 172.368 tok/s | 0.43x |
| `symtable` | 182.500 | 1.0632s | 1.0520s | 171.659 tok/s | 0.43x |
| `mandfa` | 182.500 | 1.0810s | 1.0287s | 168.823 tok/s | 0.42x |

#### Carga Média Filtrada: 500 Blocos (~36.500 Tokens / 5 Rodadas)
Executado com o comando:
```bash
python tests/benchmark_lexers.py --lexers=ply,symtable,automatalib --blocks=500 --rounds=5
```

| Estratégia | Tokens | Tempo Médio (s) | Tempo Mín (s) | Vazão (tokens/s) | Relativo (vs PLY) |
|---|---|---|---|---|---|
| `automatalib` | 36.500 | 0.0659s | 0.0655s | 553.689 tok/s | 1.37x |
| `symtable` | 36.500 | 0.0799s | 0.0787s | 456.645 tok/s | 1.13x |
| `ply` | 36.500 | 0.0902s | 0.0891s | 404.778 tok/s | 1.00x (baseline) |

### 11.3. Teste de Performance e Conformidade no Pytest ([tests/test_perf_large_tokens.py](file:///run/media/rag/DADOS/repositorios/Dropbox/dados/rogerio/projetos/projetos.github/tppcompiler-code-start/tests/test_perf_large_tokens.py))
- Integra-se diretamente ao hook `--lexer` do [conftest.py](file:///run/media/rag/DADOS/repositorios/Dropbox/dados/rogerio/projetos/projetos.github/tppcompiler-code-start/tests/conftest.py).
- Processa >36.000 tokens em memória sem overhead de processos do sistema operacional.
- Realiza asserção rigorosa de igualdade: compara elemento a elemento se a sequência de tipos de tokens emitida pelo lexer testado é 100% idêntica ao baseline `PLY`.
- Execução com todas as 6 estratégias:
```bash
pytest tests/test_perf_large_tokens.py --lexer=all -v -s
```
**Resultado:**
```text
======================= test session starts =======================
collected 12 items

tests/test_perf_large_tokens.py::test_large_token_sequence_performance[ply] 
[PERFORMANCE] Lexer: ply             | Tokens: 36.500 | Tempo: 0.0916s | Vazão: 398.548 tok/s PASSED
tests/test_perf_large_tokens.py::test_large_token_sequence_performance[mandfa] 
[PERFORMANCE] Lexer: mandfa          | Tokens: 36.500 | Tempo: 0.0669s | Vazão: 545.805 tok/s PASSED
tests/test_perf_large_tokens.py::test_large_token_sequence_performance[symtable] 
[PERFORMANCE] Lexer: symtable        | Tokens: 36.500 | Tempo: 0.0928s | Vazão: 393.307 tok/s PASSED
tests/test_perf_large_tokens.py::test_large_token_sequence_performance[symtableman] 
[PERFORMANCE] Lexer: symtableman     | Tokens: 36.500 | Tempo: 0.0961s | Vazão: 379.735 tok/s PASSED
tests/test_perf_large_tokens.py::test_large_token_sequence_performance[automatalib] 
[PERFORMANCE] Lexer: automatalib     | Tokens: 36.500 | Tempo: 0.0717s | Vazão: 508.948 tok/s PASSED
tests/test_perf_large_tokens.py::test_large_token_sequence_performance[automatalibman] 
[PERFORMANCE] Lexer: automatalibman  | Tokens: 36.500 | Tempo: 0.0699s | Vazão: 522.034 tok/s PASSED

tests/test_perf_large_tokens.py::test_token_types_conformance_with_baseline[ply] PASSED
tests/test_perf_large_tokens.py::test_token_types_conformance_with_baseline[mandfa] PASSED
tests/test_perf_large_tokens.py::test_token_types_conformance_with_baseline[symtable] PASSED
tests/test_perf_large_tokens.py::test_token_types_conformance_with_baseline[symtableman] PASSED
tests/test_perf_large_tokens.py::test_token_types_conformance_with_baseline[automatalib] PASSED
tests/test_perf_large_tokens.py::test_token_types_conformance_with_baseline[automatalibman] PASSED

======================= 12 passed in 1.33s ========================
```

---

## 12. Validação Completa da Suíte de Testes do Projeto (44 Testes)

Com a incorporação do módulo de performance [tests/test_perf_large_tokens.py](file:///run/media/rag/DADOS/repositorios/Dropbox/dados/rogerio/projetos/projetos.github/tppcompiler-code-start/tests/test_perf_large_tokens.py) junto à suíte funcional de 42 casos de [tests/tpplex_test.py](file:///run/media/rag/DADOS/repositorios/Dropbox/dados/rogerio/projetos/projetos.github/tppcompiler-code-start/tests/tpplex_test.py), o Pytest passa a coletar e validar **44 testes por padrão**:

```bash
$ pytest -v
======================= test session starts =======================
platform linux -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0
collected 44 items

tests/test_perf_large_tokens.py::test_large_token_sequence_performance[ply] PASSED [  2%]
tests/test_perf_large_tokens.py::test_token_types_conformance_with_baseline[ply] PASSED [  4%]
tests/tpplex_test.py::test_execute[ply--k-] PASSED          [  6%]
tests/tpplex_test.py::test_execute[ply--k-teste.c] PASSED   [  9%]
tests/tpplex_test.py::test_execute[ply--k-notexist.tpp] PASSED [ 11%]
...
tests/tpplex_test.py::test_execute[ply--k-lex-test-039.tpp] PASSED [100%]

======================= 44 passed in 14.21s =======================
```
