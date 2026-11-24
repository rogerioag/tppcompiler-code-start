# src/tppcodegen/__init__.py
"""
Pacote principal de geração de código (tppcodegen).
Factory para obtenção do gerador de código com base na estratégia solicitada.
"""

from .base import BaseCodeGen
from .llvm.tppcodegen import LLVMCodeGen

__all__ = [
    "get_codegen",
    "BaseCodeGen",
    "LLVMCodeGen",
]


def get_codegen(strategy="llvm", **kwargs) -> BaseCodeGen:
    """
    Factory que retorna a instância do gerador de código de acordo com a estratégia.
    """
    strategy = strategy.lower()
    if strategy == "llvm":
        return LLVMCodeGen(**kwargs)
    else:
        raise ValueError(f"Estratégia de geração de código desconhecida: '{strategy}'")
