# src/tpplexer/mandfa_lexer/mandfa_lexer.py
"""
mandfa_lexer.py - Analisador Léxico manual baseado em Autômato Finito Determinístico (AFD/DFA).

Implementação procedural e orientada a objetos sem dependência de geradores (como PLY).
Percorre a cadeia de entrada caractere a caractere, utilizando lookahead para transições de estado,
resolvendo palavras reservadas, identificadores, números, operadores compostos, comentários
e tratamento de erros léxicos padronizados.
"""

from typing import Optional, Dict
import re

from ..base import BaseLexer, Token
from ..LogErrorLexer import le, log
from ..ply_lexer.tokens import reserved_words


class ManualDFALexer(BaseLexer):
    """
    Analisador Léxico manual para a linguagem TPP usando AFD (DFA).
    """

    # Conjunto de caracteres aceitos na linguagem
    LETRAS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZáÁãÃàÀéÉíÍóÓõÕ")
    DIGITOS = set("0123456789")
    ALFANUM_UNDER = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZáÁãÃàÀéÉíÍóÓõÕ0123456789_")

    # Expressão regular auxiliar para validação precisa de Notação Científica conforme o PLY
    RE_NOTACAO_CIENTIFICA = re.compile(r"^[\-\+]?[1-9]\.[0-9]+[eE][\-\+]?[0-9]+")

    def __init__(self, check_key: bool = False, **kwargs):
        self.check_key = check_key
        self.le = le
        self.data = ""
        self.length = 0
        self.pos = 0
        self.lineno = 1

    def input(self, data: str) -> None:
        """Carrega a entrada e reinicia os ponteiros do autômato."""
        self.data = data
        self.length = len(data)
        self.pos = 0
        self.lineno = 1

    def _peek(self, offset: int = 0) -> Optional[str]:
        """Observa o caractere na posição (pos + offset) sem avançar."""
        target = self.pos + offset
        if target < self.length:
            return self.data[target]
        return None

    def _advance(self) -> Optional[str]:
        """Consome e retorna o caractere atual, avançando o ponteiro."""
        if self.pos < self.length:
            c = self.data[self.pos]
            self.pos += 1
            return c
        return None

    def _report_error(self, key: str, lineno: int, lexpos: int, valor: str = "") -> None:
        """Emite erro formatado ou chave conforme a opção check_key."""
        col = self.get_column(self.data, lexpos)
        msg = self.le.newError(self.check_key, key, lineno, col, valor=valor)
        print(msg)

    def token(self) -> Optional[Token]:
        """
        Retorna o próximo Token reconhecido pelo autômato ou None ao atingir EOF.
        """
        while self.pos < self.length:
            c = self.data[self.pos]

            # -------------------------------------------------------------
            # 1. Espaços em branco e quebras de linha
            # -------------------------------------------------------------
            if c == '\n':
                self.lineno += 1
                self.pos += 1
                continue
            elif c in ' \t\r':
                self.pos += 1
                continue

            # -------------------------------------------------------------
            # 2. Comentários: { ... }
            # -------------------------------------------------------------
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
                    # Comentário não fechado até o fim do arquivo (EOF)
                    self._report_error('ERR-LEX-UNC-COMMENT', start_lineno, start_pos)
                    return None
                continue

            start_pos = self.pos
            start_lineno = self.lineno

            # -------------------------------------------------------------
            # 3. Notação Científica iniciada por sinal: +1.496e11 ou -1.496e11
            # -------------------------------------------------------------
            if c in '+-' and self._peek(1) in set("123456789"):
                match = self.RE_NOTACAO_CIENTIFICA.match(self.data[self.pos:])
                if match:
                    lexeme = match.group(0)
                    self.pos += len(lexeme)
                    return Token("NUM_NOTACAO_CIENTIFICA", lexeme, start_lineno, start_pos)

            # -------------------------------------------------------------
            # 4. Identificadores e Palavras Reservadas: [letra][letra|digito|_]*
            # -------------------------------------------------------------
            if c in self.LETRAS:
                self.pos += 1
                while self.pos < self.length and self.data[self.pos] in self.ALFANUM_UNDER:
                    self.pos += 1
                lexeme = self.data[start_pos:self.pos]
                tok_type = reserved_words.get(lexeme, "ID")
                return Token(tok_type, lexeme, start_lineno, start_pos)

            # -------------------------------------------------------------
            # 5. Números (Inteiro, Ponto Flutuante, Notação Científica)
            # -------------------------------------------------------------
            if c in self.DIGITOS or (c == '.' and self._peek(1) in self.DIGITOS):
                # Verifica primeiro se casa com Notação Científica exata
                match_nc = self.RE_NOTACAO_CIENTIFICA.match(self.data[self.pos:])
                if match_nc:
                    lexeme = match_nc.group(0)
                    self.pos += len(lexeme)
                    return Token("NUM_NOTACAO_CIENTIFICA", lexeme, start_lineno, start_pos)

                has_dot = False
                has_exp = False

                if c == '.':
                    has_dot = True
                    self.pos += 1  # Consome '.'

                while self.pos < self.length:
                    curr = self.data[self.pos]
                    if curr in self.DIGITOS:
                        self.pos += 1
                    elif curr == '.' and not has_dot and not has_exp:
                        has_dot = True
                        self.pos += 1
                    elif curr in 'eE' and not has_exp:
                        # Expoente exige pelo menos um dígito adiante (com opcional + ou -)
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

            # -------------------------------------------------------------
            # 6. Operadores Relacionais e Atribuição
            # -------------------------------------------------------------
            if c == ':':
                self.pos += 1
                if self._peek(0) == '=':
                    self.pos += 1
                    return Token("ATRIBUICAO", ":=", start_lineno, start_pos)
                return Token("DOIS_PONTOS", ":", start_lineno, start_pos)

            if c == '<':
                self.pos += 1
                nxt = self._peek(0)
                if nxt == '=':
                    self.pos += 1
                    return Token("MENOR_IGUAL", "<=", start_lineno, start_pos)
                elif nxt == '>':
                    self.pos += 1
                    return Token("DIFERENTE", "<>", start_lineno, start_pos)
                return Token("MENOR", "<", start_lineno, start_pos)

            if c == '>':
                self.pos += 1
                if self._peek(0) == '=':
                    self.pos += 1
                    return Token("MAIOR_IGUAL", ">=", start_lineno, start_pos)
                return Token("MAIOR", ">", start_lineno, start_pos)

            if c == '=':
                self.pos += 1
                return Token("IGUAL", "=", start_lineno, start_pos)

            # -------------------------------------------------------------
            # 7. Operadores Lógicos
            # -------------------------------------------------------------
            if c == '&':
                self.pos += 1
                if self._peek(0) == '&':
                    self.pos += 1
                    return Token("E", "&&", start_lineno, start_pos)
                # & isolado é caractere inválido
                self._report_error('ERR-LEX-INV-CHAR', start_lineno, start_pos, valor='&')
                continue

            if c == '|':
                self.pos += 1
                if self._peek(0) == '|':
                    self.pos += 1
                    return Token("OU", "||", start_lineno, start_pos)
                # | isolado é caractere inválido
                self._report_error('ERR-LEX-INV-CHAR', start_lineno, start_pos, valor='|')
                continue

            if c == '!':
                self.pos += 1
                return Token("NAO", "!", start_lineno, start_pos)

            # -------------------------------------------------------------
            # 8. Operadores Aritméticos
            # -------------------------------------------------------------
            if c == '+':
                self.pos += 1
                return Token("MAIS", "+", start_lineno, start_pos)

            if c == '-':
                self.pos += 1
                return Token("MENOS", "-", start_lineno, start_pos)

            if c == '*':
                self.pos += 1
                return Token("VEZES", "*", start_lineno, start_pos)

            if c == '/':
                self.pos += 1
                return Token("DIVIDE", "/", start_lineno, start_pos)

            # -------------------------------------------------------------
            # 9. Delimitadores
            # -------------------------------------------------------------
            if c == '(':
                self.pos += 1
                return Token("ABRE_PARENTESE", "(", start_lineno, start_pos)

            if c == ')':
                self.pos += 1
                return Token("FECHA_PARENTESE", ")", start_lineno, start_pos)

            if c == '[':
                self.pos += 1
                return Token("ABRE_COLCHETE", "[", start_lineno, start_pos)

            if c == ']':
                self.pos += 1
                return Token("FECHA_COLCHETE", "]", start_lineno, start_pos)

            if c == ',':
                self.pos += 1
                return Token("VIRGULA", ",", start_lineno, start_pos)

            # -------------------------------------------------------------
            # 10. Caractere Inválido
            # -------------------------------------------------------------
            self._report_error('ERR-LEX-INV-CHAR', start_lineno, start_pos, valor=c)
            self.pos += 1

        return None
