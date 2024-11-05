from typing import Type
from arvore_abstrata import Programa, DeclaracaoVariaveis, SeqComando, ListaIdentificador, Declaracoes, Interfaceexp, ExpNum
from rply import Token, token

class Semantic():

    def __init__(self, treeRoot) -> None:
        self.lista_de_simbolos = []
        self.treeRoot = treeRoot

    def checkar_variavel_nao_declarada(self,treeRoot, nivel = 0):
        if treeRoot is None:
            return
        if isinstance(treeRoot, token.Token):
            print("vamos?",treeRoot)
            if treeRoot.value not in [s for sublist in self.lista_de_simbolos for s in sublist]:
                raise ValueError(f"{treeRoot.value} não foi declarada")
        if isinstance(treeRoot, ExpNum) and treeRoot.valor.name == 'ID':
            print("vamos?",treeRoot)
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