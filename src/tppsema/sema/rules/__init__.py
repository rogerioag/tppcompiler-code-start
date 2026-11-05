# src/tppsema/sema/rules/__init__.py
"""
Regras semânticas da linguagem TPP, separadas por categoria (docs/SEM-SPECS.md).

Cada módulo tem uma função verificar(arvore, tabela, sema), chamada pelo
TPPSema na ordem de REGRAS.
"""

from . import functions, variables, coercions, arrays, assignments, returns, expressions

REGRAS = [functions, variables, coercions, arrays, assignments, returns, expressions]
