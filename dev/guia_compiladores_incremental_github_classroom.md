# Guia Completo: Gerenciamento Incremental de Compiladores com GitHub Classroom, Git e PLY

Este documento reúne toda a discussão técnica sobre o fluxo de desenvolvimento e entrega incremental de um compilador nas quatro fases clássicas (Léxica, Sintática, Semântica e Geração de Código), utilizando **Python (PLY)**, **GitHub Actions**, estratégias de **Git Remotes/Branches** e considerações sobre **Git Submodules**.

---

## Sumário
1. [Submódulos no Git vs. Repositórios Principais](#1-submódulos-no-git-vs-repositórios-principais)
2. [Estratégia Pedagógica para Projetos Incrementais](#2-estratégia-pedagógica-para-projetos-incrementais)
3. [Estrutura do Projeto com Python e PLY](#3-estrutura-do-projeto-com-python-e-ply)
4. [Configuração de Testes com Pytest](#4-configuração-de-testes-com-pytest)
5. [Pipeline de CI Incremental no GitHub Actions](#5-pipeline-de-ci-incremental-no-github-actions)
6. [Gerenciamento de Branches pelo Docente](#6-gerenciamento-de-branches-pelo-docente)
7. [Fluxo Operacional de Sincronização (Aluno e Docente)](#7-fluxo-operacional-de-sincronização-aluno-e-docente)
8. [Propagação de Correções Retroativas (Hotfixes)](#8-propagação-de-correções-retroativas-hotfixes)

---

## 1. Submódulos no Git vs. Repositórios Principais

Ao trabalhar com submódulos no Git, as alterações feitas dentro do submódulo **não são enviadas automaticamente** para o repositório remoto de origem ao executar `git push` no repositório pai.

### Como funciona o relacionamento
- O repositório principal armazena apenas um **ponteiro (hash do commit)** para o submódulo.
- O submódulo é um repositório Git autônomo com sua própria árvore e branches.

### Fluxo correto de alteração
1. **Commit e push no submódulo:**
   ```bash
   cd caminho/do/submodulo
   git checkout main
   git add .
   git commit -m "feat: alteração interna no submódulo"
   git push origin main
   ```
2. **Atualização do ponteiro no repositório pai:**
   ```bash
   cd ..
   git add caminho/do/submodulo
   git commit -m "chore: atualiza ponteiro do submódulo"
   git push origin main
   ```

---

## 2. Estratégia Pedagógica para Projetos Incrementais

Em vez de criar um *assignment* isolado por fase no GitHub Classroom (o que exige que os alunos fiquem copiando manualmente o código das fases anteriores), a melhor abordagem é manter **um único repositório por aluno para todo o semestre** e integrar as fases via **Git Remote Upstream**.

### Vantagens
- Histórico de commits contínuo e rastreabilidade total do desenvolvimento.
- Eliminação do trabalho manual de copiar/colar arquivos de uma fase para a outra.
- Testes de regressão contínuos (garantindo que alterações na geração de código não quebrem o analisador sintático).

---

## 3. Estrutura do Projeto com Python e PLY

```text
.
├── .github/
│   └── workflows/
│       └── autograding.yml
├── .gitignore
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── lexer.py         # Disponível na Fase 1
│   ├── parser.py        # Liberado na Fase 2
│   ├── semantic.py      # Liberado na Fase 3
│   └── codegen.py       # Liberado na Fase 4
└── tests/
    ├── conftest.py
    ├── test_phase1_lexer.py
    ├── test_phase2_parser.py
    ├── test_phase3_semantic.py
    └── test_phase4_codegen.py
```

### Arquivo `.gitignore` Recomendado
Evita que arquivos gerados pelo PLY (`parsetab.py`, `parser.out`) ou caches locais entrem no controle de versão:
```gitignore
__pycache__/
*.pyc
parsetab.py
parser.out
.pytest_cache/
```

---

## 4. Configuração de Testes com Pytest

### `tests/conftest.py`
Configura o `sys.path` automaticamente para importar o pacote `src/`:
```python
import sys
from pathlib import Path

# Adiciona o diretório src/ ao sys.path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
```

### `tests/test_phase1_lexer.py` (Exemplo para Analisador Léxico)
```python
import pytest
from lexer import lexer

def tokenize(input_code):
    lexer.input(input_code)
    return [(tok.type, tok.value) for tok in iter(lexer.token, None)]

def test_keywords_and_identifiers():
    code = "if x then y else 42"
    tokens = tokenize(code)
    expected = [
        ("IF", "if"),
        ("ID", "x"),
        ("THEN", "then"),
        ("ID", "y"),
        ("ELSE", "else"),
        ("INT_CONST", 42),
    ]
    assert tokens == expected

def test_illegal_character_handling():
    code = "let a = @;"
    with pytest.raises(Exception):
        tokenize(code)
```

---

## 5. Pipeline de CI Incremental no GitHub Actions

O arquivo `.github/workflows/autograding.yml` verifica a existência dos arquivos de teste de cada fase usando `hashFiles()`. Conforme novas fases são integradas, as suítes respectivas são ativadas em sequência:

```yaml
name: Avaliacao PLY Compiler

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout do repositório
        uses: actions/checkout@v4

      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: "pip"

      - name: Instalar dependências
        run: |
          python -m pip install --upgrade pip
          pip install ply pytest

      # ==========================================
      # FASE 1: Léxico (lexer.py)
      # ==========================================
      - name: Testes da Fase 1 - Léxico
        if: hashFiles('tests/test_phase1_lexer.py') != ''
        run: pytest tests/test_phase1_lexer.py -v

      # ==========================================
      # FASE 2: Sintático (parser.py)
      # ==========================================
      - name: Testes da Fase 2 - Sintático
        if: hashFiles('tests/test_phase2_parser.py') != ''
        run: pytest tests/test_phase2_parser.py -v

      # ==========================================
      # FASE 3: Semântico (semantic.py)
      # ==========================================
      - name: Testes da Fase 3 - Semântico
        if: hashFiles('tests/test_phase3_semantic.py') != ''
        run: pytest tests/test_phase3_semantic.py -v

      # ==========================================
      # FASE 4: Geração de Código (codegen.py)
      # ==========================================
      - name: Testes da Fase 4 - CodeGen
        if: hashFiles('tests/test_phase4_codegen.py') != ''
        run: pytest tests/test_phase4_codegen.py -v
```

---

## 6. Gerenciamento de Branches pelo Docente

No repositório template privado/docente, estruture uma cadeia linear de branches:

```bash
# 1. Configurar branch base (Fase 1 - Léxico)
git checkout -b main
git add .
git commit -m "feat: release Phase 1 - Lexer skeleton and tests"

# 2. Criar Fase 2 (Sintático) a partir da Fase 1
git checkout -b phase2-parser
# Adicionar src/parser.py, tests/test_phase2_parser.py
git add .
git commit -m "feat: release Phase 2 - Parser skeleton and tests"

# 3. Criar Fase 3 (Semântico) a partir da Fase 2
git checkout -b phase3-semantic
# Adicionar src/semantic.py, tests/test_phase3_semantic.py
git add .
git commit -m "feat: release Phase 3 - Semantic skeleton and tests"

# 4. Criar Fase 4 (Geração de Código) a partir da Fase 3
git checkout -b phase4-codegen
# Adicionar src/codegen.py, tests/test_phase4_codegen.py
git add .
git commit -m "feat: release Phase 4 - CodeGen skeleton and tests"

# 5. Enviar branches para o repositório remoto
git push origin main phase2-parser phase3-semantic phase4-codegen
```

---

## 7. Fluxo Operacional de Sincronização (Aluno e Docente)

### Liberação da Fase pelo Professor
Quando chegar a data de início da Fase 2 (Parser):
```bash
git checkout main
git merge phase2-parser -m "Release Phase 2: Parser skeleton & tests"
git push origin main
```

### Configuração e Atualização pelo Aluno

1. **Configurar o remote upstream (apenas uma vez no início do semestre):**
   ```bash
   git remote add upstream https://github.com/sua-organizacao/compiler-template.git
   ```

2. **Obter a nova fase:**
   
   ```bash
   git fetch upstream
   git merge upstream/main -m "Merge upstream Phase 2"
   git push origin main
   ```

---

## 8. Propagação de Correções Retroativas (Hotfixes)

Caso precise corrigir enunciados, templates ou testes de fases anteriores no meio do semestre:

```bash
# Corrigir o problema na branch principal
git checkout main
git commit -am "fix(tests): corrige caso de teste no lexer"
git push origin main

# Propagar a correção em cascata para as branches futuras
git checkout release-fase-2-tppparser && git merge main && git push origin release-fase-2-tppparser
git checkout phase3-semantic && git merge phase2-parser && git push origin phase3-semantic
git checkout phase4-codegen && git merge phase3-semantic && git push origin phase4-codegen
```






```bash
[rag@backporting tppcompiler-code-start]$ git checkout main && git commit -a -m "Fixing specifications." && git push origin main
M       docs/LEX-SPECS.md
Mudou para o branch 'main'
Seu branch está atualizado com 'origin/main'.
[main 6caa44d] Fixing specifications.
 1 file changed, 11 insertions(+), 19 deletions(-)
Enumerando objetos: 7, concluído.
Contando objetos: 100% (7/7), concluído.
Compressão delta usando até 16 threads
Comprimindo objetos: 100% (4/4), concluído.
Escrevendo objetos: 100% (4/4), 473 bytes | 473.00 KiB/s, concluído.
Total 4 (delta 3), reutilizados 0 (delta 0), pack reutilizados 0 (de 0)
remote: Resolving deltas: 100% (3/3), completed with 3 local objects.
To https://github.com/rogerioag/tppcompiler-code-start.git
   793c56a..6caa44d  main -> main
[rag@backporting tppcompiler-code-start]$ git checkout release-fase-2-tppparser && git merge main && git push origin release-fase-2-tppparser
Mudou para o branch 'release-fase-2-tppparser'
Seu branch está atualizado com 'origin/release-fase-2-tppparser'.
Atualizando 793c56a..6caa44d
Fast-forward
 docs/LEX-SPECS.md | 30 +++++++++++-------------------
 1 file changed, 11 insertions(+), 19 deletions(-)
Total 0 (delta 0), reutilizados 0 (delta 0), pack reutilizados 0 (de 0)
To https://github.com/rogerioag/tppcompiler-code-start.git
   793c56a..6caa44d  release-fase-2-tppparser -> release-fase-2-tppparser
[rag@backporting tppcompiler-code-start]$ 

```

```bash
git checkout release-fase-2-tppparser && git merge main && git push origin release-fase-2-tppparser

git commit -am "fixing Syn-specs"
git push origin release-fase-2-tppparser
```

## Criação da fase 3: Semântica

```bash
git checkout -b release-fase-3-tppsema
# Adicionar arquivos da semântica.
git add .
git commit -m "feat: release Fase 3 - Semântica code start."
```

