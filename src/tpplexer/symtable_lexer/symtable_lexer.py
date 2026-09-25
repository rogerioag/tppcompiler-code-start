# src/tpplexer/symtable_lexer/symtable_lexer.py
"""
symtable_lexer.py - Analisador Léxico Puro Orientado a Tabela de Símbolos (Symbol Table Driven).

Implementação independente que herda diretamente de BaseLexer (sem herança de ManualDFALexer).
A Tabela de Símbolos é pré-populada com todos os tokens estáticos da linguagem (palavras reservadas,
operadores e delimitadores). Ao varrer o código-fonte:
1. Termos alfanuméricos são consultados na Tabela de Símbolos:
   - Se for palavra reservada nativa ou ID já registrado: retorna o token correspondente;
   - Se não existir: é um novo identificador, que é instalado na tabela e retorna Token("ID").
2. Operadores e delimitadores são consultados diretamente na Tabela de Símbolos (lookahead 2 ou 1 caractere).
3. Numerais são reconhecidos e tipados conforme a gramática TPP.
"""

from typing import Optional, Dict, Any, List
import re

from ..base import BaseLexer, Token
from ..LogErrorLexer import le
from ..ply_lexer.tokens import reserved_words


class SymbolEntry:
    """Entrada da Tabela de Símbolos contendo metadados do símbolo ou identificador."""
    def __init__(
        self,
        lexeme: str,
        token_type: str,
        lineno: int = 0,
        column: int = 0,
        is_builtin: bool = False
    ):
        self.lexeme = lexeme
        self.token_type = token_type
        self.first_line = lineno
        self.first_column = column
        self.is_builtin = is_builtin
        self.occurrences: List[tuple] = [(lineno, column)] if not is_builtin else []

    def add_occurrence(self, lineno: int, column: int) -> None:
        """Adiciona uma nova ocorrência do identificador no código-fonte."""
        self.occurrences.append((lineno, column))

    def __repr__(self) -> str:
        kind = "builtin" if self.is_builtin else f"count={len(self.occurrences)}"
        return f"SymbolEntry({self.lexeme!r}, type={self.token_type}, {kind})"


class SymbolTable:
    """
    Tabela de Símbolos pré-populada com as palavras reservadas, operadores
    e delimitadores da linguagem TPP.
    """

    OPERATORS_AND_DELIMITERS = {
        ":=": "ATRIBUICAO",
        "<=": "MENOR_IGUAL",
        ">=": "MAIOR_IGUAL",
        "<>": "DIFERENTE",
        "&&": "E",
        "||": "OU",
        "!": "NAO",
        "+": "MAIS",
        "-": "MENOS",
        "*": "VEZES",
        "/": "DIVIDE",
        "<": "MENOR",
        ">": "MAIOR",
        "=": "IGUAL",
        "(": "ABRE_PARENTESE",
        ")": "FECHA_PARENTESE",
        "[": "ABRE_COLCHETE",
        "]": "FECHA_COLCHETE",
        ",": "VIRGULA",
        ":": "DOIS_PONTOS",
    }

    def __init__(self):
        self._table: Dict[str, SymbolEntry] = {}
        self._init_builtins()

    def _init_builtins(self) -> None:
        """Pré-instala palavras reservadas e operadores nativos da linguagem."""
        # 1. Palavras reservadas (se, então, senão, etc.)
        for lexeme, token_type in reserved_words.items():
            self._table[lexeme] = SymbolEntry(lexeme, token_type, is_builtin=True)

        # 2. Operadores e delimitadores (:=, <=, +, etc.)
        for lexeme, token_type in self.OPERATORS_AND_DELIMITERS.items():
            self._table[lexeme] = SymbolEntry(lexeme, token_type, is_builtin=True)

    def lookup(self, lexeme: str) -> Optional[SymbolEntry]:
        """Busca um lexema na tabela de símbolos."""
        return self._table.get(lexeme)

    def install_identifier(self, lexeme: str, lineno: int, column: int) -> SymbolEntry:
        """
        Instala um novo identificador ou adiciona ocorrência a um existente.
        """
        if lexeme in self._table:
            entry = self._table[lexeme]
            entry.add_occurrence(lineno, column)
            return entry

        entry = SymbolEntry(lexeme, "ID", lineno, column, is_builtin=False)
        self._table[lexeme] = entry
        return entry

    def reset_user_symbols(self) -> None:
        """Remove os identificadores de usuário, mantendo os símbolos nativos."""
        self._table = {k: v for k, v in self._table.items() if v.is_builtin}

    def all_symbols(self) -> Dict[str, SymbolEntry]:
        """Retorna todos os símbolos (nativos + usuário)."""
        return dict(self._table)

    def user_symbols(self) -> Dict[str, SymbolEntry]:
        """Retorna apenas os identificadores cadastrados durante a análise."""
        return {k: v for k, v in self._table.items() if not v.is_builtin}


