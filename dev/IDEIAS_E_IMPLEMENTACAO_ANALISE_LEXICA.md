# Ideias Didáticas, Arquitetura e Implementação - Análise Léxica TPP

Este documento consolida o diagnóstico, correções realizadas, técnicas de tratamento de erros e propostas didáticas discutidas para o ensino de **Análise Léxica (Scanner)** e integração com **Análise Sintática (Parser/PLY)** no projeto **`analise-lexica-code-start`**.

---

## 1. Visão Geral do Projeto `analise-lexica-code-start`

- **Linguagem Alvo:** `TPP` (Linguagem Didática de Compiladores).
- **Ferramenta Principal:** Python 3 + `ply.lex` (Python Lex-Yacc).
- **Estrutura de Arquivos:**
  - `tpplex.py`: Módulo principal do lexer, especificações de ERs, tokens, comentários e CLI.
  - `myerror.py`: Classe `MyError` que gerencia e formata mensagens/códigos de erro com base em propriedades.
  - `ErrorMessages.properties`: Dicionário contendo os textos e chaves de erros (ex: `ERR-LEX-INV-CHAR`, `ERR-LEX-UNC-COMMENT`).
  - `tpplex_test.py`: Suíte de testes automatizados executada via `pytest`.
  - `tests/`: Pasta contendo 39 casos de teste em programas `.tpp` e saídas esperadas `.lex.out`.

---

## 2. Tratamento de Comentários Não Fechados (`ERR-LEX-UNC-COMMENT`)

### Problema Identificado
A regra padrão `t_COMENTARIO` utilizava a expressão `r"(\{((.|\n)*?)\})"`, exigindo obrigatoriamente a chave de fechamento `\}`. Quando um comentário era aberto com `{` mas não era fechado antes do fim do arquivo (`EOF`), a regra falhava e o PLY tentava tokenizar o texto do comentário, gerando erros de caractere inválido (`ERR-LEX-INV-CHAR`).

### Solução Implementada (`tpplex.py`)

#### 1. Regra para Comentário Não Fechado:
```python
def t_COMENTARIO_NAO_FECHADO(t):
    r'\{[^}]*$'
    column = define_column(t.lexer.lexdata, t.lexpos)
    message = le.newError(check_key, 'ERR-LEX-UNC-COMMENT', t.lineno, column)
    print(message)
    t.lexer.lineno += t.value.count('\n')
```
* **Como funciona:** A ER `r"\{[^}]*$"` busca o caractere `{` seguido de qualquer caractere diferente de `\}` até o fim da entrada (`$`). Caso o comentário seja fechado antes do `EOF`, a regra `t_COMENTARIO` tem precedência/correspondência adequada.

#### 2. Ajuste do Cache do PLY (`lextab.py`):
- O PLY compila e salva tabelas em `lextab.py` quando instanciado com `optimize=True`. Durante o desenvolvimento de novas regras, alterou-se para `lexer = lex.lex(optimize=False, debug=True, debuglog=log)` para evitar a execução de regras salvas em cache desatualizado.

#### 3. Ajuste do Processamento da CLI em `main()`:
- A verificação antiga `if len(sys.argv) < 3` impedia a execução simples `python tpplex.py arquivo.tpp` sem a flag `-k`. A lógica foi refatorada para validar a presença do arquivo independentemente da flag `-k`:
  - `python tpplex.py` (Sem arquivo) $\rightarrow$ Retorna `ERR-LEX-USE` (`"Uso: python tpplex.py file.tpp"`).
  - `python tpplex.py teste.c` (Extensão errada) $\rightarrow$ Retorna `ERR-LEX-NOT-TPP` (`"Não é um arquivo .tpp."`).
  - `python tpplex.py tests/lex-test-039.tpp` $\rightarrow$ Executa e formata o erro completo ou chave dependendo da flag `-k`.
  - `python tpplex.py tests/lex-test-100.tpp` $\rightarrow$ Retorna `ERR-LEX-FILE-NOT-EXISTS` ou a mensagem `Arquivo .tpp não existe.`

---

