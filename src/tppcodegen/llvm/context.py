# src/tppcodegen/llvm/context.py
"""
Contexto de geração de código LLVM-IR (llvmlite).

TODO (alunos): estruturar o contexto compartilhado entre os emissores durante a
travessia da ASA, mantendo:
  - o módulo LLVM (llvmlite.ir.Module) e a configuração de target/triple/datalayout;
  - o IRBuilder da função e do bloco básico atuais;
  - o mapeamento de tipos TPP -> LLVM (inteiro -> i32, flutuante -> float, vazio -> void);
  - a tabela de endereços/alocações (globais e locais por escopo);
  - o registro de funções declaradas no módulo e funções externas de E/S (leia/escreva).
"""


class ContextoLLVM:
    """
    Mantém o estado do módulo LLVM-IR durante a geração de código.
    """

    def __init__(self):
        self.module = None
        self.builder = None
        self.funcao_atual = None
        self.globais = {}
        self.locais = {}
        self.funcoes = {}
        self.symbol_table = None

    def setup(self, module_name: str, symbol_table=None):
        """
        Inicializa o módulo LLVM e as configurações básicas de alvo (target).

        TODO (alunos): criar o ir.Module(name=module_name), configurar
        triple/data_layout (via llvmlite.binding) e declarar funções auxiliares
        de entrada/saída (leia/escreva), se necessário.
        """
        self.symbol_table = symbol_table
        self.globais = {}
        self.locais = {}
        self.funcoes = {}

    def salvar(self, output_path: str):
        """
        Grava o código LLVM-IR gerado no arquivo de saída (ex.: '<arquivo>.tpp.ll').

        TODO (alunos): verificar/validar o módulo e gravar str(self.module) em output_path.
        """
        if self.module is not None:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(str(self.module))
