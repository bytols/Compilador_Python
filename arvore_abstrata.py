from rply.token import BaseBox


class Programa(BaseBox):

    def __init__(self, declaracaoVariaveis,seqComando, value=None) -> None:
        self.declaracaoVariaveis = declaracaoVariaveis
        self.seqComando = seqComando
        self.value = value
        self.child = [None] * 2

    def eval(self):
        return [self.declaracaoVariaveis , self.seqComando]
    
class DeclaracaoVariaveis(BaseBox):

    def __init__(self, declaracao, proxima_declaracao=None ) -> None:
        self.declaracao = declaracao
        self.proxima_declaracao = proxima_declaracao

    def eval(self):
        return[self.declaracao , self.proxima_declaracao]
class SeqComando(BaseBox):

    def __init__(self, comando, seqComando=None, value=None) -> None:
        self.comando = comando
        self.seqComando = seqComando
        self.value = value

    def eval(self):
        return[self.comando , self.seqComando]
    
class Declaracoes(BaseBox):

    def __init__(self, identificador , numero ):
        self.identificador = identificador
        self.numero = numero

    def eval(self):
        return(print(f"inteiro {self.identificador} = {self.numero} ;"))
class Comando(BaseBox):

    def __init__(self, left, right ):
        self.left = left
        self.right = right

    def eval(self):
        return(int(self.left.value) + int(self.right.value))