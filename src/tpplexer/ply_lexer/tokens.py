"""
tokens.py - Definições de Tokens e Palavras Reservadas para a Linguagem TPP.
"""

__all__ = [
    "tokens",
    "reserved_words",
    "reserved",
    "markers",
    "math_symbols",
    "logical_symbols",
    "comparison_symbols",
    "control_symbols",
    "TOKENS_SYMBOLS",
]

# Palavras reservadas da linguagem TPP
reserved_words = {
    "se": "SE",
    "então": "ENTAO",
    "senão": "SENAO",
    "fim": "FIM",
    "repita": "REPITA",
    "flutuante": "FLUTUANTE",
    "retorna": "RETORNA",
    "até": "ATE",
    "leia": "LEIA",
    "escreva": "ESCREVA",
    "inteiro": "INTEIRO",
}

# Alias para compatibilidade
reserved = reserved_words

# Identificadores e numerais
markers = [
    "ID",
    "NUM_NOTACAO_CIENTIFICA",
    "NUM_PONTO_FLUTUANTE",
    "NUM_INTEIRO",
]

# Operadores aritméticos binários
math_symbols = [
    "MAIS",   # +
    "MENOS",  # -
    "VEZES",  # *
    "DIVIDE", # /
]

# Operadores lógicos
logical_symbols = [
    "E",   # &&
    "OU",  # ||
    "NAO", # !
]

# Operadores relacionais
comparison_symbols = [
    "DIFERENTE",   # <>
    "MENOR_IGUAL", # <=
    "MAIOR_IGUAL", # >=
    "MENOR",       # <
    "MAIOR",       # >
    "IGUAL",       # =
]

# Símbolos delimitadores e atribuição
control_symbols = [
    "ABRE_PARENTESE",  # (
    "FECHA_PARENTESE", # )
    "ABRE_COLCHETE",   # [
    "FECHA_COLCHETE",  # ]
    "VIRGULA",         # ,
    "DOIS_PONTOS",     # :
    "ATRIBUICAO",      # :=
]

# Lista completa de tokens reconhecidos pelo PLY
tokens = (
    markers
    + math_symbols
    + logical_symbols
    + comparison_symbols
    + control_symbols
    + list(reserved_words.values())
)

# Mapeamento para visualização/conversão de símbolos
TOKENS_SYMBOLS = {
    # Aritméticos
    "MAIS": "+",
    "MENOS": "-",
    "VEZES": "*",
    "DIVIDE": "/",
    # Lógicos
    "E": "&&",
    "OU": "||",
    "NAO": "!",
    # Relacionais
    "DIFERENTE": "<>",
    "MENOR_IGUAL": "<=",
    "MAIOR_IGUAL": ">=",
    "MENOR": "<",
    "MAIOR": ">",
    "IGUAL": "=",
    # Delimitadores
    "ABRE_PARENTESE": "(",
    "FECHA_PARENTESE": ")",
    "ABRE_COLCHETE": "[",
    "FECHA_COLCHETE": "]",
    "VIRGULA": ",",
    "DOIS_PONTOS": ":",
    "ATRIBUICAO": ":=",
    # Palavras Reservadas
    "SE": "se",
    "ENTAO": "então",
    "SENAO": "senão",
    "FIM": "fim",
    "REPITA": "repita",
    "FLUTUANTE": "flutuante",
    "RETORNA": "retorna",
    "ATE": "até",
    "LEIA": "leia",
    "ESCREVA": "escreva",
    "INTEIRO": "inteiro",
}
