"""
Estratégia padrão de geração de código ("llvm") usando llvmlite.

- tppcodegen.py: LLVMCodeGen, que percorre a ASA e coordena a geração do módulo LLVM-IR.
- context.py: contexto de geração (módulo LLVM, IRBuilder, tipos, escopos e funções).
- emitters/: emissão de código LLVM-IR organizada por categoria da linguagem TPP.
"""
