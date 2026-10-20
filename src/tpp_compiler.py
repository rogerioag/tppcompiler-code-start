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
from src.tppparser import get_parser

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

# Etapas do compilador, em ordem. A última etapa passada na linha de comando
# define até onde a compilação vai; as anteriores executam com a estratégia
# passada ou, se omitida, com a estratégia padrão.
ETAPAS = ["lexer", "parser", "sema", "gencode"]
ESTRATEGIAS_PADRAO = {"lexer": "ply", "parser": "yacc", "sema": "sema", "gencode": "llvm"}
OPCOES_ETAPAS = {
    "lexer": ("--lexer",),
    "parser": ("--parser",),
    "sema": ("--sema", "--semantic"),
    "gencode": ("--gencode", "--codegen"),
}


def etapa_final(argv):
    """Retorna a etapa mais avançada pedida em argv ('lexer' se nenhuma for passada)."""
    final = "lexer"
    for etapa in ETAPAS:
        if any(arg == opcao or arg.startswith(opcao + "=") for arg in argv for opcao in OPCOES_ETAPAS[etapa]):
            final = etapa
    return final


def tratador_de_erros(etapa):
    """Mensagens de uso/arquivo: chaves ERR-SYN-* na análise sintática, ERR-GLOB-* nas demais."""
    if etapa == "parser":
        return MyError('ParserErrors'), 'ERR-SYN'
    return MyError('GlobalErrors'), 'ERR-GLOB'


# Adaptação para imprimir a chave ao invés da mensagem.
class ArgumentParser(argparse.ArgumentParser):
    def parse_args(self, args=None, namespace=None):
        self._current_args = args if args is not None else sys.argv[1:]
        return super().parse_args(args=args, namespace=namespace)

    def error(self, message):
        current_args = getattr(self, '_current_args', sys.argv[1:])
        if "-k" in current_args:
            err_handler, prefix = tratador_de_erros(etapa_final(current_args))
            print(err_handler.newError(True, f'{prefix}-USE'))
            sys.exit(0)
        super().error(message)


def main():
    cli = ArgumentParser(description="Compilador TPP [tppc]")
    cli.add_argument("fonte", help="arquivo-fonte .tpp")
    # default=None para saber quais etapas foram pedidas; as estratégias padrão
    # são aplicadas depois (ESTRATEGIAS_PADRAO).
    cli.add_argument("--lexer", choices=["ply", "mandfa", "symtable", "symtableman", "automatalib", "automatalibman"], default=None, help="Estratégia Léxica (padrão: ply)")
    cli.add_argument("--parser", choices=["yacc", "topdown"], default=None, help="Estratégia Sintática (padrão: yacc). Executa também a Análise Léxica.")
    cli.add_argument("--sema", "--semantic", choices=["sema"], default=None, help="Estratégia Semântica (padrão: sema). Executa também as Análises Léxica e Sintática.")
    cli.add_argument("--gencode", "--codegen", choices=["llvm"], default=None, help="Estratégia de Geração de Código (padrão: llvm). Executa também as etapas anteriores.")
    cli.add_argument("-k", action="store_true", default=False, help="Imprimir chaves de Erro.")
    cli.add_argument("-t", "--tree", action="store_true", default=False, help="Gerar Árvore Sintática.")
    
    args = cli.parse_args()

    final = etapa_final(sys.argv[1:])
    for etapa in ETAPAS:
        if getattr(args, etapa) is None:
            setattr(args, etapa, ESTRATEGIAS_PADRAO[etapa])

    check_key = bool(args.k)
    err_handler, prefix = tratador_de_erros(final)

    if not args.fonte or not args.fonte.strip():
        print(err_handler.newError(check_key, f'{prefix}-USE'))
        return

    if not args.fonte.endswith('.tpp'):
        print(err_handler.newError(check_key, f'{prefix}-NOT-TPP'))
        return

    if not os.path.exists(args.fonte):
        print(err_handler.newError(check_key, f'{prefix}-FILE-NOT-EXISTS'))
        return

    with open(args.fonte, "r") as data:
        source_file = data.read()

    if final == "lexer":
        log.info("[lexer]: Executing Lexical Analysis.")
        lexer = get_lexer(args.lexer, check_key=check_key)
        for token in lexer.get_tokens(source_file):
            print(token.type)
        return

    # A partir da Análise Sintática, a Análise Léxica é feita sob demanda pelo
    # parser (que pede os tokens ao lexer escolhido), sem imprimir os tokens.
    log.info("[parser]: Executing Syntax Analysis (lexer: %s).", args.lexer)
    parser = get_parser(args.parser, check_key=check_key, check_gentree=args.tree, lexer=args.lexer)
    syntax_tree = parser.parse(source_file, filename=args.fonte, check_key=check_key, check_gentree=args.tree)
    if final == "parser":
        return

    # TODO: Análise Semântica (args.sema) sobre syntax_tree.
    log.info("[sema]: Semantic Analysis not implemented yet.")
    print("Análise Semântica ainda não implementada.", file=sys.stderr)
    if final == "sema":
        return

    # TODO: Geração de Código (args.gencode) sobre a árvore reduzida.
    log.info("[gencode]: Code Generation not implemented yet.")
    print("Geração de Código ainda não implementada.", file=sys.stderr)

    
    
    

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
