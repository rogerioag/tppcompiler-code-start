# tests/test_perf_large_tokens.py
"""
Teste de Desempenho e Stress Léxico com Grande Sequência de Tokens.

Gera um programa sintético em TPP contendo dezenas de milhares de tokens
e valida para a estratégia selecionada via --lexer:
1. Tempo de execução e vazão (throughput em tokens/s)
2. Conformidade e ausência de erros léxicos
3. Paridade estrita dos tipos de tokens gerados em relação ao baseline PLY
"""

import sys
import time
import pytest
from pathlib import Path

# Adiciona a raiz do projeto ao sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.tpplexer import get_lexer
from tests.benchmark_lexers import generate_large_tpp_code, ALL_STRATEGIES

# Quantidade de blocos para o teste de performance automatizado (~36.500 tokens)
BENCHMARK_BLOCKS = 500


def pytest_generate_tests(metafunc):
    """Gera os casos de teste dinamicamente com base na opção --lexer do pytest."""
    if "lexer_type" in metafunc.fixturenames:
        lexer_opt = metafunc.config.getoption("lexer")
        if lexer_opt == "all":
            lexers = ALL_STRATEGIES
        else:
            lexers = [lexer_opt]
        metafunc.parametrize("lexer_type", lexers)


@pytest.fixture(scope="module")
def large_tpp_code():
    """Gera o código de teste uma única vez por sessão de teste para economizar CPU."""
    return generate_large_tpp_code(num_blocks=BENCHMARK_BLOCKS)


@pytest.fixture(scope="module")
def baseline_tokens(large_tpp_code):
    """Extrai os tipos de tokens de referência usando o PLYLexer (baseline)."""
    ref_lexer = get_lexer("ply")
    ref_lexer.input(large_tpp_code)
    tokens = []
    while True:
        tok = ref_lexer.token()
        if not tok:
            break
        tokens.append(tok.type)
    return tokens


def test_large_token_sequence_performance(lexer_type, large_tpp_code):
    """
    Mede o tempo de processamento para uma massa grande de tokens (>36.000 tokens).
    Verifica a taxa de transferência (tokens/segundo) e a ausência de erros.
    """
    lexer = get_lexer(lexer_type)
    lexer.input(large_tpp_code)

    token_count = 0
    start_time = time.perf_counter()

    while True:
        tok = lexer.token()
        if not tok:
            break
        token_count += 1

    elapsed_time = time.perf_counter() - start_time
    throughput = token_count / elapsed_time if elapsed_time > 0 else 0.0

    print(
        f"\n[PERFORMANCE] Lexer: {lexer_type:<15} | Tokens: {token_count:,} | "
        f"Tempo: {elapsed_time:.4f}s | Vazão: {throughput:,.0f} tok/s".replace(",", ".")
    )

    # Asserções de integridade
    assert token_count > 0, "Nenhum token foi gerado pelo analisador léxico"
    assert elapsed_time < 5.0, f"O analisador {lexer_type} demorou mais de 5s ({elapsed_time:.2f}s)"


def test_token_types_conformance_with_baseline(lexer_type, large_tpp_code, baseline_tokens):
    """
    Verifica se a sequência exata de tipos de tokens gerada pela estratégia
    coincide integralmente com os tipos de tokens emitidos pelo baseline PLY.
    """
    lexer = get_lexer(lexer_type)
    lexer.input(large_tpp_code)

    current_tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        current_tokens.append(tok.type)

    assert len(current_tokens) == len(baseline_tokens), (
        f"Divergência na quantidade de tokens para '{lexer_type}': "
        f"esperado {len(baseline_tokens)}, obtido {len(current_tokens)}"
    )

    # Verifica os primeiros 500 tokens para diagnosticar divergências de forma detalhada
    sample_size = min(500, len(baseline_tokens))
    for idx in range(sample_size):
        assert current_tokens[idx] == baseline_tokens[idx], (
            f"Divergência de token no índice {idx} ({lexer_type}): "
            f"esperado '{baseline_tokens[idx]}', obtido '{current_tokens[idx]}'"
        )

    # Asserção de paridade total
    assert current_tokens == baseline_tokens, (
        f"A sequência completa de tokens divergiu para o lexer '{lexer_type}'"
    )


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main(sys.argv[1:] + [__file__]))
