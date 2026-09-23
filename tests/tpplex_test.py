import pytest
import subprocess
import shlex
import os, fnmatch

# test_cases = [
#     ("", "-k"), 
#     ("teste.c", "-k"), 
#     ("notexist.tpp", "-k"), 
#     ("lex-test-001.tpp", "-k"), 
#     ("lex-test-002.tpp", "-k"), 
#     ("lex-test-003.tpp", "-k"), 
#     ("lex-test-004.tpp", "-k"), 
#     ("lex-test-005.tpp", "-k"), 
#     ("lex-teste-006.tpp", "-k"), 
#     ("bubble_sort_2.tpp", "-k"), 
#     ("bubble_sort.tpp", "-k"), 
#     ("Busca_Linear_1061992.tpp", "-k"), 
#     ("buscaLinear-2020-2.tpp", "-k"), 
#     ("comp.tpp", "-k"), 
#     ("fatorial-2020-2.tpp", "-k"), 
#     ("fatorial.tpp", "-k"), 
#     ("fat.tpp", "-k"), 
#     ("fibonacci-2020-2.tpp", "-k"), 
#     ("fibonacci.tpp", "-k"), 
#     ("hanoi-2020-2.tpp", "-k"), 
#     ("insertionSort-2020-2.tpp", "-k"), 
#     ("insertSort-2020-2.tpp", "-k"), 
#     ("maiorDoVetor.tpp", "-k"), 
#     ("multiplicavetor.tpp", "-k"),
#     ("operacao_vetor-2020-2.tpp", "-k"), 
#     ("paraBinario-2020-2.tpp", "-k"), 
#     ("primo.tpp", "-k"), 
#     ("produtoEscalar.tpp", "-k"), 
#     ("prog_test.tpp", "-k"), 
#     ("sample.tpp", "-k"), 
#     ("selectionSort-2020-2.tpp", "-k"), 
#     ("selectionsort.tpp", "-k"), 
#     ("soma_maior_que_3.tpp", "-k"), 
#     ("somavet.tpp", "-k"), 
#     ("subtraiVetores.tpp", "-k"), 
#     ("verifica_valor_10.tpp", "-k"), 
#     ("verif_num_negativo.tpp", "-k"), 
#     ("bubble_sort-2020-2.tpp", "-k")
# ]

# Testes para se passar um arquivo em branco, um arquivo com outra extensão e um arquivo .tpp que não existe.
test_cases = [("ply", "-k", ""), ("ply", "-k", "teste.c"), ("ply", "-k", "notexist.tpp")]

files = fnmatch.filter(os.listdir('tests/lex-tests/'), '*.tpp')
for file in sorted(files):
    test_cases.append(("ply", "-k", file))
    

@pytest.mark.parametrize("lexer_type, key_option, input_file", test_cases)
def test_execute(lexer_type, key_option, input_file):
    if(input_file != ''):
        path_file = 'tests/lex-tests/' + input_file
    else:
        path_file = ""
    
    # Executa o comando de compilação.
    cmd = "python src/tpp_compiler.py --lexer {0} {1} {2}".format(lexer_type, key_option, path_file)

    process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    stdout, stderr = process.communicate()
    stdout, stderr

    path_file = 'tests/lex-tests/' + input_file
    output_file = open(path_file + ".lex.out", "r")

    #read whole file to a string
    expected_output = output_file.read()

    output_file.close()

    print("Generated output:")
    print(stdout)
    print("Expected output:")
    print(expected_output)

    assert stdout.decode("utf-8").strip() == expected_output.strip()

