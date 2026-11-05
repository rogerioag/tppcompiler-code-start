import pytest
import subprocess
import shlex
import os, fnmatch

def pytest_generate_tests(metafunc):
    """Gera dinamicamente os casos de teste com base na opção --sema."""
    sema_opt = metafunc.config.getoption("sema")

    if sema_opt == "all":
        semas = ["sema"]
    else:
        semas = [sema_opt]

    # Testes para se passar um arquivo em branco, um arquivo com outra extensão e um arquivo .tpp que não existe.
    cases = []
    for sema in semas:
        cases.append((sema, "-k", ""))
        cases.append((sema, "-k", "teste.c"))
        cases.append((sema, "-k", "notexist.tpp"))

    # Arquivos de teste .tpp
    files = sorted(fnmatch.filter(os.listdir('tests/sem-tests/'), '*.tpp'))
    for file in files:
        for sema in semas:
            cases.append((sema, "-k", file))

    metafunc.parametrize("sema_type, key_option, input_file", cases)


# @pytest.mark.parametrize("sema_type, key_option, input_file", test_cases)
def test_execute(sema_type, key_option, input_file):
    if(input_file != ''):
        path_file = 'tests/sem-tests/' + input_file
    else:
        path_file = ""

    # Executa o comando de compilação.
    cmd = "python src/tpp_compiler.py --sema {0} {1} {2}".format(sema_type, key_option, path_file)

    process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = process.communicate()
    stdout, stderr

    path_file = 'tests/sem-tests/' + input_file
    output_file = open(path_file + ".sem.out", "r")

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
