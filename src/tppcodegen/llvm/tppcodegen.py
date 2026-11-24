# src/tppcodegen/llvm/tppcodegen.py
"""
LLVMCodeGen: gerador de código LLVM-IR da linguagem TPP.

Recebe a árvore sintática abstrata podada (ASA) produzida pela análise
semântica (src/tppsema), percorre as declarações e comandos emitindo código
LLVM-IR via llvmlite e grava o resultado em '<arquivo>.tpp.ll'.
"""

import os

from src.myerror import MyError
from src.tppcodegen.base import BaseCodeGen
from src.tppcodegen.llvm.context import ContextoLLVM
from src.tppcodegen.llvm import emitters


class LLVMCodeGen(BaseCodeGen):
    """
    Gerador de código intermediário LLVM-IR para a linguagem TPP.
    """

    def __init__(self, check_key: bool = False, **kwargs):
        self.check_key = check_key
        self.error_handler = MyError('CodeGenErrors')
        self.contexto = ContextoLLVM()
        self.erros = 0
        self.avisos = 0

    def emitir(self, chave: str, *args, linha=None, coluna=None, **data):
        """
        Imprime uma mensagem de erro (ERR-CODEGEN-*) ou de aviso (WAR-CODEGEN-*).

        Com a opção -k, imprime apenas a chave; caso contrário, imprime a
        mensagem do CodeGenErrorMessages.properties, formatada com args/data.
        """
        if chave.startswith('ERR-'):
            self.erros += 1
        else:
            self.avisos += 1
        print(self.error_handler.newError(self.check_key, chave, linha, coluna, *args, **data))

    def generate(self, tree, filename: str = "", symbol_table=None, check_key: bool = None, **kwargs):
        """
        Gera o código LLVM-IR a partir de 'tree' e salva em '<filename>.ll'.
        """
        if check_key is not None:
            self.check_key = check_key
        self.erros = 0
        self.avisos = 0

        module_name = os.path.basename(filename) if filename else "tpp_module"
        output_file = f"{filename}.ll" if filename else "output.ll"

        self.contexto = ContextoLLVM()
        self.contexto.setup(module_name, symbol_table=symbol_table)

        # TODO (alunos): percorrer a árvore sintática abstrata (ASA) utilizando
        # os módulos em src/tppcodegen/llvm/emitters/ (declarations, functions,
        # commands, expressions, io) para construir o módulo LLVM-IR.
        _ = (tree, emitters)

        # TODO (alunos): ao concluir a geração de código, salvar o arquivo '.ll'
        # e emitir as mensagens de saída e sucesso:
        #   self.contexto.salvar(output_file)
        #   self.emitir('WAR-CODEGEN-OUTPUT-FILE', file=output_file)
        #   self.emitir('WAR-CODEGEN-SUCCESS')
        _ = output_file

        return self.contexto.module
