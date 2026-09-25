#!/usr/bin/env python3
# tests/benchmark_lexers.py
"""
Script de Benchmark e Análise de Desempenho dos Analisadores Léxicos do TPP.

Gera uma carga massiva de tokens representativa (palavras-chave, identificadores,
inteiros, flutuantes, notação científica, operadores e comentários) e mede:
- Tempo total decorrido (média, mínimo e máximo)
- Vazão (throughput) em tokens/segundo
- Comparação relativa (speedup vs baseline PLY)
- Verificação de conformidade na contagem e tipos dos tokens
"""

import sys
import time
import argparse
import statistics
from pathlib import Path

# Garante que a raiz do projeto esteja no sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.tpplexer import get_lexer

ALL_STRATEGIES = ["ply", "mandfa", "symtable", "symtableman", "automatalib", "automatalibman"]


def generate_large_tpp_code(num_blocks: int = 1500) -> str:
    """
    Gera um programa sintético em TPP contendo uma distribuição equilibrada de:
    - Palavras-chave: se, entao, repita, ate, inteiro, flutuante, fim, retorna
    - Identificadores: variáveis novas e reutilizadas
    - Literais numéricos: inteiros, decimais e notação científica
    - Operadores: :=, +, -, *, /, =, <, >, <=, >=, <>
    - Comentários de bloco { ... } e espaços em branco
    
    Cada bloco gera 46 tokens léxicos.
    Com 1.500 blocos = ~69.000 tokens.
    Com 2.500 blocos = ~115.000 tokens.
    """
    blocks = []
    for i in range(num_blocks):
        blocks.append(f"""
        {{ Bloco estruturado de processamento e stress léxico #{i} }}
        inteiro: cont_{i}, limite_{i}, acum_{i}
        flutuante: taxa_{i}, delta_{i}, total_{i}
        
        cont_{i} := 0
        acum_{i} := {i * 7} + 42
        taxa_{i} := 1.75e-3
        delta_{i} := 0.0052
        limite_{i} := {i} + 50
        
        repita
            se cont_{i} >= 10 entao
                total_{i} := taxa_{i} * 3.14159 + cont_{i} / 2.0 - delta_{i}
            senao
                total_{i} := delta_{i} * 1.5e2
            fim
            cont_{i} := cont_{i} + 1
            acum_{i} := acum_{i} * 2 - 1
        ate cont_{i} = limite_{i}
        """)
    return "\n".join(blocks)


def run_benchmark_for_strategy(strategy: str, code: str, rounds: int = 3, warmup: bool = True):
    """
    Executa a análise léxica em memória para uma estratégia específica,
    coletando métricas estatísticas ao longo de múltiplas rodadas.
    """
    # Rodada de aquecimento (warm-up) para carregar classes e JIT/caches
    if warmup:
        warmup_lex = get_lexer(strategy)
        warmup_lex.input(code[:5000])
        while warmup_lex.token():
            pass

    durations = []
    token_count = 0
    token_types_sample = []

    for r in range(rounds):
        lexer = get_lexer(strategy)
        lexer.input(code)
        
        count = 0
        t0 = time.perf_counter()
        while True:
            tok = lexer.token()
            if not tok:
                break
            count += 1
            if r == 0 and len(token_types_sample) < 50:
                token_types_sample.append(tok.type)
        t1 = time.perf_counter()
        
        durations.append(t1 - t0)
        token_count = count

    mean_time = statistics.mean(durations)
    min_time = min(durations)
    max_time = max(durations)
    std_dev = statistics.stdev(durations) if len(durations) > 1 else 0.0
    throughput = token_count / mean_time if mean_time > 0 else 0.0

    return {
        "strategy": strategy,
        "token_count": token_count,
        "mean_time": mean_time,
        "min_time": min_time,
        "max_time": max_time,
        "std_dev": std_dev,
        "throughput": throughput,
        "sample_tokens": token_types_sample,
    }


