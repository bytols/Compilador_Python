from rply.token import BaseBox
from abc import ABC, abstractmethod

class Interfaceexp(ABC):
    @abstractmethod
    def eval():
        raise NotImplementedError
    
class InterfaceComando(ABC):
    @abstractmethod
    def eval():
        raise NotImplementedError
    
# definindo as classes que representam os não termians que serão os nós das arvores
class Programa(BaseBox):

    #classe init qeu recebe seus não terminais , e as vezes seus não terminais case seja um id ou algo relevante...
    # também define seu tipo e valor, que representa o tipo de nó que é
    # também define as listas que receberão outros nós irmãos e filhos!
    def __init__(self, declaracaoVariaveis,seqComando) -> None:
        self.declaracaoVariaveis = declaracaoVariaveis
        self.seqComando = seqComando
        self.tipo = 'Programa'
        self.valor = 'Programa'
        self.filhos = []
        self.irmaos = []

    # função eval que retorna os não terminais da regra de produçaõ!
    def eval(self):
        return [self.declaracaoVariaveis , self.seqComando]
    
    # o resto da classe segue essa linha!
class DeclaracaoVariaveis(BaseBox):

    def __init__(self, declaracao, proxima_declaracao=None ) -> None:
        self.declaracao = declaracao
        self.proxima_declaracao = proxima_declaracao
        self.tipo = 'DeclaracaoVariaveis'
        self.valor = 'DeclaracaoVariaveis'
        self.filhos = []
        self.irmaos = []

    def eval(self):
        return[self.declaracao , self.proxima_declaracao]
class SeqComando(BaseBox):

    def __init__(self, comando, seqComando=None) -> None:
        self.comando = comando
        self.seqComando = seqComando
        self.tipo = 'SeqComando'
        self.valor = 'SeqComando'
        self.filhos = []
        self.irmaos = []

    def eval(self):
        return[self.comando , self.seqComando]
    
class Declaracoes(BaseBox):

    def __init__(self, declaracao , listaIdentificador = None, valor = None):
        self.declaracao = declaracao
        self.listaIdentificador = listaIdentificador
        self.tipo = 'Declaracoes'
        self.valor = valor
        self.filhos = []
        self.irmaos = []

    def eval(self):
        return([self.declaracao ,self.listaIdentificador])
    
class ListaIdentificador(BaseBox):
    
    def __init__(self, id, listaIdentificador = None) -> None:
        self.listaIdentificador = listaIdentificador
        self.id = id
        self.tipo = 'listaIdentificador'
        self.valor = id.value
        self.filhos = []
        self.irmaos = []

    def eval(self):
        return([self.listaIdentificador])

class ComandoSe(BaseBox):

    def __init__(self, exp, acao, acao_else =None):
        self.exp = exp
        self.acao = acao
        self.acao_else = acao_else
        self.tipo = 'se-entao-senao'
        self.valor = "se-entao-senao"
        self.filhos = []
        self.irmaos = []

    def eval(self):
        if self.acao_else:
            return([self.exp, self.acao, self.acao_else])
        else:
            return([self.exp, self.acao])

class ComandoEnquanto(BaseBox):

    def __init__(self, exp, acao):
        self.exp = exp
        self.acao = acao
        self.tipo = 'Enquanto'
        self.valor = 'Enquanto'
        self.filhos = []
        self.irmaos = []

    def eval(self):
        return([self.exp, self.acao])

class ComandoRepita(BaseBox):

    def __init__(self, exp, acao):
        self.exp = exp
        self.acao = acao
        self.tipo = 'Repita-Enquanto'
        self.valor = 'Repita-Enquanto'
        self.filhos = []
        self.irmaos = []

    def eval(self):
        return([self.exp, self.acao])

class ComandoLer(BaseBox):

    def __init__(self, id):
        self.tipo = 'Ler'
        self.valor = 'Ler'
        self.filhos = []
        self.irmaos = []

    def eval(self):
        return([self.valor])

class ComandoMostrar(BaseBox, InterfaceComando):

    def __init__(self, id):
        self.tipo = 'Mostrar'
        self.valor = 'Mostrar'
        self.filhos = []
        self.irmaos = []

    def eval(self):
        return([self.valor])

class ComandoAtribuir(BaseBox, InterfaceComando):

    def __init__(self, id, exp):
        self.exp = exp
        self.tipo = 'Atribuir'
        self.valor = 'Atribuir'
        self.filhos = []
        self.irmaos = []

    def eval(self):
        return([self.exp, self.valor])
    
class Acao(BaseBox):

    def __init__(self,comando):
        self.comando = comando
        self.tipo = 'Acao'
        self.valor = 'Acao'
        self.filhos = []
        self.irmaos = []

    def eval(self):
        return self.comando
    
class Exsp(BaseBox, Interfaceexp):

    def __init__(self, left, right, token):
        self.exp_left = left
        self.exp_right = right
        self.tipo = 'Exsp'
        self.valor = token
        self.filhos = []
        self.irmaos = []

    def eval(self):
        return [self.exp_left , self.exp_right] 

class ExpEOu(BaseBox, Interfaceexp):
    
    def __init__(self, left, right, token):
        self.exp_left = left
        self.exp_right = right
        self.tipo = 'ExpEOu'
        self.valor = token
        self.filhos = []
        self.irmaos = []

    def eval(self):
        return [self.exp_left , self.exp_right] 
    
class ExpParenteses(BaseBox, Interfaceexp):
    
    def __init__(self, exp ,token):
        self.exp = exp
        self.tipo = 'ExpParenteses'
        self.valor = token
        self.filhos = []
        self.irmaos = []

    def eval(self):
        return self.exp 

class ExpNum(BaseBox, Interfaceexp):
    
    def __init__(self, token):
        self.token = token
        self.tipo = 'ExpNum'
        self.valor = token
        self.filhos = []
        self.irmaos = []

    def eval(self):
        return [self.exp_left , self.exp_right] 

class ConverterReal(BaseBox):

    def __init__(self, exp):
        self.exp = exp
        self.tipo = "converter_real"
        self.valor = "converter_real"
        self.filhos = []
        self.irmaos = []

    def eval(self):
        return self.exp 
    
class Converter_Ints(BaseBox):

    def __init__(self, exp):
        self.exp = exp
        self.tipo = "converter_int"
        self.valor = "converter_int"
        self.filhos = []
        self.irmaos = []

    def eval(self):
        return self.exp 