from typing import Type
from arvore_abstrata import Declaracoes, Exsp, ExpNum, ComandoRepita, ComandoSe, ComandoEnquanto, InterfaceComando, ConverterReal, ComandoAtribuir
from rply import Token, token
import string

def verificar_elemento(lista_simbolos, valor, tipo):
    for sublista in lista_simbolos:
        if len(sublista) > 2 and valor == sublista[1] and sublista[2] == tipo:
            return True 
    return False

def descer_exp(treenode, lista_simbolos):
    if treenode is None:
            return False
    if isinstance(treenode, ExpNum):
        valor = treenode.valor.value
        if verificar_elemento(lista_simbolos=lista_simbolos, valor=valor , tipo="real"):
            return True
        else:
            pass
            #print(f'O valor "{valor}" está contido na sublista, mas o primeiro elemento não é "real".')

    try:
        for filho in treenode.filhos:
            if descer_exp(filho, lista_simbolos):  # Propaga o True encontrado
                return True
    except AttributeError:
        pass
    return False

def concertar_exp(treenode, lista_simbolos):
    if treenode is None:
            return False
    if isinstance(treenode, ExpNum):
        valor = treenode.valor.value
        if treenode.valor.value.isdigit():
            if treenode.tipo != "converter_real":
                new_node = ExpNum(float(treenode.valor.value))
                treenode.filhos = [new_node]
            treenode.valor = "converter_real"
            treenode.tipo = "converter_real"
        if verificar_elemento(lista_simbolos, valor, "inteiro"):
            if treenode.tipo != "converter_real":
                new_node = ExpNum(treenode.valor.value)
                treenode.filhos = [new_node]
            treenode.valor = "converter_real"
            treenode.tipo = "converter_real"
    try:
        for filho in treenode.filhos:
            concertar_exp(filho, lista_simbolos)
    except AttributeError:
            pass

