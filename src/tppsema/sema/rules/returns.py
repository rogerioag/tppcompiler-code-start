# src/tppsema/sema/rules/returns.py
"""
Regras semânticas do item "6. Retorno múltiplo" do docs/SEM-SPECS.md:

  - 6.1 Quantidade de valores do retorna: ERR-SEM-FUNC-RET-NUM-ERROR
  - 6.2 Chamada com mais de um retorno em expressão: ERR-SEM-CALL-FUNC-MULTI-RET-IN-EXP
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
