# src/tpplexer/automatalib_lexer/automatalib_lexer.py
"""
automatalib_lexer.py - Analisador Léxico Puro baseado formalmente na biblioteca automata-lib.

Implementa o algoritmo de reconhecimento léxico por Autômatos Finitos Determinísticos (DFA)
utilizando a regra do Prefixo Mais Longo (Maximal Munch / Longest Match Rule).
Não herda de ManualDFALexer; herda diretamente de BaseLexer.
Cada classe de token, operador e delimitador é formalmente modelado como um objeto DFA M = (Q, Sigma, delta, q0, F).
"""

from typing import Optional, List, Tuple
from automata.fa.dfa import DFA

from ..base import BaseLexer, Token
from ..LogErrorLexer import le
from ..ply_lexer.tokens import reserved_words


# =====================================================================
# 1. Fábrica de Autômatos Finitos Determinísticos Formais (automata-lib)
# =====================================================================

def _build_dfa_id() -> DFA:
    """AFD formal para Identificadores: [a-zA-Zá-õ][a-zA-Zá-õ0-9_]*"""
    digits = set("0123456789")
    letters = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZáÁãÃàÀéÉíÍóÓõÕ")
    alphanum = letters | digits | {"_"}
    return DFA(
        states={"q0", "q1"},
        input_symbols=alphanum,
        transitions={
            "q0": {c: "q1" for c in letters},
            "q1": {c: "q1" for c in alphanum},
        },
        initial_state="q0",
        final_states={"q1"},
        allow_partial=True
    )


def _build_dfa_inteiro() -> DFA:
    """AFD formal para Números Inteiros: [0-9]+"""
    digits = set("0123456789")
    return DFA(
        states={"q0", "q1"},
        input_symbols=digits,
        transitions={
            "q0": {c: "q1" for c in digits},
            "q1": {c: "q1" for c in digits},
        },
        initial_state="q0",
        final_states={"q1"},
        allow_partial=True
    )


def _build_dfa_notacao_cientifica() -> DFA:
    r"""
    AFD formal para Notação Científica: [+-]?[1-9]\.[0-9]+[eE][+-]?[0-9]+
    Conforme especificação da linguagem TPP.
    """
    digits = set("0123456789")
    nonzero = set("123456789")
    symbols = digits | set("+-eE.")

    states = {"q0", "q_sign", "q_first", "q_dot", "q_frac", "q_exp", "q_expsign", "q_expdigits"}
    transitions = {s: {} for s in states}

    for c in "+-":
        transitions["q0"][c] = "q_sign"
    for c in nonzero:
        transitions["q0"][c] = "q_first"
        transitions["q_sign"][c] = "q_first"

    transitions["q_first"]["."] = "q_dot"

    for c in digits:
        transitions["q_dot"][c] = "q_frac"
        transitions["q_frac"][c] = "q_frac"
        transitions["q_exp"][c] = "q_expdigits"
        transitions["q_expsign"][c] = "q_expdigits"
        transitions["q_expdigits"][c] = "q_expdigits"

    for c in "eE":
        transitions["q_frac"][c] = "q_exp"

    for c in "+-":
        transitions["q_exp"][c] = "q_expsign"

    return DFA(
        states=states,
        input_symbols=symbols,
        transitions=transitions,
        initial_state="q0",
        final_states={"q_expdigits"},
        allow_partial=True
    )


def _build_dfa_flutuante() -> DFA:
    r"""
    AFD formal para Números Flutuantes: \d+[eE][-+]?\d+|(\.\d+|\d+\.\d*)([eE][-+]?\d+)?
    """
    digits = set("0123456789")
    symbols = digits | set(".eE+-")
    states = {"q0", "q_dot_start", "q_int", "q_dot", "q_frac", "q_exp", "q_expsign", "q_expdigits"}
    transitions = {s: {} for s in states}

    for c in digits:
        transitions["q0"][c] = "q_int"
        transitions["q_dot_start"][c] = "q_frac"
        transitions["q_int"][c] = "q_int"
        transitions["q_dot"][c] = "q_frac"
        transitions["q_frac"][c] = "q_frac"
        transitions["q_exp"][c] = "q_expdigits"
        transitions["q_expsign"][c] = "q_expdigits"
        transitions["q_expdigits"][c] = "q_expdigits"

    transitions["q0"]["."] = "q_dot_start"
    transitions["q_int"]["."] = "q_dot"

    for c in "eE":
        transitions["q_int"][c] = "q_exp"
        transitions["q_dot"][c] = "q_exp"
        transitions["q_frac"][c] = "q_exp"

    for c in "+-":
        transitions["q_exp"][c] = "q_expsign"

    return DFA(
        states=states,
        input_symbols=symbols,
        transitions=transitions,
        initial_state="q0",
        final_states={"q_dot", "q_frac", "q_expdigits"},
        allow_partial=True
    )


def _build_dfa_literal(literal: str) -> DFA:
    """Gera um AFD linear mínimo para literais e operadores da linguagem."""
    states = {f"q{i}" for i in range(len(literal) + 1)}
    symbols = set(literal)
    transitions = {f"q{i}": {} for i in range(len(literal) + 1)}
    for i in range(len(literal)):
        transitions[f"q{i}"][literal[i]] = f"q{i+1}"
    return DFA(
        states=states,
        input_symbols=symbols,
        transitions=transitions,
        initial_state="q0",
        final_states={f"q{len(literal)}"},
        allow_partial=True
    )


