# src/tppsema/sema/rules/coercions.py
"""
Regras semânticas do item "3. Atribuição de tipos distintos e coerções implícitas" do docs/SEM-SPECS.md:

  - WAR-SEM-ATR-DIFF-TYPES-IMP-COERC-OF-VAR, -OF-NUM, -OF-EXP, -OF-RET-VAL
  - WAR-SEM-ATR-DIFF-TYPES-IMP-COERC-OF-FUNC-ARG
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
