"""
newline_filter.py - Inserção do token NEWLINE entre o lexer e o parser.
"""

from ply.lex import LexToken


class NewlineFilter:
    """
    Insere o token NEWLINE no fim das linhas que terminam um comando, como a
    inserção automática de ';' do Go. Uma quebra de linha vira NEWLINE quando:
      - o último token da linha pode encerrar um comando (TERMINADORES); e
      - ela não está dentro de (), [] ou {}.
    Depois de 'então', 'senão', 'repita', 'até', operadores e ',' a quebra de
    linha é apenas continuação. No fim da entrada também é inserido um NEWLINE.
    """

    TERMINADORES = {'ID', 'NUM_INTEIRO', 'NUM_PONTO_FLUTUANTE', 'NUM_NOTACAO_CIENTIFICA',
                    'FECHA_PARENTESE', 'FECHA_COLCHETE', 'FECHA_CHAVE', 'FIM'}
    ABERTURAS = {'ABRE_PARENTESE', 'ABRE_COLCHETE', 'ABRE_CHAVE'}
    FECHAMENTOS = {'FECHA_PARENTESE', 'FECHA_COLCHETE', 'FECHA_CHAVE'}

    def __init__(self, lexer):
        self.lexer = lexer
        self.input("")

    def input(self, data):
        self.lexer.input(data)
        self.anterior = None
        self.pendentes = []
        self.nivel = 0

    def token(self):
        if self.pendentes:
            return self._registra(self.pendentes.pop())

        tok = self.lexer.token()
        ant = self.anterior
        if (ant is not None and ant.type in self.TERMINADORES and self.nivel == 0
                and (tok is None or tok.lineno > ant.lineno)):
            if tok is not None:
                self.pendentes.append(tok)
            nl = LexToken()
            nl.type = 'NEWLINE'
            nl.value = '\\n'
            nl.lineno = ant.lineno
            nl.lexpos = ant.lexpos + len(str(ant.value))
            self.anterior = nl
            return nl

        return self._registra(tok)

    def _registra(self, tok):
        if tok is not None:
            if tok.type in self.ABERTURAS:
                self.nivel += 1
            elif tok.type in self.FECHAMENTOS:
                self.nivel = max(0, self.nivel - 1)
            self.anterior = tok
        return tok