class SymbolTableLexer(BaseLexer):
    """
    Analisador Léxico Orientado a Tabela de Símbolos para a linguagem TPP.
    Herda diretamente de BaseLexer (sem herança de ManualDFALexer).
    """

    LETRAS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZáÁãÃàÀéÉíÍóÓõÕ")
    DIGITOS = set("0123456789")
    ALFANUM_UNDER = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZáÁãÃàÀéÉíÍóÓõÕ0123456789_")

    # Expressão regular para validação precisa de Notação Científica conforme o PLY
    RE_NOTACAO_CIENTIFICA = re.compile(r"^[\-\+]?[1-9]\.[0-9]+[eE][\-\+]?[0-9]+")

    def __init__(self, check_key: bool = False, **kwargs):
        self.check_key = check_key
        self.le = le
        self.data = ""
        self.length = 0
        self.pos = 0
        self.lineno = 1
        self.symbol_table = SymbolTable()

    def input(self, data: str) -> None:
        """Carrega o código-fonte e reseta identificadores da Tabela de Símbolos."""
        self.data = data
        self.length = len(data)
        self.pos = 0
        self.lineno = 1
        self.symbol_table.reset_user_symbols()

    def _peek(self, offset: int = 0) -> str:
        """Observa o caractere em (pos + offset) sem avançar o cursor."""
        target = self.pos + offset
        if target < self.length:
            return self.data[target]
        return ""

    def _report_error(self, key: str, lineno: int, lexpos: int, valor: str = "") -> None:
        """Emite erro formatado ou chave conforme a opção check_key."""
        col = self.get_column(self.data, lexpos)
        msg = self.le.newError(self.check_key, key, lineno, col, valor=valor)
        print(msg)

    def token(self) -> Optional[Token]:
        """
        Retorna o próximo Token reconhecido ou None ao atingir EOF.
        A resolução de palavras-chave, operadores e identificadores é orientada pela Tabela de Símbolos.
        """
        while self.pos < self.length:
            c = self.data[self.pos]

            # 1. Quebra de linha
            if c == '\n':
                self.lineno += 1
                self.pos += 1
                continue

            # 2. Espaços em branco e tabulações
            if c in ' \t\r':
                self.pos += 1
                continue

            # 3. Comentários: { ... }
            if c == '{':
                start_pos = self.pos
                start_lineno = self.lineno
                self.pos += 1
                fechado = False
                while self.pos < self.length:
                    ch = self.data[self.pos]
                    if ch == '\n':
                        self.lineno += 1
                    elif ch == '}':
                        self.pos += 1
                        fechado = True
                        break
                    self.pos += 1

                if not fechado:
                    self._report_error('ERR-LEX-UNC-COMMENT', start_lineno, start_pos)
                    return None
                continue

            start_pos = self.pos
            start_lineno = self.lineno

            # 4. Notação Científica iniciada por sinal (+ ou -)
            if c in '+-' and self._peek(1) in set("123456789"):
                match = self.RE_NOTACAO_CIENTIFICA.match(self.data[self.pos:])
                if match:
                    lexeme = match.group(0)
                    self.pos += len(lexeme)
                    return Token("NUM_NOTACAO_CIENTIFICA", lexeme, start_lineno, start_pos)

            # 5. Termos Alfanuméricos (Palavras Reservadas vs Identificadores via Tabela de Símbolos)
            if c in self.LETRAS:
                self.pos += 1
                while self.pos < self.length and self.data[self.pos] in self.ALFANUM_UNDER:
                    self.pos += 1
                lexeme = self.data[start_pos:self.pos]
                col = self.get_column(self.data, start_pos)

                # Consulta na Tabela de Símbolos
                entry = self.symbol_table.lookup(lexeme)
                if entry is not None:
                    # Se for palavra reservada nativa ou identificador pré-existente
                    if entry.is_builtin:
                        return Token(entry.token_type, lexeme, start_lineno, start_pos)
                    else:
                        entry.add_occurrence(start_lineno, col)
                        return Token(entry.token_type, lexeme, start_lineno, start_pos)
                else:
                    # Não existe na tabela: é um novo identificador! Instala na Tabela de Símbolos
                    self.symbol_table.install_identifier(lexeme, start_lineno, col)
                    return Token("ID", lexeme, start_lineno, start_pos)

            # 6. Numerais (Notação Científica, Ponto Flutuante, Inteiro)
            if c in self.DIGITOS or (c == '.' and self._peek(1) in self.DIGITOS):
                match_nc = self.RE_NOTACAO_CIENTIFICA.match(self.data[self.pos:])
                if match_nc:
                    lexeme = match_nc.group(0)
                    self.pos += len(lexeme)
                    return Token("NUM_NOTACAO_CIENTIFICA", lexeme, start_lineno, start_pos)

                has_dot = False
                has_exp = False

                if c == '.':
                    has_dot = True
                    self.pos += 1

                while self.pos < self.length:
                    curr = self.data[self.pos]
                    if curr in self.DIGITOS:
                        self.pos += 1
                    elif curr == '.' and not has_dot and not has_exp:
                        has_dot = True
                        self.pos += 1
                    elif curr in 'eE' and not has_exp:
                        next1 = self._peek(1)
                        next2 = self._peek(2)
                        if next1 in self.DIGITOS:
                            has_exp = True
                            self.pos += 2
                        elif next1 in '+-' and next2 in self.DIGITOS:
                            has_exp = True
                            self.pos += 3
                        else:
                            break
                    else:
                        break

                lexeme = self.data[start_pos:self.pos]
                if has_dot or has_exp:
                    return Token("NUM_PONTO_FLUTUANTE", lexeme, start_lineno, start_pos)
                else:
                    return Token("NUM_INTEIRO", lexeme, start_lineno, start_pos)

            # 7. Operadores e Delimitadores (resolvidos diretamente pela Tabela de Símbolos)
            # Tenta operador composto de 2 caracteres (:=, <=, >=, <>, &&, ||)
            two_chars = self.data[self.pos : self.pos + 2]
            entry_two = self.symbol_table.lookup(two_chars)
            if entry_two is not None and entry_two.is_builtin:
                self.pos += 2
                return Token(entry_two.token_type, two_chars, start_lineno, start_pos)

            # Tenta operador / delimitador de 1 caractere (+, -, *, /, (, ), [, ], ,, :, <, >, =)
            entry_one = self.symbol_table.lookup(c)
            if entry_one is not None and entry_one.is_builtin:
                self.pos += 1
                return Token(entry_one.token_type, c, start_lineno, start_pos)

            # 8. Caractere Inválido
            self._report_error('ERR-LEX-INV-CHAR', start_lineno, start_pos, valor=c)
            self.pos += 1

        return None