def format_table(results, baseline_strategy="ply", as_markdown=False):
    """Formata os resultados do benchmark em formato de tabela de texto ou Markdown."""
    baseline_result = next((r for r in results if r["strategy"] == baseline_strategy), results[0])
    baseline_time = baseline_result["mean_time"]

    headers = [
        "Estratégia",
        "Tokens",
        "Tempo Médio (s)",
        "Tempo Mín (s)",
        "Vazão (tokens/s)",
        "Relativo (vs PLY)",
    ]

    rows = []
    for r in results:
        ratio = baseline_time / r["mean_time"] if r["mean_time"] > 0 else 0.0
        rel_str = f"{ratio:.2f}x"
        if r["strategy"] == baseline_strategy:
            rel_str += " (baseline)"

        rows.append([
            r["strategy"],
            f"{r['token_count']:,}".replace(",", "."),
            f"{r['mean_time']:.4f}s",
            f"{r['min_time']:.4f}s",
            f"{r['throughput']:,.0f} tok/s".replace(",", "."),
            rel_str,
        ])

    if as_markdown:
        md_lines = []
        md_lines.append("| " + " | ".join(headers) + " |")
        md_lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
        for row in rows:
            md_lines.append("| " + " | ".join(row) + " |")
        return "\n".join(md_lines)
    else:
        col_widths = [max(len(row[i]) for row in [headers] + rows) for i in range(len(headers))]
        fmt_row = lambda r: "  ".join(f"{r[i]:<{col_widths[i]}}" for i in range(len(r)))

        sep = "=" * (sum(col_widths) + 2 * (len(col_widths) - 1))
        div = "-" * len(sep)

        lines = [sep, fmt_row(headers), div]
        for row in rows:
            lines.append(fmt_row(row))
        lines.append(sep)
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Benchmark de Performance dos Analisadores Léxicos do TPP"
    )
    parser.add_argument(
        "--blocks",
        type=int,
        default=2500,
        help="Número de blocos de código a gerar (~46 tokens por bloco; padrão: 2500 = ~115.000 tokens)",
    )
    parser.add_argument(
        "--rounds",
        type=int,
        default=3,
        help="Número de rodadas de teste por analisador (padrão: 3)",
    )
    parser.add_argument(
        "--lexers",
        type=str,
        default="all",
        help=f"Lista de estratégias separadas por vírgula ou 'all' (opções: {', '.join(ALL_STRATEGIES)})",
    )
    parser.add_argument(
        "--markdown",
        action="store_true",
        help="Exibe a tabela formatada em Markdown",
    )
    args = parser.parse_args()

    if args.lexers.lower() == "all":
        selected_strategies = ALL_STRATEGIES
    else:
        selected_strategies = [s.strip().lower() for s in args.lexers.split(",") if s.strip()]
        for s in selected_strategies:
            if s not in ALL_STRATEGIES:
                print(f"Erro: estratégia desconhecida '{s}'. Opções válidas: {ALL_STRATEGIES}")
                sys.exit(1)

    print(f"\n[+] Gerando código de entrada TPP com {args.blocks} blocos estruturados...")
    code = generate_large_tpp_code(num_blocks=args.blocks)
    estimated_size_kb = len(code.encode("utf-8")) / 1024
    print(f"    Tamanho do fonte: {estimated_size_kb:.1f} KB (~{len(code.splitlines())} linhas)\n")

    print(f"[+] Iniciando medições ({args.rounds} rodadas por estratégia com warm-up)...")
    results = []
    for strat in selected_strategies:
        print(f"    -> Testando '{strat}'...", end="", flush=True)
        r = run_benchmark_for_strategy(strat, code, rounds=args.rounds, warmup=True)
        results.append(r)
        print(f" concluído: {r['token_count']} tokens em {r['mean_time']:.4f}s ({r['throughput']:,.0f} tok/s)")

    # Validação de conformidade entre os resultados
    ref_tokens = results[0]["token_count"]
    mismatch = False
    for r in results[1:]:
        if r["token_count"] != ref_tokens:
            print(f"\n[!] AVISO DE CONFORMIDADE: '{r['strategy']}' gerou {r['token_count']} tokens, divergindo de '{results[0]['strategy']}' ({ref_tokens} tokens)!")
            mismatch = True

    if not mismatch:
        print(f"\n[✓] Conformidade verificada: todas as estratégias reconheceram exatamente {ref_tokens:,} tokens.".replace(",", "."))

    print("\n" + "=" * 80)
    print(f"RELATÓRIO DE BENCHMARK (Massa: {ref_tokens:,} tokens)".replace(",", "."))
    print("=" * 80)
    print(format_table(results, baseline_strategy="ply", as_markdown=args.markdown))
    print()


if __name__ == "__main__":
    main()
