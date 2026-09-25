# src/tpplexer/symtable_lexer/symtableman_lexer.py
"""
symtableman_lexer.py - Analisador Léxico integrado com Tabela de Símbolos (Symbol Table) com herança de ManualDFALexer.

Demonstra a abordagem clássica de compiladores onde o scanner reconhece termos e palavras,
consulta palavras reservadas estáticas e instala/atualiza identificadores na Tabela de Símbolos.
"""

from typing import Optional, Dict, Any, List
from ..mandfa_lexer.mandfa_lexer import ManualDFALexer
from ..base import Token


class SymbolEntry:
    """Entrada da Tabela de Símbolos contendo metadados do identificador."""
    def __init__(self, lexeme: str, token_type: str, lineno: int, column: int):
        self.lexeme = lexeme
        self.token_type = token_type
        self.first_line = lineno
        self.first_column = column
        self.occurrences: List[tuple] = [(lineno, column)]

    def add_occurrence(self, lineno: int, column: int):
        self.occurrences.append((lineno, column))

    def __repr__(self):
        return f"SymbolEntry({self.lexeme!r}, type={self.token_type}, count={len(self.occurrences)})"


class SymbolTable:
    """Tabela de Símbolos para armazenamento e consulta de identificadores."""
    def __init__(self):
        self._table: Dict[str, SymbolEntry] = {}

    def insert_or_update(self, lexeme: str, token_type: str, lineno: int, column: int) -> SymbolEntry:
        if lexeme in self._table:
            entry = self._table[lexeme]
            entry.add_occurrence(lineno, column)
            return entry
        entry = SymbolEntry(lexeme, token_type, lineno, column)
        self._table[lexeme] = entry
        return entry

    def lookup(self, lexeme: str) -> Optional[SymbolEntry]:
        return self._table.get(lexeme)

    def all_symbols(self) -> Dict[str, SymbolEntry]:
        return dict(self._table)

    def clear(self):
        self._table.clear()


class SymbolTableManLexer(ManualDFALexer):
    """
    Analisador Léxico que estende o AFD Manual (ManualDFALexer) instalando e rastreando
    identificadores na Tabela de Símbolos.
    """

    def __init__(self, check_key: bool = False, **kwargs):
        super().__init__(check_key=check_key, **kwargs)
        self.symbol_table = SymbolTable()

    def input(self, data: str) -> None:
        super().input(data)
        self.symbol_table.clear()

    def token(self) -> Optional[Token]:
        tok = super().token()
        if tok is None:
            return None

        # Se for identificador, registra na tabela de símbolos
        if tok.type == "ID":
            col = self.get_column(self.data, tok.lexpos)
            self.symbol_table.insert_or_update(tok.value, tok.type, tok.lineno, col)

        return tok


# Alias para retrocompatibilidade
SymbolTableLexer = SymbolTableManLexer
