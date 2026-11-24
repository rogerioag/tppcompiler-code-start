# src/tppcodegen/llvm/emitters/declarations.py
"""
Emissão LLVM-IR para declarações de variáveis (globais e locais) e arranjos:

  - Variáveis globais escalares e arranjos (ir.GlobalVariable, com inicializador).
  - Variáveis locais escalares e arranjos (builder.alloca no bloco de entrada).
  - Inicialização na declaração (ex.: inteiro: v[5] := {1, 2, 3, 4, 5}).
"""


def emitir_declaracao_variaveis(no, contexto, codegen, global_scope: bool = False):
    """
    Traduz um nó 'declaracao_variaveis' para alocação global ou local em LLVM-IR.

    no:           nó da ASA representando a declaração.
    contexto:     ContextoLLVM com módulo, builder e tabelas de endereços.
    codegen:      instância de LLVMCodeGen (use codegen.emitir(...) para erros/avisos).
    global_scope: True para variáveis globais; False para variáveis locais.
    """
    # TODO (alunos): implementar a emissão de declarações globais e locais.
    pass
