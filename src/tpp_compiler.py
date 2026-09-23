import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
for path in (ROOT_DIR, BASE_DIR):
    if path not in sys.path:
        sys.path.insert(0, path)

import argparse
from src.myerror import MyError
from src.tpplexer import get_lexer
# from src.tppparser import get_parser

import logging
logging.basicConfig(
    filename = "tpp_compiler.log",
    encoding='utf-8',
    level = logging.DEBUG,
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s")

log = logging.getLogger()

syntax_tree = None
reduced_syntax_tree = None

# Adaptação para imprimir a chave ao invés da mensagem.
class ArgumentParser(argparse.ArgumentParser):
    def parse_args(self, args=None, namespace=None):
        self._current_args = args if args is not None else sys.argv[1:]
        return super().parse_args(args=args, namespace=namespace)

    def error(self, message):
        current_args = getattr(self, '_current_args', sys.argv[1:])
        if "-k" in current_args:
            ge = MyError('GlobalErrors')
            print(ge.newError(True, 'ERR-GLOB-USE'))
            sys.exit(0)
        super().error(message)


def main():
    cli = ArgumentParser(description="Compilador TPP Modular")
    cli.add_argument("fonte", help="arquivo-fonte .tpp")
    cli.add_argument("--lexer", choices=["ply", "manual", "symtable"], default="ply", help="Estratégia Léxica")
    cli.add_argument("--parser", choices=["yacc", "topdown"], default="yacc", help="Estratégia Sintática")
    cli.add_argument("--sema", "--semantic", default="default", help="Estratégia Semântica")
    cli.add_argument("--gencode", "--codegen", default="llvm", help="Estratégia de Geração de Código")
    cli.add_argument("-k", action="store_true", default=False, help="Imprimir chaves de Erro.")
    
    args = cli.parse_args()

    check_key = bool(args.k)

    ge = MyError('GlobalErrors')

    if not args.fonte or not args.fonte.strip():
        print(ge.newError(check_key, 'ERR-GLOB-USE'))
        return

    if not args.fonte.endswith('.tpp'):
        print(ge.newError(check_key, 'ERR-GLOB-NOT-TPP'))
        return

    if not os.path.exists(args.fonte):
        print(ge.newError(check_key, 'ERR-GLOB-FILE-NOT-EXISTS'))
        return

    if args.lexer:
        log.info("[lexer]: Executing Lexical Analysis.")
         # 1. Instancia o Lexer e o Parser dinamicamente
        lexer = get_lexer(args.lexer, check_key=check_key)
        # parser = get_parser(args.parser, lexer=lexer)

        data = open(args.fonte)

        source_file = data.read()
        # lexer.input(source_file)

        for token in lexer.get_tokens(source_file):
            #print(token.type, token.value)
            print(token.type)
    
    



#     if utils.args.parser:
#         syntax_tree = execute_syntax_analisys(source_input)
#     pass

#     if utils.args.semantic:
#        if syntax_tree != ():
#           reduced_syntax_tree = execute_semantic_analisys(syntax_tree)
#        else:
#            syntax_tree = execute_syntax_analisys(source_input)
#            reduced_syntax_tree = execute_semantic_analisys(syntax_tree)
#        pass
#     pass

#         if utils.args.gencode:
#             if reduced_syntax_tree != None:
#                 execute_code_generation(reduced_syntax_tree)
#             else:
#                 syntax_tree = execute_syntax_analisys(source_input)
#                 if syntax_tree != ():
#                     reduced_syntax_tree = execute_semantic_analisys(syntax_tree)
#                     execute_code_generation(reduced_syntax_tree)
#                 pass

#         pass

#     def execute_syntax_analisys(source_input):
#     log.info("[parser]: Executing Syntax Analysis.")
#     syntax_tree = parser.parse(source_input)
#     if syntax_tree != ():
#         print("Generating Syntax Tree Graph...")
#         graph = utils.Graph(utils.args.file, 'Sintax Tree')
#         # program = parser.parse(source_input)
#         syntax_tree.render(graph)
#         graph.export()
#     return syntax_tree

# def execute_semantic_analisys(syntax_tree):
#     log.info("[sema]: Executing Semantic Analysis.")
#     sema = Semantic(syntax_tree)
#     sema.check_semantic_rules()
#     return reduced_syntax_tree

# def execute_code_generation(reduced_syntax_tree):
#     log.info("[gencode]: Executing Code Generation.")
#     gencode = GenCode(reduced_syntax_tree)
#     gencode.generate()
#     return
   

    # ast = parser.parse(codigo)
    # print(f"Compilação concluída usando Léxico [{args.lexer.upper()}] + Sintático [{args.parser.upper()}]!")
   #  print(ge.newError(check_key, 'ERR-GLOB-COMP-COMPL-SUCCESS', 0, 0, args.lexer.upper(), args.parser.upper(), args.sema.upper(), args.gencode.upper()))

if __name__ == "__main__":
    main()









# def main():

#     global check_tpp
#     global check_key

#     check_tpp = False
#     check_key = False
#     has_file_arg = False
#     idx_tpp = -1

#     for idx, arg in enumerate(sys.argv[1:], start=1):
#         if arg == "-k":
#             check_key = True
#         else:
#             has_file_arg = True
#             aux = arg.split('.')
#             if aux[-1] == 'tpp':
#                 check_tpp = True
#                 idx_tpp = idx

#     if not has_file_arg:
#         raise TypeError(le.newError(check_key, 'ERR-LEX-USE'))
#     elif not check_tpp:
#         raise IOError(le.newError(check_key, 'ERR-LEX-NOT-TPP'))
#     elif not os.path.exists(sys.argv[idx_tpp]):
#         raise IOError(le.newError(check_key, 'ERR-LEX-FILE-NOT-EXISTS'))
#     else:
#         data = open(argv[idx_tpp])

#         source_file = data.read()
#         lexer.input(source_file)

#         # Tokenize
#         while True:
#             tok = lexer.token()
#             if not tok:
#                 break      # No more input
#             #print(tok)
#             print(tok.type)
#             #print(tok.value)




# if __name__ == "__main__":

#     try:
#         main()
#     except Exception as e:
#         print(e)
#     except (ValueError, TypeError):
#         print(e)
