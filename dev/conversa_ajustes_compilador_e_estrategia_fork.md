# Ajustes no Compilador TPP e Estratégia de Desenvolvimento Incremental com Git

**Data:** 23 de Setembro de 2026  
**Projeto:** `tppcompiler-code-start` / Compilador TPP  
**Ambiente:** Linux / Python 3.14 / PLY / Pytest  

---

## Sumário
1. [Exibição da Chave `ERR-GLOB-USE` com a Opção `-k`](#1-exibição-da-chave-err-glob-use-com-a-opção--k)
2. [Ordem Cronológica de Tokens e Erros Léxicos (`lex-test-002.tpp`)](#2-ordem-cronológica-de-tokens-e-erros-léxicos-lex-test-002tpp)
3. [Compatibilidade do Iterador do Lexer com o Yacc (Sintático)](#3-compatibilidade-do-iterador-do-lexer-com-o-yacc-sintático)
4. [Correção da Execução dos Testes no `pytest` (`path_file`)](#4-correção-da-execução-dos-testes-no-pytest-path_file)
5. [Estratégia de Desenvolvimento Incremental Baseada em Fork / Upstream (Substituição do GitHub Classroom)](#5-estratégia-de-desenvolvimento-incremental-baseada-em-fork--upstream-substituição-do-github-classroom)

---

## 1. Exibição da Chave `ERR-GLOB-USE` com a Opção `-k`

### Contexto e Problema
Ao executar o compilador sem fornecer o arquivo-fonte obrigatório `fonte`:
```bash
python src/tpp_compiler.py --lexer ply -k
```
O `argparse` padrão emitia a mensagem completa de uso para o `stderr` e encerrava com código de saída 2:
```text
usage: tpp_compiler.py [-h] [--lexer {ply,manual,symtable}] [--parser {yacc,topdown}] [--sema SEMA]
                       [--gencode GENCODE] [-k]
                       fonte
tpp_compiler.py: error: the following arguments are required: fonte
```
O comportamento desejado era que, quando a opção `-k` estivesse presente na linha de comando, fosse exibida apenas a chave de erro padronizada:
```text
ERR-GLOB-USE
```
Porém, se a opção `-k` **não** estivesse presente, a mensagem padrão de uso do `argparse` deveria ser mantida.

### Solução Implementada em `src/tpp_compiler.py`
Foi criada uma subclasse customizada de `argparse.ArgumentParser` sobrescrevendo o método `error()`:

```python
class ArgumentParser(argparse.ArgumentParser):
    def parse_args(self, args=None, namespace=None):
        self._current_args = args if args is not None else sys.argv[1:]
        return super().parse_args(args=args, namespace=namespace)

    def error(self, message):
        current_args = getattr(self, '_current_args', sys.argv[1:])
        if "-k" in current_args:
            ge = MyError('GlobalErrors')
            print(ge.newError(True, 'ERR-GLOB-USE'))
            sys.exit(0)
        super().error(message)
```

E no fluxo principal de `main()`:
```python
    if not args.fonte or not args.fonte.strip():
        print(ge.newError(check_key, 'ERR-GLOB-USE'))
        return
```

### Validação
- **Com `-k`:**
  ```bash
  $ python src/tpp_compiler.py --lexer ply -k
  ERR-GLOB-USE
  ```
- **Sem `-k`:**
  ```bash
  $ python src/tpp_compiler.py --lexer ply
  usage: tpp_compiler.py [-h] [--lexer {ply,manual,symtable}] ... fonte
  tpp_compiler.py: error: the following arguments are required: fonte
  ```

---

## 2. Ordem Cronológica de Tokens e Erros Léxicos (`lex-test-002.tpp`)

### Contexto e Problema
No arquivo de teste `tests/lex-tests/lex-test-002.tpp`:
```text
inteiro: a,b
ç
```
O caractere inválido `ç` encontra-se na linha 2, após a declaração `inteiro: a,b` da linha 1.

A saída gerada estava colocando o erro no topo:
```text
ERR-LEX-INV-CHAR
INTEIRO
DOIS_PONTOS
ID
VIRGULA
ID
```
Quando a saída esperada e correta era:
```text
INTEIRO
DOIS_PONTOS
ID
VIRGULA
ID
ERR-LEX-INV-CHAR
```

### Causa Raiz
No arquivo `src/tpplexer/ply_lexer/ply_lexer.py`, o método `get_tokens()` consumia todos os tokens de uma só vez convertendo-os em lista:
```python
# Versão anterior com problema:
def get_tokens(self, data: str):
    self.input(data)
    return list(iter(self.token, None))  # <-- Criava a lista inteira na memória
```

Enquanto a lista era montada, ao ler o `ç`, o PLY disparava `t_error()`, que executava `print(message)` diretamente no `stdout`. Somente depois que toda a lista de tokens terminava é que o loop `for token in ...` em `tpp_compiler.py` imprimia os tokens regulares (`INTEIRO`, `DOIS_PONTOS`, etc.).

### Solução Implementada em `src/tpplexer/ply_lexer/ply_lexer.py`
O método `get_tokens()` foi alterado para retornar um **iterador preguiçoso (lazy)**:

```python
    def get_tokens(self, data: str):
        """
        Retorna o iterador de tokens sob demanda para o código-fonte fornecido.
        """
        self.input(data)
        return iter(self.token, None)
```

Dessa forma:
1. `INTEIRO`, `DOIS_PONTOS`, `ID`, `VIRGULA`, `ID` são lidos e impressos linha a linha.
2. Na linha 2, ao pedir o próximo token, o PLY detecta `ç` e imprime `ERR-LEX-INV-CHAR`.
3. A saída segue a ordem cronológica exata do código-fonte.

---

## 3. Compatibilidade do Iterador do Lexer com o Yacc (Sintático)

### Pergunta
*A alteração de `get_tokens()` para iterador vai funcionar com o PLY Yacc?*

### Resposta e Análise Técnica
**Sim, funciona perfeitamente.**

1. **O Yacc nunca chama `get_tokens()`**: O `ply.yacc` (ao executar `parser.parse(codigo, lexer=lexer)`) interage exclusivamente via método **`lexer.token()`** passo a passo, sob demanda, conforme realiza as ações de *shift* e *reduce*.
2. **O método `token()` permaneceu inalterado**:
   ```python
   def token(self) -> Optional[Token]:
       tok = self.lexer.token()
       if tok is None:
           return None
       return Token(type=tok.type, value=tok.value, lineno=tok.lineno, lexpos=tok.lexpos)
   ```
3. O `get_tokens()` é apenas um utilitário de alto nível usado pela CLI (`tpp_compiler.py`) e por scripts de teste.

---

## 4. Correção da Execução dos Testes no `pytest` (`path_file`)

### Problema Observado
Após parametrizar os testes em `tests/tpplex_test.py`:
```python
@pytest.mark.parametrize("lexer_type, key_option, input_file", test_cases)
def test_execute(lexer_type, key_option, input_file):
    if(input_file != ''):
        path_file = 'tests/lex-tests/' + input_file
    else:
        path_file = ""
    
    cmd = "python src/tpp_compiler.py --lexer {0} {1} {2}".format(lexer_type, key_option, input_file)
```
39 dos 42 testes falharam com `ERR-GLOB-FILE-NOT-EXISTS`.

### Causa
O comando estava recebendo `input_file` (ex: `lex-test-001.tpp`) em vez de `path_file` (ex: `tests/lex-tests/lex-test-001.tpp`). Como o arquivo não existia na raiz do projeto, o compilador reportava que o arquivo não existia.

### Solução
Substituição na chamada de formatação do comando:
```python
cmd = "python src/tpp_compiler.py --lexer {0} {1} {2}".format(lexer_type, key_option, path_file)
```
Resultado: **42 testes passaram com 100% de sucesso**.

---

## 5. Estratégia de Desenvolvimento Incremental Baseada em Fork / Upstream (Substituição do GitHub Classroom)

Devido à descontinuação do **GitHub Classroom**, foi definida uma estratégia padrão da indústria usando **Git Remote Upstream** e **GitHub Template Repository**.

### 5.1. Prevenção de Plágio: Template Privado vs. Fork Público
No GitHub, um *Fork* de um repositório público é obrigatoriamente público. Para garantir que os repositórios dos estudantes sejam privados:
1. No repositório base do professor (`tppcompiler-code-start`), ativa-se a opção **Template Repository**.
2. O aluno clica em **"Use this template"** $\rightarrow$ **"Create a new repository"** e cria seu repositório como **Privado**.
3. O aluno adiciona o repositório do professor como `upstream`:
   ```bash
   git remote add upstream https://github.com/rogerioag/tppcompiler-code-start.git
   ```

### 5.2. Estrutura Modular das Fases
O projeto foi estruturado de forma aditiva para evitar conflitos de merge entre fases:
```text
tppcompiler-code-start/
├── src/
│   ├── tpp_compiler.py        # CLI principal (compartilhado)
│   ├── myerror.py             # Tratamento de erros (compartilhado)
│   ├── tpplexer/              # [Fase 1 - Léxico]
│   ├── tppparser/             # [Fase 2 - Sintático: esqueleto + regras liberadas na F2]
│   ├── tppsema/               # [Fase 3 - Semântico: esqueleto liberado na F3]
│   └── tppcodegen/            # [Fase 4 - Geração de Código: esqueleto liberado na F4]
├── tests/
│   ├── tpplex_test.py         # Testes da Fase 1
│   ├── tppparser_test.py      # Testes da Fase 2 (adicionado na Fase 2)
│   ├── tppsema_test.py        # Testes da Fase 3 (adicionado na Fase 3)
│   └── tppcodegen_test.py     # Testes da Fase 4 (adicionado na Fase 4)
└── docs/                      # Relatório acumulativo em PDF
```

### 5.3. Fluxo do Docente
- O professor pode manter branches preparadas: `release-fase-2`, `release-fase-3`, etc.
- No lançamento de cada fase (ou envio de hotfixes em testes):
  ```bash
  git checkout main
  git merge release-fase-2 -m "feat: release Fase 2 - Analisador Sintático"
  git push origin main
  ```

### 5.4. Fluxo do Estudante
1. **Configuração Inicial:**
   ```bash
   git clone https://github.com/<aluno>/tppcompiler-<aluno>.git
   cd tppcompiler-<aluno>
   git remote add upstream https://github.com/rogerioag/tppcompiler-code-start.git
   ```
2. **Desenvolvimento e Entrega da Fase:**
   O aluno implementa no diretório da fase correspondente (ex: `src/tpplexer/`), testa localmente com `pytest` e faz push:
   ```bash
   git add .
   git commit -m "feat: Implementação da Análise Léxica"
   git push origin main
   ```
3. **Recebimento da Próxima Fase (ou Hotfixes):**
   ```bash
   git pull upstream main --no-rebase -m "Merge Fase 2 do professor"
   git push origin main
   ```
   *Como os novos módulos adicionam pastas/arquivos distintos, a integração é automática e sem conflitos.*

### 5.5. CI Contínuo com GitHub Actions
Foi definida a pipeline `.github/workflows/tests.yml` com condicional `if: hashFiles(...) != ''` para executar progressivamente apenas os testes das fases já liberadas.

---
*Documento gerado automaticamente para registro de arquitetura e decisões de projeto.*