# =====================================================================
# 2. Classe AutomataLibLexer (Herança Direta de BaseLexer)
# =====================================================================

class AutomataLibLexer(BaseLexer):
    """
    Analisador Léxico Puro baseado na biblioteca automata-lib.

    Cada padrão de token é um AFD formal. O reconhecimento de tokens na cadeia de entrada
    é conduzido pelo algoritmo Maximal Munch (Prefixo Mais Longo), sem qualquer herança
    ou dependência de ManualDFALexer.
    """

    def __init__(self, check_key: bool = False, **kwargs):
        self.check_key = check_key
        self.le = le
        self.data = ""
        self.length = 0
        self.pos = 0
        self.lineno = 1

        # Construção da lista de regras (tipo do token, DFA associado)
        # A ordem define a precedência em caso de empate de mesmo comprimento
        self.rules: List[Tuple[str, DFA]] = [
            # Numerais (Notação Científica tem precedência para sinais + / -)
            ("NUM_NOTACAO_CIENTIFICA", _build_dfa_notacao_cientifica()),
            ("NUM_PONTO_FLUTUANTE", _build_dfa_flutuante()),
            ("NUM_INTEIRO", _build_dfa_inteiro()),

            # Identificadores (Palavras reservadas são checadas em seguida)
            ("ID", _build_dfa_id()),

            # Operadores compostos (2 caracteres)
            ("ATRIBUICAO", _build_dfa_literal(":=")),
            ("MENOR_IGUAL", _build_dfa_literal("<=")),
            ("MAIOR_IGUAL", _build_dfa_literal(">=")),
            ("DIFERENTE", _build_dfa_literal("<>")),
            ("E", _build_dfa_literal("&&")),
            ("OU", _build_dfa_literal("||")),

            # Operadores simples e delimitadores (1 caractere)
            ("MENOR", _build_dfa_literal("<")),
            ("MAIOR", _build_dfa_literal(">")),
            ("IGUAL", _build_dfa_literal("=")),
            ("NAO", _build_dfa_literal("!")),
            ("MAIS", _build_dfa_literal("+")),
            ("MENOS", _build_dfa_literal("-")),
            ("VEZES", _build_dfa_literal("*")),
            ("DIVIDE", _build_dfa_literal("/")),
            ("ABRE_PARENTESE", _build_dfa_literal("(")),
            ("FECHA_PARENTESE", _build_dfa_literal(")")),
            ("ABRE_COLCHETE", _build_dfa_literal("[")),
            ("FECHA_COLCHETE", _build_dfa_literal("]")),
            ("VIRGULA", _build_dfa_literal(",")),
            ("DOIS_PONTOS", _build_dfa_literal(":")),
        ]

    def input(self, data: str) -> None:
        """Carrega a entrada e inicializa o cursor e linha."""
        self.data = data
        self.length = len(data)
        self.pos = 0
        self.lineno = 1

    def _report_error(self, key: str, lineno: int, lexpos: int, valor: str = "") -> None:
        """Emite o erro formatado ou chave conforme a opção check_key."""
        col = self.get_column(self.data, lexpos)
        msg = self.le.newError(self.check_key, key, lineno, col, valor=valor)
        print(msg)

    def _match_dfa_longest(self, dfa: DFA, start_pos: int) -> int:
        """
        Executa a simulação determinística do DFA caractere a caractere a partir de start_pos.
        Retorna o comprimento do maior prefixo aceito (ou 0 se for rejeitado).
        """
        curr_state = dfa.initial_state
        longest_match_len = 0
        current_len = 0
        idx = start_pos

        while idx < self.length:
            char = self.data[idx]
            transitions = dfa.transitions.get(curr_state)
            if not transitions or char not in transitions:
                break
            curr_state = transitions[char]
            current_len += 1
            idx += 1
            if curr_state in dfa.final_states:
                longest_match_len = current_len

        return longest_match_len

    def token(self) -> Optional[Token]:
        """
        Retorna o próximo Token da entrada conforme o algoritmo Maximal Munch.
        """
        while self.pos < self.length:
            c = self.data[self.pos]

            # 1. Quebra de linha
            if c == '\n':
                self.lineno += 1
                self.pos += 1
                continue
            
            # 2. Espaços em branco
            if c in ' \t\r':
                self.pos += 1
                continue

            # 3. Comentários {...}
            if c == '{':
                start_lineno = self.lineno
                start_pos = self.pos
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

            start_lineno = self.lineno
            start_pos = self.pos

            # 4. Maximal Munch (busca o maior prefixo aceito entre os AFDs)
            best_type = None
            best_len = 0

            for tok_type, dfa in self.rules:
                mlen = self._match_dfa_longest(dfa, self.pos)
                if mlen > best_len:
                    best_len = mlen
                    best_type = tok_type

            if best_len > 0:
                lexeme = self.data[start_pos : start_pos + best_len]
                self.pos += best_len

                # Palavra reservada vs Identificador
                if best_type == "ID":
                    tok_type = reserved_words.get(lexeme, "ID")
                    return Token(tok_type, lexeme, start_lineno, start_pos)

                return Token(best_type, lexeme, start_lineno, start_pos)

            # 5. Caractere Inválido
            self._report_error('ERR-LEX-INV-CHAR', start_lineno, start_pos, valor=c)
            self.pos += 1

        return None
