# src/tppcodegen/llvm/emitters/functions.py
"""
Emissão LLVM-IR para funções:

  - Definição de função (ir.FunctionType, ir.Function) e mapeamento de 'principal' -> 'main'.
  - Alocação de parâmetros formais (incluindo passagem de arranjos por ponteiro).
  - Chamada de função (builder.call) com coerção implícita de argumentos quando necessária.
  - Comando 'retorna' (builder.ret / builder.ret_void) e suporte a retorno múltiplo.
"""


def emitir_declaracao_funcao(no, contexto, codegen):
    """
    Traduz um nó 'declaracao_funcao' para uma função LLVM-IR no módulo atual.
    """
    # TODO (alunos): implementar a criação da função, bloco de entrada, parâmetros e corpo.
    pass


def emitir_chamada_funcao(no, contexto, codegen):
    """
    Traduz um nó 'chamada_funcao' para uma instrução call em LLVM-IR.
    """
    # TODO (alunos): implementar a avaliação de argumentos e chamada da função.
    return None


def emitir_retorna(no, contexto, codegen):
    """
    Traduz um nó 'retorna' para uma instrução ret em LLVM-IR.
    """
    # TODO (alunos): implementar o retorno da função (incluindo coerção de tipo se necessário).
    pass
