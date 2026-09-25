# src/tpplexer/automatalib_lexer/automatalibman_lexer.py
"""
automatalibman_lexer.py - Analisador Léxico baseado na biblioteca formal automata-lib com herança de ManualDFALexer.

Mapeia a 5-tupla formal M = (Q, Sigma, delta, q0, F) utilizando objetos DFA da automata-lib
para validar formalmente as linguagens regulares de identificadores, números inteiros e
notação científica na linguagem TPP.
"""

from typing import Optional, Set
from automata.fa.dfa import DFA

from ..mandfa_lexer.mandfa_lexer import ManualDFALexer
from ..base import Token


def _build_dfa_id() -> DFA:
    """Constroi o AFD formal para identificadores em TPP."""
    digits = set("0123456789")
    letters = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZáÁãÃàÀéÉíÍóÓõÕ")
    alphanum = letters | digits | {"_"}

    transitions = {
        "q0": {c: "q1" for c in letters} | {c: "qd" for c in (digits | {"_"})},
        "q1": {c: "q1" for c in alphanum},
        "qd": {c: "qd" for c in alphanum}
    }

    return DFA(
        states={"q0", "q1", "qd"},
        input_symbols=alphanum,
        transitions=transitions,
        initial_state="q0",
        final_states={"q1"}
    )


def _build_dfa_notacao_cientifica() -> DFA:
    """Constrói o AFD formal para literais em Notação Científica."""
    digits = set("0123456789")
    nonzero = set("123456789")
    symbols = digits | set("+-eE.")

    states = {"q0", "q_sign", "q_first", "q_dot", "q_frac", "q_exp", "q_expsign", "q_expdigits", "qd"}
    transitions = {s: {c: "qd" for c in symbols} for s in states}

    for c in "+-":
        transitions["q0"][c] = "q_sign"
    for c in nonzero:
        transitions["q0"][c] = "q_first"

    for c in nonzero:
        transitions["q_sign"][c] = "q_first"

    transitions["q_first"]["."] = "q_dot"

    for c in digits:
        transitions["q_dot"][c] = "q_frac"

    for c in digits:
        transitions["q_frac"][c] = "q_frac"
    for c in "eE":
        transitions["q_frac"][c] = "q_exp"

    for c in "+-":
        transitions["q_exp"][c] = "q_expsign"
    for c in digits:
        transitions["q_exp"][c] = "q_expdigits"

    for c in digits:
        transitions["q_expsign"][c] = "q_expdigits"

    for c in digits:
        transitions["q_expdigits"][c] = "q_expdigits"

    return DFA(
        states=states,
        input_symbols=symbols,
        transitions=transitions,
        initial_state="q0",
        final_states={"q_expdigits"}
    )


def _build_dfa_inteiro() -> DFA:
    """Constrói o AFD formal para numerais inteiros."""
    digits = set("0123456789")
    transitions = {
        "q0": {c: "q1" for c in digits},
        "q1": {c: "q1" for c in digits}
    }
    return DFA(
        states={"q0", "q1"},
        input_symbols=digits,
        transitions=transitions,
        initial_state="q0",
        final_states={"q1"}
    )


class AutomataLibManLexer(ManualDFALexer):
    """
    Analisador Léxico que emprega Autômatos Finitos Determinísticos formais (automata-lib)
    com herança de ManualDFALexer para o reconhecimento e validação de tokens da linguagem TPP.
    """

    def __init__(self, check_key: bool = False, **kwargs):
        super().__init__(check_key=check_key, **kwargs)
        self.dfa_id = _build_dfa_id()
        self.dfa_notacao_cientifica = _build_dfa_notacao_cientifica()
        self.dfa_inteiro = _build_dfa_inteiro()

    def is_valid_identifier(self, lexeme: str) -> bool:
        """Verifica se o lexema é aceito pelo AFD formal de identificadores."""
        try:
            return self.dfa_id.accepts_input(lexeme)
        except Exception:
            return False

    def is_scientific_notation(self, lexeme: str) -> bool:
        """Verifica se o lexema é aceito pelo AFD formal de Notação Científica."""
        try:
            return self.dfa_notacao_cientifica.accepts_input(lexeme)
        except Exception:
            return False

    def is_integer(self, lexeme: str) -> bool:
        """Verifica se o lexema é aceito pelo AFD formal de inteiros."""
        try:
            return self.dfa_inteiro.accepts_input(lexeme)
        except Exception:
            return False
