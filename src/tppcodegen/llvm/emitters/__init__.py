# src/tppcodegen/llvm/emitters/__init__.py
"""
Emissores de código LLVM-IR da linguagem TPP, separados por categoria.

Cada módulo concentra a tradução de um conjunto de nós da árvore sintática
abstrata (ASA) para instruções LLVM-IR usando o ContextoLLVM.
"""

from . import declarations, functions, commands, expressions, io

__all__ = [
    "declarations",
    "functions",
    "commands",
    "expressions",
    "io",
]
