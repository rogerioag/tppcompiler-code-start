# src/tppsema/sema/rules/assignments.py
"""
Regras semânticas do item "5. Atribuição múltipla, encadeada e tuplas" do docs/SEM-SPECS.md:

  - 5.1 Alvos da atribuição: ERR-SEM-ATR-INVALID-TARGET
  - 5.2 Quantidade de alvos e de valores: ERR-SEM-ATR-DIFF-NUM-TARGETS-VALUES
  - 5.3 Tuplas fora da atribuição: ERR-SEM-TUPLE-NOT-ALLOWED
  - 5.4 Atribuição encadeada (ordem de avaliação)
  - 5.5 Declaração com inicialização encadeada
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
