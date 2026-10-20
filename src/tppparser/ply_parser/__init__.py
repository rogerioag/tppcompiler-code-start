"""
Analisador sintático da linguagem TPP baseado em PLY (Yacc).

- ply_parser.py: monta o parser (yacc) e define o PLYParser.
- grammar/: regras da gramática, separadas por categoria.
- newline_filter.py: insere o token NEWLINE entre o lexer e o parser.
- estado.py: estado compartilhado entre as regras durante uma análise.
"""
