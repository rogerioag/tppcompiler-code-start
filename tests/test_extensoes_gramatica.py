# tests/test_extensoes_gramatica.py
"""
Testes das extensões da linguagem TPP:
1. Comentários no formato {* ... *} e tokens ABRE_CHAVE / FECHA_CHAVE (todos os lexers)
2. Atribuição múltipla, retorno múltiplo e inicialização de arrays (parser PLY)
3. Alvos entre parênteses e o NEWLINE inserido pelo NewlineFilter (parser PLY)
"""

import sys
import pytest
from pathlib import Path

# Adiciona a raiz do projeto ao sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.tpplexer import get_lexer
from src.tppparser import get_parser
from tests.benchmark_lexers import ALL_STRATEGIES


def pytest_generate_tests(metafunc):
    """Gera os casos de teste dinamicamente com base na opção --lexer do pytest."""
    if "lexer_type" in metafunc.fixturenames:
        lexer_opt = metafunc.config.getoption("lexer")
        if lexer_opt == "all":
            lexers = ALL_STRATEGIES
        else:
            lexers = [lexer_opt]
        metafunc.parametrize("lexer_type", lexers)


def tokens_de(lexer_type, codigo):
    lexer = get_lexer(lexer_type, check_key=True)
    return [(t.type, t.lineno) for t in lexer.get_tokens(codigo)]


def test_chaves_e_comentarios(lexer_type, capsys):
    codigo = "A := {1, 2} {* c1 *}\n{*multi\n* } linha*}\nB := {{3}}\n"
    assert tokens_de(lexer_type, codigo) == [
        ("ID", 1), ("ATRIBUICAO", 1), ("ABRE_CHAVE", 1), ("NUM_INTEIRO", 1),
        ("VIRGULA", 1), ("NUM_INTEIRO", 1), ("FECHA_CHAVE", 1),
        ("ID", 4), ("ATRIBUICAO", 4), ("ABRE_CHAVE", 4), ("ABRE_CHAVE", 4),
        ("NUM_INTEIRO", 4), ("FECHA_CHAVE", 4), ("FECHA_CHAVE", 4),
    ]
    assert capsys.readouterr().out == ""


def test_comentario_nao_fechado(lexer_type, capsys):
    assert tokens_de(lexer_type, "x := 1\n{* aberto\n") == [
        ("ID", 1), ("ATRIBUICAO", 1), ("NUM_INTEIRO", 1),
    ]
    assert "ERR-LEX-UNC-COMMENT" in capsys.readouterr().out


PROGRAMA_VALIDO = """\
{* Retorno múltiplo, atribuição múltipla e inicialização de arrays *}
inteiro: A[6], M[2][2]
A := {1, 2, 3, 4, 5, 6}
M := {{1, 2}, {3, 4}}
(A[0], A[1]) := 9, 9

(inteiro, flutuante) divmod(inteiro: a, inteiro: b)
  retorna(a / b, a - (a / b) * b)
fim

inteiro principal()
  inteiro: x, y
  x, y := divmod(10, 3)
  x, y := y, x
  A[0], A[1] := A[1], A[0]
  A[x] := x := y := 0
  x, y := A[0], A[1] := 7, 8
  x := y
  (x, y) := y, x
  ((x), y) := (1, 2)
  x := x +
       y
  escreva(divmod(x,
                 y))
  se x > y então x := y fim
  se x > y então
    x := y
  senão y := x fim
  repita x := x - 1 até x = 0
  retorna(0)
fim
"""


def analisar(codigo):
    return get_parser("yacc", check_key=True).parse(codigo, check_key=True, check_gentree=True)


def test_parser_aceita_extensoes(capsys):
    raiz = analisar(PROGRAMA_VALIDO)
    saida = capsys.readouterr().out
    assert "ERR-" not in saida
    assert "WAR-SYN-ANA-SUCCESS" in saida
    nomes = {no.name for no in raiz.descendants}
    assert {"tipos_retorno", "lista_alvos", "lista_expressoes", "inicializacao_arranjo", "tupla"} <= nomes
    assert not {"bloco", "NEWLINE"} & nomes


