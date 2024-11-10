from typing import Type
from arvore_abstrata import Declaracoes, Exsp, ExpNum, ComandoRepita, ComandoSe, ComandoEnquanto, InterfaceComando, ConverterReal
from rply import Token, token
import string
def descer_exp(treenode, lista_simbolos):
    if treenode is None:
            return False
    if isinstance(treenode, ExpNum):
        valor = treenode.valor.value
        for sublista in lista_simbolos:
            if any(valor in elemento for elemento in sublista):
                if sublista[2] == "real":
                    return True
                else:
                    print(f'O valor "{valor}" está contido na sublista {sublista}, mas o primeiro elemento não é "real".')
                break
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
        print("concertar" , treenode.valor)
        for sublista in lista_simbolos:
            if any(valor in elemento for elemento in sublista):
                if sublista[2] == "inteiro":
                    if treenode.valor.value.isdigit():
                        if treenode.tipo != "converter_real":
                            new_node = ExpNum(float(treenode.valor.value))
                            treenode.filhos = [new_node]
                        treenode.valor = "converter_real"
                        treenode.tipo = "converter_real"
                        print("foi")
                    else:
                        for sublista in lista_simbolos:
                            if len(sublista) > 1 and sublista[1] == treenode.valor.value:
                                sublista[2] = 'real'
                                lista_simbolos.remove(sublista)
                                novo_elemento = sublista  
                                lista_simbolos.append(novo_elemento)
                                print("affs")
                        if treenode.tipo != "converter_real":
                            new_node = ExpNum(treenode.valor.value)
                            treenode.filhos = [new_node]
                        treenode.valor = "converter_real"
                        treenode.tipo = "converter_real"
                        print("foi2")
                else:
                    pass
                break
    try:
        for filho in treenode.filhos:
            concertar_exp(filho, lista_simbolos)
    except AttributeError:
            pass

class Semantic():

    def __init__(self, treeRoot) -> None:
        self.lista_de_simbolos = []
        self.treeRoot = treeRoot

    def ajustar_arvore (self,treeRoot, nivel = 0):
        if treeRoot is None:
            return
        real = None
        if(isinstance(treeRoot,InterfaceComando )):
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