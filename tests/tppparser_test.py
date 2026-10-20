import pytest
import subprocess
import shlex
import os, fnmatch

def pytest_generate_tests(metafunc):
    """Gera dinamicamente os casos de teste com base na opção --parser."""
    parser_opt = metafunc.config.getoption("parser")

    if parser_opt == "all":
        parsers = ["yacc"]
    else:
        parsers = [parser_opt]

    # Testes para se passar um arquivo em branco, um arquivo com outra extensão e um arquivo .tpp que não existe.
    cases = []
    for parser in parsers:
        cases.append((parser, "-k", ""))
        cases.append((parser, "-k", "teste.c"))
        cases.append((parser, "-k", "notexist.tpp"))

    # Arquivos de teste .tpp
    files = sorted(fnmatch.filter(os.listdir('tests/syn-tests/'), '*.tpp'))
    for file in files:
        for parser in parsers:
            cases.append((parser, "-k", file))

    metafunc.parametrize("parser_type, key_option, input_file", cases)


# @pytest.mark.parametrize("parser_type, key_option, input_file", test_cases)
def test_execute(parser_type, key_option, input_file):
    if(input_file != ''):
        path_file = 'tests/syn-tests/' + input_file
    else:
        path_file = ""

    # Executa o comando de compilação. O -t gera a árvore sintática (e os arquivos
    # .ast.dot, .unique.ast.dot, .unique.ast.png e ascii_tree.txt ao lado do .tpp).
    cmd = "python src/tpp_compiler.py --parser {0} {1} -t {2}".format(parser_type, key_option, path_file)

    process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = process.communicate()
    stdout, stderr

    path_file = 'tests/syn-tests/' + input_file
    output_file = open(path_file + ".syn.out", "r")

    #read whole file to a string
    expected_output = output_file.read()

    output_file.close()

    print("Generated output:")
    print(stdout)
    print("Expected output:")
    print(expected_output)

    assert stdout.decode("utf-8").strip() == expected_output.strip()


if __name__ == "__main__":
    import sys
    sys.exit(pytest.main(sys.argv[1:] + [__file__]))