def test_newline_separa_comandos(capsys):
    # Sem o NEWLINE, "y" seguido de "(x, y)" seria lido como a chamada y(x, y).
    raiz = analisar("inteiro principal()\n  x := y\n  (x, y) := 1, 2\nfim\n")
    assert "ERR-" not in capsys.readouterr().out
    nomes = [no.name for no in raiz.descendants]
    assert "chamada_funcao" not in nomes
    assert nomes.count("acao") == 2


@pytest.mark.parametrize("codigo", [
    "inteiro: x, y\nx := y := 0\n",
    "inteiro principal()\n  inteiro: x\n  x := {}\n  retorna(0)\nfim\n",
    "inteiro principal()\n  x := 1 y := 2\nfim\n",
    "inteiro principal()\n  se x > 0\n  então x := 1 fim\nfim\n",
])
def test_parser_rejeita(codigo, capsys):
    try:
        analisar(codigo)
    except AttributeError:
        # Regras de recuperação (p_*_error) sem ação devolvem None e quebram a
        # construção da árvore depois de reportar o erro.
        pass
    assert "ERR-SYN" in capsys.readouterr().out


# Declaração com inicialização: escalares, arranjos (também parcial) e
# atribuição encadeada, que declara só a primeira variável.
DECLARACOES_VALIDAS = [
    "inteiro: a := 1",
    "inteiro: a, b := 1, 2",
    "inteiro: v[5] := {1, 2, 3, 4, 5}",
    "inteiro: v[5] := {1, 2}",
    "inteiro: M[2][2] := {{1, 2}, {3, 4}}",
    "inteiro: a := b := 1",
    "inteiro: a := b := c := 1",
    "inteiro: v[2] := w := {1, 2}",
]

DECLARACOES_INVALIDAS = [
    "inteiro: a := b, c := 1",
    "inteiro: a, b := c, d := 1, 2",
    "inteiro: a := f() := 1",
]


def contextos(declaracao):
    """A declaração no escopo global e dentro de uma função."""
    return [declaracao + "\n", "f()\n  " + declaracao + "\nfim\n"]


@pytest.mark.parametrize("codigo", [c for d in DECLARACOES_VALIDAS for c in contextos(d)])
def test_declaracao_com_inicializacao(codigo, capsys):
    raiz = analisar(codigo)
    assert "ERR-" not in capsys.readouterr().out
    assert any(n.name == "declaracao_variaveis" and len(n.children) == 5 for n in raiz.descendants)


def test_arvore_atribuicao_encadeada(capsys):
    raiz = analisar("inteiro: a := b := c := 1\n")
    capsys.readouterr()
    decl = next(n for n in raiz.descendants if n.name == "declaracao_variaveis")
    assert [c.name for c in decl.children] == ["tipo", "DOIS_PONTOS", "lista_variaveis", "ATRIBUICAO", "atribuicao_encadeada"]
    elo1 = decl.children[4]
    assert [c.name for c in elo1.children] == ["lista_alvos", "ATRIBUICAO", "atribuicao_encadeada"]
    elo2 = elo1.children[2]
    assert [c.name for c in elo2.children] == ["lista_alvos", "ATRIBUICAO", "lista_expressoes"]
    alvos = [elo.children[0].children[0].children[0].children[0].name for elo in (elo1, elo2)]
    assert alvos == ["b", "c"]


@pytest.mark.parametrize("codigo", [c for d in DECLARACOES_INVALIDAS for c in contextos(d)])
def test_declaracao_com_inicializacao_rejeitada(codigo, capsys):
    try:
        analisar(codigo)
    except AttributeError:
        # Regras de recuperação (p_*_error) sem ação devolvem None.
        pass
    assert "ERR-SYN" in capsys.readouterr().out
