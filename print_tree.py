from typing import Type
from arvore_abstrata import Programa, DeclaracaoVariaveis, SeqComando


#printar o value, adicionar um self.value em todos os nós!
def print_node(treenode):
    if treenode.__class__ == Programa:
        print(treenode.declaracaoVariaveis, end="  ")
        print(treenode.seqComando, end="  ")
        return True
    if treenode.__class__ == DeclaracaoVariaveis:
        print(treenode.declaracao, end="  ")
        return True
    if treenode.__class__ == SeqComando:
        print(treenode.comando, end="  ")



def print_tree(treeRoot, nivel = 0):
    if treeRoot is None:
        return
    try:
        print("  " * nivel + str(treeRoot.valor)) 
    except:
        print("  " * nivel + str(treeRoot))

    try:
        for filho in treeRoot.filhos:
            print_tree(filho, nivel + 1)
    except:
        pass

    try:
        for irmao in treeRoot.irmaos:
            print_tree(irmao , nivel)
    except:
        pass



