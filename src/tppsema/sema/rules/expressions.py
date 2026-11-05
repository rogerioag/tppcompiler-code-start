# src/tppsema/sema/rules/expressions.py
"""
Regras semânticas do item "7. Expressões" do docs/SEM-SPECS.md:

  - 7.1 Comando sem efeito: WAR-SEM-EXP-STMT-NO-EFFECT
  - 7.2 Comparações encadeadas: WAR-SEM-REL-CHAIN
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
