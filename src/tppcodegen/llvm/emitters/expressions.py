# src/tppcodegen/llvm/emitters/expressions.py
"""
Emissão LLVM-IR para expressões:

  - Literais inteiros e flutuantes (ir.Constant).
  - Leitura de variáveis escalares (load) e indexação de arranjos (gep + load).
  - Operações aritméticas inteiras (add, sub, mul, sdiv) e flutuantes (fadd, fsub, fmul, fdiv).
  - Operações relacionais (icmp / fcmp) e lógicas (&&, ||, !).
  - Promoções e coerções de tipo (sitofp / fptosi / zext).
"""


def emitir_expressao(no, contexto, codegen):
    """
    Avalia um nó de expressão da ASA e devolve o valor LLVM-IR correspondente.
    """
    # TODO (alunos): implementar a avaliação de expressões e coerções de tipo.
    return None
