# src/tppsema/sema/rules/variables.py
"""
Regras semânticas do item "2. Variáveis" do docs/SEM-SPECS.md:

  - 2.1 Variável não declarada: ERR-SEM-VAR-NOT-DECL
  - Declarada e não inicializada: WAR-SEM-VAR-DECL-NOT-INIT
  - Declarada e não utilizada: WAR-SEM-VAR-DECL-NOT-USED, WAR-SEM-VAR-DECL-INIT-NOT-USED
  - Declarada mais de uma vez: WAR-SEM-VAR-DECL-PREV
"""


def verificar(arvore, tabela, sema):
    """
    Verifica as regras deste item na árvore sintática.

    arvore: raiz da árvore sintática (nó 'programa').
    tabela: tabela de símbolos (TabelaSimbolos).
    sema:   analisador semântico; use sema.emitir(chave, *args, linha=..., coluna=...)
            para imprimir os erros e avisos.
    """
    # TODO (alunos): implementar as verificações deste item.
    pass