class Semantic():

    def __init__(self, treeRoot) -> None:
        self.lista_de_simbolos = []
        self.treeRoot = treeRoot

    def avaliar_atribuicao(self,treeRoot, nivel = 0):    
        if treeRoot is None:
            return
        if(isinstance(treeRoot, ComandoAtribuir)):
            temp_root = treeRoot
            valor = temp_root.filhos[0]
            tipo = verificar_elemento(lista_simbolos=self.lista_de_simbolos , valor=valor.value , tipo="real")
            if tipo: 
                if treeRoot.filhos[1].tipo != "CONVERTER_REAL_RESULTADO":
                    print(f"{valor.value} é real")
                    new_node = ExpNum("CONVERTER_REAL_RESULTADO")
                    next_node = [treeRoot.filhos[1]]
                    new_node.filhos = next_node
                    treeRoot.filhos[1] = new_node
                    print("foi!")
            else:
                if treeRoot.filhos[1].tipo != "CONVERTER_INTEIRO_RESULTADO":
                    print(f"{valor.value} é inteiro")
                    new_node = ExpNum("CONVERTER_INTEIRO_RESULTADO")
                    next_node = [treeRoot.filhos[1]]
                    new_node.filhos = next_node
                    treeRoot.filhos[1] = new_node
                    print("foi!")

        try:
            for filho in treeRoot.filhos:
                self.avaliar_atribuicao(filho, nivel + 1)
        except AttributeError:
            pass
        try:
            for irmao in treeRoot.irmaos:
                self.avaliar_atribuicao(irmao , nivel)
        except :
            pass       

    def ajustar_arvore (self,treeRoot, nivel = 0):
        if treeRoot is None:
            return
        real = None
        if(isinstance(treeRoot, InterfaceComando)):
            temp_root = treeRoot
            real = descer_exp(temp_root, self.lista_de_simbolos)
        if  real:
            concertar_exp(temp_root, self.lista_de_simbolos)

        try:
            for filho in treeRoot.filhos:
                self.ajustar_arvore(filho, nivel + 1)
        except AttributeError:
            pass
        try:
            for irmao in treeRoot.irmaos:
                self.ajustar_arvore(irmao , nivel)
        except :
            pass       

    def checkar_expressao_booleana(self,treeRoot, nivel = 0):
        if treeRoot is None:
            return
        if isinstance(treeRoot, ComandoEnquanto) or isinstance(treeRoot, ComandoSe):
            if isinstance(treeRoot.filhos[0], Exsp) and treeRoot.filhos[0].valor.value not in {'>', '<', '>=', '<=', '==', '!='}:
                raise ValueError(f'a exp de {treeRoot.tipo}, não é booleano')
        if isinstance(treeRoot, ComandoRepita):
            if isinstance(treeRoot.filhos[1], Exsp) and treeRoot.filhos[1].valor.value not in {'>', '<', '>=', '<=', '==', '!='}:
                raise ValueError(f'a exp de {treeRoot.tipo}, não é booleano')
        try:
            for filho in treeRoot.filhos:
                self.checkar_expressao_booleana(filho, nivel + 1)
        except AttributeError:
            pass
        try:
            for irmao in treeRoot.irmaos:
                self.checkar_expressao_booleana(irmao , nivel)
        except :
            pass       

    def checkar_variavel_nao_declarada(self,treeRoot, nivel = 0):
        if treeRoot is None:
            return
        if isinstance(treeRoot, token.Token):
            if treeRoot.value not in [s for sublist in self.lista_de_simbolos for s in sublist]:
                raise ValueError(f"{treeRoot.value} não foi declarada")
        if isinstance(treeRoot, ExpNum) and treeRoot.valor.name == 'ID':
            if treeRoot.valor.value not in [s for sublist in self.lista_de_simbolos for s in sublist]:
                raise ValueError(f"{treeRoot.valor.value} não foi declarada")
        try:
            for filho in treeRoot.filhos:
                self.checkar_variavel_nao_declarada(filho, nivel + 1)
        except AttributeError:
            pass
        try:
            for irmao in treeRoot.irmaos:
                self.checkar_variavel_nao_declarada(irmao , nivel)
        except:
            pass

    def preencher_tabela(self,treeRoot, nivel = 0):
            if treeRoot is None:
                return
            if isinstance(treeRoot, Declaracoes):
                endereco = treeRoot.valor.value
                for i in range(len(treeRoot.filhos)):
                    treeRoot = treeRoot.filhos[i]
                    elemento = []
                    elemento.append(hex(id(treeRoot)))
                    elemento.append(treeRoot.valor.value)
                    elemento.append(endereco)
                    for substring in self.lista_de_simbolos:
                        if treeRoot.valor.value in substring:
                            raise ValueError(treeRoot.valor, "essa variavel já foi utilizada")
                    self.lista_de_simbolos.append(elemento)
                    treeRootirmaos = treeRoot.irmaos
                    for j in range(len(treeRootirmaos)):
                        elemento = []
                        elemento.append(hex(id(treeRootirmaos[j])))
                        elemento.append(treeRootirmaos[j].value)
                        elemento.append(endereco)
                        for substring in self.lista_de_simbolos:
                            if treeRootirmaos[j].value in substring:
                                raise ValueError(treeRootirmaos[j].value, "essa variavel já foi utilizada")
                        self.lista_de_simbolos.append(elemento)
            try:
                for filho in treeRoot.filhos:
                    self.preencher_tabela(filho, nivel + 1)
            except AttributeError:
                pass

            try:
                for irmao in treeRoot.irmaos:
                    self.preencher_tabela(irmao , nivel)
            except :
                pass

    def outro(self, nivel = 0):
            if self.treeRoot is None:
                return
            try:
                for filho in self.treeRoot.filhos:
                    self.preencher_tabela(filho, nivel + 1)
            except AttributeError:
                pass

            try:
                for irmao in self.treeRoot.irmaos:
                    self.preencher_tabela(irmao , nivel)
            except :
                pass