# src/tppcodegen/llvm/emitters/io.py
"""
Emissão LLVM-IR para entrada e saída (leia e escreva):

  - Declaração das funções externas de E/S (ex.: leiaInteiro, leiaFlutuante,
    escrevaInteiro, escrevaFlutuante ou printf/scanf da libc).
  - Comando 'leia(var)': lê valor da entrada padrão e armazena no endereço de var.
  - Comando 'escreva(exp)': avalia a expressão e imprime na saída padrão.
"""


def emitir_leia(no, contexto, codegen):
    """
    Traduz um nó 'leia' para chamada de leitura em LLVM-IR.
    """
    # TODO (alunos): implementar a emissão do comando leia.
    pass


def emitir_escreva(no, contexto, codegen):
    """
    Traduz um nó 'escreva' para chamada de escrita em LLVM-IR.
    """
    # TODO (alunos): implementar a emissão do comando escreva.
    pass