## 3. Abordagens Alternativas para o Ensino da Análise Léxica

Apresentar diferentes abordagens aos alunos conecta a teoria de Linguagens Formais e Autômatos com a Engenharia de Compiladores.

### Abordagem A: Tabela Pré-definida & Tabela de Símbolos
- **Conceito:** O autômato possui uma única ER genérica para palavras `[a-zA-Z_][a-zA-Z0-9_]*`. Ao identificar uma palavra, pesquisa-se em um dicionário estático de palavras reservadas. Se não for encontrada, classifica-se como `ID` e instala-se na Tabela de Símbolos.

```python
PALAVRAS_RESERVADAS = {
    "se": "SE", "então": "ENTAO", "senão": "SENAO",
    "fim": "FIM", "inteiro": "INTEIRO", "retorna": "RETORNA"
}

tabela_de_simbolos = {}

def processar_palavra(lexema, linha, coluna):
    # 1. Consulta Palavras Reservadas
    if lexema in PALAVRAS_RESERVADAS:
        return (PALAVRAS_RESERVADAS[lexema], lexema)
    
    # 2. Se não for reservada, instala na Tabela de Símbolos como ID
    if lexema not in tabela_de_simbolos:
        tabela_de_simbolos[lexema] = {
            "token": "ID",
            "primeira_ocorrencia": f"Linha {linha}, Coluna {coluna}"
        }
    return ("ID", lexema)
```

### Abordagem B: Autômato Finito Determinístico (AFD) Manual
- **Conceito:** Construção direta da máquina de estados em Python usando `while` + `if/elif` ou `match/case`, lendo caractere a caractere (`lookahead`).

```python
class ScannerManual:
    def __init__(self, codigo):
        self.codigo = codigo
        self.pos = 0

    def proximo_token(self):
        estado = 0
        lexema = ""

        while self.pos < len(self.codigo):
            c = self.codigo[self.pos]
            if estado == 0:
                if c.isspace():
                    self.pos += 1
                    continue
                elif c.isalpha():
                    lexema += c
                    estado = 1
                elif c.isdigit():
                    lexema += c
                    estado = 2
                elif c == '{':
                    estado = 3 # Comentário
            elif estado == 1:
                if c.isalnum() or c == '_':
                    lexema += c
                else:
                    return processar_palavra(lexema)
            elif estado == 2:
                if c.isdigit():
                    lexema += c
                else:
                    return ("NUM_INTEIRO", lexema)
            elif estado == 3:
                if c == '}':
                    self.pos += 1
                    estado = 0
                else:
                    self.pos += 1
                    continue
            self.pos += 1
        return None
```

### Abordagem C: Biblioteca Formal em Python (`automata-lib`)
- **Conceito:** Mapeamento 1:1 da 5-tupla formal $M = (Q, \Sigma, \delta, q_0, F)$ usando a biblioteca `automata-lib`.

```python
from automata.fa.dfa import DFA

afd_numeros = DFA(
    states={'q0', 'q1_int', 'q2_ponto', 'q3_float'},
    input_symbols={'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'},
    transitions={
        'q0': {c: 'q1_int' for c in '0123456789'} | {'.': 'q2_ponto'},
        'q1_int': {c: 'q1_int' for c in '0123456789'} | {'.': 'q2_ponto'},
        'q2_ponto': {c: 'q3_float' for c in '0123456789'},
        'q3_float': {c: 'q3_float' for c in '0123456789'}
    },
    initial_state='q0',
    final_states={'q1_int', 'q3_float'}
)
```

### Abordagem D: Estados Exclusivos do PLY (`states`)
- **Conceito:** Uso da pilha de estados do próprio PLY (`exclusive states`) para alternar modos de tokenização quando entra em um comentário `{`.

---

## 4. Integração de Lexers Customizados com o Parser (`ply.yacc`)

O `ply.yacc` é **completamente desacoplado** do `ply.lex`. Qualquer uma das 4 implementações pode ser integrada à segunda parte do compilador (Análise Sintática).

