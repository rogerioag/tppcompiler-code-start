# src/tppcodegen/llvm/emitters/commands.py
"""
Emissão LLVM-IR para comandos de controle de fluxo e atribuição:

  - Atribuição simples, múltipla e encadeada (store com coerção implícita quando necessária).
  - Condicional 'se ... então ... [senão ...] fim' (blocos if.then, if.else, if.end + cbranch).
  - Laço 'repita ... até <cond>' (blocos repeat.body, repeat.end + cbranch).
"""


def emitir_comando(no, contexto, codegen):
    """
    Despacha a emissão de um comando (atribuição, se, repita, leia, escreva, retorna, chamada).
    """
    # TODO (alunos): implementar o despacho e a tradução dos comandos da linguagem TPP.
    pass
