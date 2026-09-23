"""
regexs.py - Expressões Regulares e padrões da linguagem TPP.
"""

# Padrões base para construção de regras complexas
digito = r"([0-9])"
letra = r"([a-zA-ZáÁãÃàÀéÉíÍóÓõÕ])"
sinal = r"([\-\+]?)"

# Identificador (inicia com letra, seguido de letras, dígitos ou sublinhado)
id_regex = r"(" + letra + r"(" + digito + r"+|_|" + letra + r")*)"

# Numerais
inteiro = r"\d+"
flutuante = r'\d+[eE][-+]?\d+|(\.\d+|\d+\.\d*)([eE][-+]?\d+)?'
notacao_cientifica = (
    r"(" + sinal + r"([1-9])\." + digito + r"+[eE]" + sinal + digito + r"+)"
)

# Aliases com sufixo _regex para conveniência
inteiro_regex = inteiro
flutuante_regex = flutuante
notacao_cientifica_regex = notacao_cientifica

# Símbolos / Delimitadores
t_MAIS = r'\+'
t_MENOS = r'-'
t_VEZES = r'\*'
t_DIVIDE = r'/'
t_ABRE_PARENTESE = r'\('
t_FECHA_PARENTESE = r'\)'
t_ABRE_COLCHETE = r'\['
t_FECHA_COLCHETE = r'\]'
t_VIRGULA = r','
t_ATRIBUICAO = r':='
t_DOIS_PONTOS = r':'

# Operadores Lógicos
t_E = r'&&'
t_OU = r'\|\|'
t_NAO = r'!'

# Operadores Relacionais
t_DIFERENTE = r'<>'
t_MENOR_IGUAL = r'<='
t_MAIOR_IGUAL = r'>='
t_MENOR = r'<'
t_MAIOR = r'>'
t_IGUAL = r'='
