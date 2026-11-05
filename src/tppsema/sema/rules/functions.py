# src/tppsema/sema/rules/functions.py
"""
Regras semânticas do item "1. Funções e Procedimentos" do docs/SEM-SPECS.md:

  - 1.1 Função principal: ERR-SEM-MAIN-NOT-DECL
  - 1.2 Declaração de função: ERR-SEM-CALL-FUNC-NOT-DECL
  - 1.3 Quantidade de parâmetros: ERR-SEM-CALL-FUNC-WITH-FEW-ARGS, ERR-SEM-CALL-FUNC-WITH-MANY-ARGS
  - 1.4 Função declarada e não utilizada: WAR-SEM-FUNC-DECL-NOT-USED
  - 1.5 Retorno de função: ERR-SEM-FUNC-RET-TYPE-ERROR, ERR-SEM-CALL-FUNC-MAIN-NOT-ALLOWED, WAR-SEM-CALL-REC-FUNC-MAIN
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