### O Contrato exigido pelo `ply.yacc`:
O parser exige apenas que o objeto lexer implemente:
1. `input(data)`: Método para carregar o código-fonte.
2. `token()`: Método que retorna o próximo token com atributos `.type`, `.value`, `.lineno` e `.lexpos`, ou `None` ao fim do arquivo.

### Exemplo de Adaptador (Wrapper) para `ply.yacc`:

```python
class TokenCustomizado:
    def __init__(self, type, value, lineno=1, lexpos=0):
        self.type = type
        self.value = value
        self.lineno = lineno
        self.lexpos = lexpos

class MeuLexerCustomizado:
    def input(self, data):
        self.codigo = data
        self.pos = 0

    def token(self):
        # Lógica para obter o próximo token...
        # Retorna um objeto TokenCustomizado(...) ou None no EOF
        pass
```

### Injeção no Parser:
```python
import ply.yacc as yacc

parser = yacc.yacc()
meu_lexer = MeuLexerCustomizado()

# O parser executa normalmente utilizando a sua implementação personalizada!
parser.parse(codigo_tpp, lexer=meu_lexer)
```

### Ganho Didático de Arquitetura:
Permite demonstrar aos alunos o conceito de **polimorfismo e interfaces**, mostrando que o Analisador Sintático produz a mesma árvore de sintaxe abstrata (AST) independente de qual das 4 variantes de Analisador Léxico for utilizada.

---

## 5. Análise Sintática: Ascendente (Bottom-Up) vs Descendente (Top-Down)

Apresentar as duas famílias de algoritmos sintáticos proporciona uma visão completa da teoria de compilação.

### Comparativo das Duas Estratégias

