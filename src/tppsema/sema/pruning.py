# src/tppsema/sema/pruning.py
"""
Poda da árvore sintática.

TODO (alunos): remover os nós internos que não são necessários para a geração
de código e produzir a árvore sintática abstrata (ASA), conforme a seção
"Árvore Sintática Abstrata" do docs/SEM-SPECS.md. Por exemplo, em
"a := b + c - d" a ASA tem ':=' na raiz, com 'a' e '-' como filhos, e o '-'
tem '+' (com 'b' e 'c') e 'd' como filhos.
"""


def podar(arvore):
    """Retorna a árvore sintática abstrata (ASA) obtida pela poda de 'arvore'."""
    # TODO (alunos): implementar a poda. Por enquanto, a árvore é devolvida sem alterações.
    return arvore
