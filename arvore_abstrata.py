from rply.token import BaseBox


class Programa(BaseBox):

    def __init__(self, declaracaoVariaveis,seqComando) -> None:
        self.declaracaoVariaveis = declaracaoVariaveis
        self.seqComando = seqComando
        self.tipo = 'Programa'
        self.valor = 'Programa'
        self.filhos = []
        self.irmaos = []

    def eval(self):
        return [self.declaracaoVariaveis , self.seqComando]
    
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

    def __init__(self, exp, acao, acao_else:None):
        self.exp = exp
        self.acao = acao
        self.acao_else = acao_else
        self.tipo = 'se-entao-senao'
        self.valor = "se-entao"
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
        self.valor = id
        self.filhos = []
        self.irmaos = []

    def eval(self):
        return([self.valor])

class ComandoMostrar(BaseBox):

    def __init__(self, id):
        self.tipo = 'Mostrar'
        self.valor = id
        self.filhos = []
        self.irmaos = []

    def eval(self):
        return([self.valor])

class ComandoAtribuir(BaseBox):

    def __init__(self, exp, id):
        self.exp = exp
        self.tipo = 'Atribuir'
        self.valor = id
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
    
class Exsp(BaseBox):

    def __init__(self, exp, id):
        self

class ExpEOu(BaseBox)
    
    def __init__(self, exp, id):
        self.exp-left
        self.exp-right
        tipo = 