| Característica | Ascendente (Bottom-Up — `ply.yacc`) | Descendente (Top-Down — Recursivo Descendente) |
| :--- | :--- | :--- |
| **Algoritmo Base** | LR(1) / LALR(1) (Shift-Reduce). | LL(1) / Descendente Recursivo. |
| **Construção da Árvore** | Das folhas (tokens) em direção à raiz (símbolo inicial). | Da raiz (símbolo inicial) em direção às folhas (tokens). |
| **Implementação** | Gerado automaticamente via tabelas de ação/deslocamento (`ply.yacc`). | Escrito manualmente com uma função Python para cada Não-Terminal da gramática. |
| **Tratamento de Recursão** | Aceita **Recursão à Esquerda** nativamente ($A \rightarrow A \, \alpha$). | Requer eliminação de Recursão à Esquerda ($A \rightarrow \beta A'$) e Fatoração à Esquerda. |
| **Facilidade de Depuração** | Tabelas complexas geradas em `parsetab.py`. | Muito fácil: pode-se usar o debugger do Python ou `print` em cada função. |

---

### Exemplo Didático: Parser Descendente Recursivo em Python

Abaixo está uma demonstração de como construir um **Analisador Sintático Descendente Recursivo (LL(1))** manual em Python que consome o **mesmo Lexer** (seja ele PLY, manual ou com Tabela de Símbolos):

```python
class ParserDescendenteRecursivo:
    def __init__(self, lexer):
        self.lexer = lexer
        self.lookahead = None
        self.avancar()  # Carrega o primeiro token da entrada

    def avancar(self):
        """Pega o próximo token fornecido pelo Lexer"""
        self.lookahead = self.lexer.token()

    def match(self, token_esperado):
        """Valida se o token atual é o esperado e avança para o próximo"""
        if self.lookahead and self.lookahead.type == token_esperado:
            valor = self.lookahead.value
            self.avancar()
            return valor
        else:
            tipo_atual = self.lookahead.type if self.lookahead else "EOF"
            linha = getattr(self.lookahead, 'lineno', '?')
            raise SyntaxError(f"Erro Sintático [Linha {linha}]: Esperado '{token_esperado}', mas encontrado '{tipo_atual}'")

    # --- Regras da Gramática (Uma função para cada Não-Terminal) ---

    # Regra: programa -> INTEIRO ID ABRE_PARENTESE FECHA_PARENTESE bloco
    def programa(self):
        self.match("INTEIRO")
        nome_funcao = self.match("ID")
        self.match("ABRE_PARENTESE")
        self.match("FECHA_PARENTESE")
        self.bloco()
        print(f"[Top-Down] Programa com a função '{nome_funcao}' reconhecido com sucesso!")

    # Regra: bloco -> FIM
    def bloco(self):
        if self.lookahead and self.lookahead.type == "FIM":
            self.match("FIM")
        else:
            raise SyntaxError(f"Erro no bloco na linha {getattr(self.lookahead, 'lineno', '?')}")


# --- Testando o Parser Descendente com o Lexer Customizado ou PLY ---
if __name__ == "__main__":
    # Supondo 'meu_lexer' vindo de qualquer uma das 4 implementações léxicas:
    # meu_lexer.input("inteiro principal() fim")
    
    # parser = ParserDescendenteRecursivo(meu_lexer)
    # parser.programa()  # Inicia a análise pelo símbolo inicial
```

---

### Ganhos Didáticos ao Mostrar Ambas as Abordagens

1. **Rastreabilidade Teórica (Top-Down):** No Descendente Recursivo, cada nó da Árvore Sintática Abstrata equivale a uma chamada de função na pilha de execução da linguagem (`call stack`), tornando o conceito intuitivo para os alunos.
2. **Automação e Poder de Expressão (Bottom-Up):** No `ply.yacc` (LR/LALR), os alunos compreendem a eficiência das tabelas de transição *Shift-Reduce* e a capacidade de lidar com gramáticas mais complexas sem reescrita.
3. **Reaproveitamento do Lexer:** Demonstra que a **fase de Análise Léxica é 100% independente da técnica Sintática escolhida**, reforçando o princípio de modularidade em compiladores.

---

## 6. Arquitetura Modular do Compilador & Workflow no GitHub Classroom

### Problema do Modelo Atual
No modelo atual, para cada fase do projeto os alunos tem que baixar um novo repositório (`analise-lexica-code-start`, `analise-sintatica-code-start`, `analise-semantica-code-start` e `geracao-codigo-code-start`) disponibilizado via `assignments` do _Github Classroom_. Os alunos copiavam manualmente os arquivos atualizados da fase anterior para o repositório da fase atual. O que pode gerar problemas como:
- É propenso a erros de cópia pelos alunos.
- Perde o histórico de commits do Git.
- Torna impossível comparar diferentes implementações (ex: trocar `--lexer=manual` por `--lexer=ply`) em um mesmo projeto executável.

---

### Proposta de Arquitetura Modular (Monorepo Incremental)

Em vez de múltiplos repositórios isolados, utiliza-se a estrutura de **Repositório Único Incremental (Monorepo)** usando o padrão de projeto **Factory / Strategy**:

```text
tppcompiler/
├── src/
│   ├── tpplexer/                  # Módulo de Análise Léxica (Fase 1)
│   │   ├── __init__.py            # Fabrica o Lexer escolhido (Factory)
│   │   ├── base.py                # Interface/Classe abstrata BaseLexer
│   │   ├── ply_lexer.py           # Versão 1: Lexer implementado com PLY lex
│   │   ├── manual_dfa.py          # Versão 2: Lexer implementado com Autômato Manual (while/match)
│   │   ├── symtable_lexer.py      # Versão 3: Lexer implementado com Autômato e Tabela de Símbolos
│   │   └── automata_lib_lexer.py  # Versão 4: Lexer implementado com Autômato com a biblioteca automata-lib
│   │
│   ├── tppparser/                 # Módulo de Análise Sintática (Fase 2)
│   │   ├── __init__.py            # Fabrica o Parser escolhido (Factory)
│   │   ├── base.py                # Interface BaseParser
│   │   ├── ply_yacc.py            # Sintático Ascendente (Bottom-Up / LALR) com PLY yacc
│   │   └── topdown_parser.py      # Sintático Descendente (Top-Down / LL1)
│   │
│   ├── tppsema/                  # Módulo de Análise Semântica (Fase 3)
│   │   └── analyzer.py
│   │
│   └── tppcodegen/               # Módulo de Geração de Código (Fase 4)
│       └── generator.py
│
├── tests/                         # Testes Automatizados (pytest)
│   ├── test_tpplexer.py
│   ├── test_tppparser.py
│   ├── test_tppsema.py
│   └── test_tppcodegen.py
│
├── tppcompiler.py                        # CLI Principal do Compilador
└── README.md
```

### Implementação da Classe Base (`src/tpplexer/base.py`)

O arquivo `base.py` define o **Contrato de Interface** abstrato para todas as 4 variantes de analisadores léxicos, além da classe padronizada `Token` necessária tanto para a suíte de testes quanto para a integração transparente com o `ply.yacc` e Parsers Customizados:

```python
# src/tpplexer/base.py
from abc import ABC, abstractmethod
from typing import Optional, List, Any


class Token:
    """
    Representação padronizada de um Token no compilador.
    Totalmente compatível com as expectativas do ply.yacc e parsers manuais.
    """
    def __init__(self, type: str, value: Any, lineno: int = 1, lexpos: int = 0):
        self.type = type
        self.value = value
        self.lineno = lineno
        self.lexpos = lexpos

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)}, line={self.lineno}, pos={self.lexpos})"

    def __eq__(self, other):
        if not isinstance(other, Token):
            return False
        return (self.type == other.type and 
                self.value == other.value and 
                self.lineno == other.lineno)


class BaseLexer(ABC):
    """
    Classe Abstrata que define a interface obrigatória de todos os Lexers.
    """

    @abstractmethod
    def input(self, data: str) -> None:
        """
        Carrega a string do código-fonte TPP no lexer.
        """
        pass

    @abstractmethod
    def token(self) -> Optional[Token]:
        """
        Retorna o próximo Token da entrada ou None quando atingir o Fim de Arquivo (EOF).
        """
        pass

    def tokenize(self, data: str) -> List[Token]:
        """
        Método utilitário que consome toda a entrada e retorna a lista de Tokens.
        Muito útil para a suíte de testes automatizados e impressão na CLI.
        """
        self.input(data)
        tokens = []
        while True:
            tok = self.token()
            if tok is None:
                break
            tokens.append(tok)
        return tokens

    @staticmethod
    def get_column(data: str, lexpos: int) -> int:
        """
        Calcula a coluna (1-indexed) a partir da posição lexpos no texto.
        """
        begin_line = data.rfind('\n', 0, lexpos) + 1
        return (lexpos - begin_line) + 1
```

#### Exemplo de Herança no `ply_lexer.py`:

```python
# src/tpplexer/ply_lexer.py
import ply.lex as lex
from .base import BaseLexer, Token

class PLYLexer(BaseLexer):
    tokens = ["ID", "NUM_INTEIRO", "MAIS", "MENOS", ...]
    # Definição das regras de PLY...

    def __init__(self):
        self.lexer = lex.lex(module=self, optimize=False)

    def input(self, data: str) -> None:
        self.lexer.input(data)

    def token(self) -> Optional[Token]:
        tok = self.lexer.token()
        if tok is None:
            return None
        # Converte o LexToken do PLY para o Token padronizado da nossa base
        return Token(tok.type, tok.value, tok.lineno, tok.lexpos)
```

---

### Padrão Factory para Seleção Dinâmica via CLI (`main.py`)

No arquivo `src/tpplexer/__init__.py`, cria-se a fábrica de lexers:

```python
# src/tpplexer/__init__.py
from .ply_lexer import PLYLexer
from .manual_dfa import ManualDFALexer
from .symtable_lexer import SymbolTableLexer

def get_lexer(strategy="ply"):
    strategy = strategy.lower()
    if strategy == "ply":
        return PLYLexer()
    elif strategy == "manual":
        return ManualDFALexer()
    elif strategy == "symtable":
        return SymbolTableLexer()
    else:
        raise ValueError(f"Estratégia léxica desconhecida: '{strategy}'")
```

E no `tppcompiler.py` principal, o aluno/professor pode alternar qualquer combinação com argumentos CLI:

```python
# tppcompiler.py
import argparse
from src.lexer import get_lexer
from src.parser import get_parser

def main():
    cli = argparse.ArgumentParser(description="Compilador TPP Modular")
    cli.add_argument("fonte", help="Arquivo-fonte .tpp")
    cli.add_argument("--lexer", choices=["ply", "manual", "symtable"], default="ply", help="Estratégia Léxica")
    cli.add_argument("--parser", choices=["yacc", "topdown"], default="yacc", help="Estratégia Sintática")
    
    args = cli.parse_args()

    # 1. Instancia o Lexer e o Parser dinamicamente
    lexer = get_lexer(args.lexer)
    parser = get_parser(args.parser, lexer=lexer)

    # 2. Executa a compilação
    with open(args.fonte) as f:
        codigo = f.read()

    ast = parser.parse(codigo)
    print(f"Compilação concluída usando Léxico [{args.lexer.upper()}] + Sintático [{args.parser.upper()}]!")

if __name__ == "__main__":
    main()
```

#### Exemplo de Execução no Terminal pelos Alunos:
```bash
# Testar combinação PLY + YACC
python main.py programa.tpp --lexer=ply --parser=yacc

# Testar combinação Autômato Manual + Sintático Descendente
python main.py programa.tpp --lexer=manual --parser=topdown
```

---

### Estratégia de Gerenciamento no GitHub Classroom

Para evitar que o aluno tenha que copiar arquivos manualmente entre fases, recomendam-se duas estratégias no GitHub Classroom:

#### Estratégia A: Repositório Único por Semestre (Recomendada)
1. O aluno cria **um único repositório** no GitHub Classroom no início do semestre (ex: `tppcompiler-nomealuno`).
2. **Fase 1 (Léxica):** O repositório inicial contém apenas o esqueleto de `src/tpplexer/` e os testes de léxico em `tests/test_lexer.py`.
3. **Fase 2 (Sintática):** No GitHub Classroom, você publica a *Assignment 2* apontando para uma nova **Branch** (ex: `analise-sintatica-code-start`) ou abre um _Pull Request_ no repositório do aluno adicionando a pasta `src/parser/` e os testes sintáticos `tests/test_parser.py`.
4. **Resultado:** O aluno não copia nada; apenas dá `git pull` ou resolve o _merge_ no seu próprio repositório, mantendo 100% do histórico e os _lexers_ implementados anteriormente.

#### Estratégia B: Atualização via `git remote` (Template Upstream)
Se você mantiver um repositório modelo (Template) no GitHub:
1. Quando a Fase 2 (Sintática) iniciar, você faz o _commit_ dos novos arquivos de esqueleto sintático no seu repositório _Template_.
2. O aluno roda no terminal dele apenas dois comandos:
   ```bash
   git remote add template https://github.com/rogerioag/tppcompiler-template.git
   git pull template main --allow-unrelated-histories
   ```
3. O Git faz o merge automático dos novos diretórios (`src/tppparser/`) preservando todo o trabalho que o aluno fez na pasta `src/tpplexer/`.

#### Estratégia C: Subprojetos com Git Submodules (Uma Assignment por Fase no GitHub Classroom)
Se você preferir manter um **Assignment separado no GitHub Classroom para cada fase** (ex: `tpplexer`, `tppparser`, `tppsema`, `tppcodegen`), pode-se usar **Git Submodules**:

1. **Estrutura:** O repositório principal `tppcompiler` possui submódulos Git apontando para os repositórios individuais de cada fase:

   - `src/tpplexer/` $\rightarrow$ submódulo ligado ao repositório `tpplexer-aluno`
   - `src/tppparser/` $\rightarrow$ submódulo ligado ao repositório `tppparser-aluno`
   - `src/tppsema/` $\rightarrow$ submódulo ligado ao repositório `tppsema-aluno`
   - `src/tppcodegen/` $\rightarrow$ submódulo ligado ao repositório `tppcodegen-aluno`

2. **Como o aluno vincula cada fase:**

   - **Na Fase 1:**
     
     ```bash
     git clone https://github.com/turma-compiladores/tppcompiler.git tppcompiler-aluno
     cd tppcompiler-aluno
     git submodule add https://github.com/turma-compiladores/tpplexer-code-start.git src/tpplexer
     ```
   - **Na Fase 2:**
     
     ```bash
     git submodule add https://github.com/turma-compiladores/tppparser-code-start.git src/tppparser
     ```

   **Na Fase 3:**

   ```bash
   git submodule add https://github.com/turma-compiladores/tppsema-code-start.git src/tppsema
   ```

   **Na Fase 4:**

   ```bash
   git submodule add https://github.com/turma-compiladores/tppcodegen-code-start.git src/tppcodegen
   ```

3. **Arquivo `.gitmodules` gerado:**

   ```ini
   [submodule "src/tpplexer"]
   	path = src/tpplexer
   	url = https://github.com/turma-compiladores/tpplexer-code-start.git
   
   [submodule "src/tppparser"]
   	path = src/tppparser
   	url = https://github.com/turma-compiladores/tppparser-code-start.git
   
   [submodule "src/tppsema"]
   	path = src/tppsema
   	url = https://github.com/turma-compiladores/tppsema-code-start.git
   	
   [submodule "src/tppcodegen"]
   	path = src/tppcodegen
   	url = https://github.com/turma-compiladores/tppcodegen-code-start.git
   ```

4. **Vantagem:** O GitHub Classroom continua avaliando cada repositório isoladamente (`tpplexer` tem sua nota no _autograder_ do Classroom, `tppparser` tem a sua), enquanto o repositório principal `tppcompiler` integra tudo em um compilador executável!

---

### Benefícios dessa Solução

1. **Zero Cópias Manuais:** Elimina totalmente o "copia e cola" entre projetos.
2. **Flexibilidade e Comparação:** Os alunos conseguem executar baterias de testes comparando performance ou comportamento entre `--lexer=ply` vs `--lexer=manual` no mesmo projeto.
3. **Prática Profissional:** Ensina os alunos a trabalharem com **Padrões de Projeto (Factory/Strategy)**, **CLI com `argparse`**, **Testes Automatizados Modulares** e **Gerenciamento Avançado do Git (Submodules/Branches)**.



Criar forks do repositório do professor e usar upstreams.

https://docs.github.com/en/pull-requests/how-tos/work-with-forks/fork-a-repo



In GitHub, **"upstream"** usually refers to the **original repository** that you forked. When you create a personal copy (a fork) of someone else's project, your copy is called **"origin"**, while the main repository where the project lives is called **"upstream"**. [[1](https://codingarchitect.dev/blog/understanding-the-terms-upstream-vs-origin-used-with-github/), [2](https://www.geeksforgeeks.org/git/how-to-add-upstream-in-git/)]

Alternatively, "upstream" can also refer to a **tracking branch** on a remote server that your local git branch connects to. [[1](https://stackoverflow.com/questions/9257533/what-is-the-difference-between-origin-and-upstream-on-github), [2](https://codingarchitect.dev/blog/understanding-the-terms-upstream-vs-origin-used-with-github/)]

Here is how to manage both types of upstream configurations.

1. Syncing a Fork (The Original Project Repo)

To keep your GitHub fork updated with new code from the original creator, you must tell your local Git where that original "upstream" repository is located. [[1](https://docs.github.com/pt/pull-requests/collaborating-with-pull-requests/working-with-forks/configuring-a-remote-repository-for-a-fork), [2](https://www.geeksforgeeks.org/git/how-to-add-upstream-in-git/)]

- **Add the upstream connection:** Copy the URL of the original main repository and run:

  bash

  ```
  git remote add upstream https://github.com/ORIGINAL-OWNER/ORIGINAL-REPOSITORY.git
  ```

  Use o código com cuidado.

- 

- **Verify your remotes:** Check that both `origin` (your copy) and `upstream` (their copy) are listed:

  bash

  ```
  git remote -v
  ```

  Use o código com cuidado.

- **Fetch and merge upstream updates:** Pull down the newest changes from the original repository to your local computer:

  bash

  ```
  git fetch upstream
  git checkout main
  git merge upstream/main
  ```

  Use o código com cuidado.

   [[1](https://docs.github.com/en/pull-requests/how-tos/work-with-forks/configuring-a-remote-repository-for-a-fork), [2](https://docs.github.com/articles/fork-a-repo), [3](https://medium.com/@nynptel/difference-between-origin-and-upstream-for-a-git-repository-67e0a7f1a90e), [4](https://www.linkedin.com/pulse/git-github-demystified-guide-open-source-contribution-nishan-baral-i4ndc), [5](https://carpentries.github.io/maintainer-onboarding/06-git-workflow.html)]

- Setting an Upstream Branch (Tracking Remote Branches)

When you create a brand-new branch on your local computer, Git doesn't automatically know where to upload it on GitHub. You need to link your local branch to a remote tracking branch (the upstream branch). [[1](https://stackoverflow.com/questions/9257533/what-is-the-difference-between-origin-and-upstream-on-github), [2](https://www.youtube.com/watch?v=wBc0WcyTtOA), [3](https://codingarchitect.dev/blog/understanding-the-terms-upstream-vs-origin-used-with-github/), [4](https://medium.com/@pradeepdevops81/real-git-problems-we-actually-hit-and-how-we-solved-them-fcddf0a9d666)]

- **Push a new branch and set its upstream:** Use the `-u` flag the first time you push your branch. This links them permanently so you can just type `git push` or `git pull` in the future.

  bash

  ```
  git push -u origin feature-branch
  ```

  Use o código com cuidado.

- **Link an existing local branch to an existing remote branch:** If the branch already exists on GitHub, track it with:

  ```bash
  git branch --set-upstream-to=origin/feature-branch
  ```

  Use o código com cuidado.

   [[1](https://stackoverflow.com/questions/9257533/what-is-the-difference-between-origin-and-upstream-on-github), [2](https://graphite.com/guides/git-set-upstream), [3](https://graphite.com/guides/git-push-u-origin-command-guide), [4](https://nyu-dataservices.gitlab.io/rdm-instruction/intro-to-git-and-github.html), [5](https://www.reddit.com/r/git/comments/g3cr6h/trying_to_understand_the_git_process_flow/)]

**Origin vs. Upstream Comparison**

| Term         | What it Represents                                           | Common Use Case                                            |
| ------------ | ------------------------------------------------------------ | ---------------------------------------------------------- |
| **Origin**   | Your personal, copied version of the repository hosted on GitHub. | Where you push your code, experiment, and create branches. |
| **Upstream** | The primary project repository owned by the original authors. | Where you fetch the latest official project updates.       |

To learn more about working with community projects, you can read the [GitHub Docs guide on configuring a remote for a fork](https://www.google.com/url?sa=i&source=web&rct=j&url=https://docs.github.com/en/pull-requests/how-tos/work-with-forks/configuring-a-remote-repository-for-a-fork&ved=2ahUKEwijpsrVpbKWAxWsrJUCHZw_AJcQy_kOegoIAggACAAIIhAC&opi=89978449&cd&psig=AOvVaw3x5XQ0s-KlC-0z1_xPre6N&ust=1787421382013000). [[1](https://docs.github.com/en/pull-requests/how-tos/work-with-forks/configuring-a-remote-repository-for-a-fork)]

What are you trying to accomplish today? I can help you **sync an outdated fork**, **push a brand new branch**, or **resolve merge conflicts** with the main repo. [[1](https://www.geos.ed.ac.uk/~smudd/NMDM_Course/html/more_advanced_github.html)]





**GitHub Docs**

+ **Configurar um repositório remoto para um fork - GitHub Docs**

Você deve configurar um remoto que aponta para o repositório upstream no Git para sincronizar alterações realizadas em um fork com...



+ **Configuring a remote repository for a fork - GitHub Docs**

To add an upstream remote in Git, you can do the following: 1. Open your terminal or Git Bash 2. List the remotes currently config...



- **Fork a repository - GitHub Docs**

  You can also clone your forked repository: 1. Navigate to your fork of the repository 2. Copy the URL for the repository 3. Open y...

  ![img](data:image/png;base64,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)

