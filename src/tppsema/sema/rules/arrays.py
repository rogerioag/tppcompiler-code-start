# src/tppsema/sema/rules/arrays.py
"""
Regras semânticas do item "4. Arranjos" do docs/SEM-SPECS.md:

  - 4.1 Índice não inteiro, no tamanho da declaração e no uso: ERR-SEM-ARRAY-INDEX-NOT-INT
  - 4.2 Índice fora do intervalo, e tamanho não positivo na declaração: ERR-SEM-ARRAY-INDEX-OUT-OF-RANGE
  - 4.3 Inicialização de arranjos: WAR-SEM-ARRAY-INIT-EXCESS-ELEMS, ERR-SEM-ARRAY-INIT-DIM, ERR-SEM-ARRAY-INIT-IN-EXP
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
