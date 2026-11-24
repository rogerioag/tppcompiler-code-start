import fnmatch
import os
import shlex
import subprocess
import sys

import pytest

# Organização dos testes da Fase 4 (Geração de Código):
#
# 1. test_execute (saída do compilador):
#    Compila 'tests/codegen-tests/<nome>.tpp' via CLI (src/tpp_compiler.py --codegen ...)
#    e compara a saída padrão com 'tests/codegen-tests/<nome>.tpp.codegen.out'.
#    Inclui também os casos de validação de entrada (vazio, extensão inválida, inexistente).
#
# 2. test_llvm_ir (comparação do LLVM-IR gerado):
#    Para cada '<nome>.tpp' que possuir um arquivo de referência '<nome>.tpp.ll.out',
#    executa o compilador para gerar '<nome>.tpp.ll' e compara com '<nome>.tpp.ll.out'
#    usando 'llvm-diff'.
#
# 3. test_code_execution (compilação e execução do binário gerado):
#    Para cada '<nome>.tpp' que possuir '<nome>.tpp.ll.exe.out', gera '<nome>.tpp.ll',
#    compila com 'clang' para um executável temporário, executa o binário (fornecendo
#    '<nome>.tpp.in' na entrada padrão, se existir) e compara a saída com
#    '<nome>.tpp.ll.exe.out'.

CODEGEN_TESTS_DIR = "tests/codegen-tests"


def _listar_estrategias(config):
    codegen_opt = config.getoption("codegen")
    if codegen_opt == "all":
        return ["llvm"]
    return [codegen_opt]


def pytest_generate_tests(metafunc):
    """Gera dinamicamente os casos de teste com base na opção --codegen."""
    codegens = _listar_estrategias(metafunc.config)
    files = sorted(fnmatch.filter(os.listdir(CODEGEN_TESTS_DIR), "*.tpp"))

    if "key_option" in metafunc.fixturenames:
        cases = []
        for codegen in codegens:
            cases.append((codegen, "-k", ""))
            cases.append((codegen, "-k", "teste.c"))
            cases.append((codegen, "-k", "notexist.tpp"))

        for file in files:
            for codegen in codegens:
                cases.append((codegen, "-k", file))

        metafunc.parametrize("codegen_type, key_option, input_file", cases)

    elif metafunc.function.__name__ == "test_llvm_ir":
        cases = [
            (codegen, file)
            for file in files
            if os.path.exists(os.path.join(CODEGEN_TESTS_DIR, file + ".ll.out"))
            for codegen in codegens
        ]
        metafunc.parametrize("codegen_type, input_file", cases)

    elif metafunc.function.__name__ == "test_code_execution":
        cases = [
            (codegen, file)
            for file in files
            if os.path.exists(os.path.join(CODEGEN_TESTS_DIR, file + ".ll.exe.out"))
            for codegen in codegens
        ]
        metafunc.parametrize("codegen_type, input_file", cases)


def test_execute(codegen_type, key_option, input_file):
    if input_file != "":
        path_file = os.path.join(CODEGEN_TESTS_DIR, input_file)
    else:
        path_file = ""

    cmd = "python src/tpp_compiler.py --codegen {0} {1} {2}".format(
        codegen_type, key_option, path_file
    )
    process = subprocess.Popen(
        shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    expected_path = os.path.join(CODEGEN_TESTS_DIR, input_file + ".codegen.out")
    with open(expected_path, "r", encoding="utf-8") as output_file:
        expected_output = output_file.read()

    print("Generated output:")
    print(stdout)
    print("Expected output:")
    print(expected_output)

    assert stdout.decode("utf-8").strip() == expected_output.strip()


def test_llvm_ir(codegen_type, input_file):
    path_file = os.path.join(CODEGEN_TESTS_DIR, input_file)
    generated_ll = path_file + ".ll"
    expected_ll = path_file + ".ll.out"

    if os.path.exists(generated_ll):
        os.remove(generated_ll)

    cmd = [sys.executable, "src/tpp_compiler.py", "--codegen", codegen_type, "-k", path_file]
    compile_res = subprocess.run(cmd, capture_output=True, text=True)
    assert compile_res.returncode == 0, compile_res.stderr
    assert os.path.exists(generated_ll), f"Arquivo LLVM-IR não gerado: {generated_ll}"

    diff_res = subprocess.run(
        ["llvm-diff", generated_ll, expected_ll],
        capture_output=True,
        text=True,
    )
    print("llvm-diff stdout:")
    print(diff_res.stdout)
    print("llvm-diff stderr:")
    print(diff_res.stderr)

    assert diff_res.returncode == 0 and diff_res.stdout.strip() == "" and diff_res.stderr.strip() == ""


def test_code_execution(codegen_type, input_file, tmp_path):
    path_file = os.path.join(CODEGEN_TESTS_DIR, input_file)
    generated_ll = path_file + ".ll"
    expected_exe_out = path_file + ".ll.exe.out"
    stdin_file = path_file + ".in"

    if os.path.exists(generated_ll):
        os.remove(generated_ll)

    cmd = [sys.executable, "src/tpp_compiler.py", "--codegen", codegen_type, "-k", path_file]
    compile_res = subprocess.run(cmd, capture_output=True, text=True)
    assert compile_res.returncode == 0, compile_res.stderr
    assert os.path.exists(generated_ll), f"Arquivo LLVM-IR não gerado: {generated_ll}"

    exe_name = input_file + ".ll.exe"
    exe_path = str(tmp_path / exe_name)

    clang_res = subprocess.run(
        ["clang", generated_ll, "-o", exe_path],
        capture_output=True,
        text=True,
    )
    assert clang_res.returncode == 0, f"Erro ao compilar LLVM-IR com clang:\n{clang_res.stderr}"

    stdin_data = None
    if os.path.exists(stdin_file):
        with open(stdin_file, "r", encoding="utf-8") as f:
            stdin_data = f.read()

    run_res = subprocess.run(
        [exe_path],
        input=stdin_data,
        capture_output=True,
        text=True,
    )

    with open(expected_exe_out, "r", encoding="utf-8") as f:
        expected_output = f.read()

    print("Program output:")
    print(run_res.stdout)
    print("Expected output:")
    print(expected_output)

    assert run_res.stdout.strip() == expected_output.strip()


if __name__ == "__main__":
    sys.exit(pytest.main(sys.argv[1:] + [__file__]))
