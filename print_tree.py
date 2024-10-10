from typing import Type
from arvore_abstrata import Programa, DeclaracaoVariaveis, SeqComando





def print_tree(treeRoot, nivel = 0, file:str = "results.txt") -> None:
    with open("results.txt" , "w") as file:
        if treeRoot is None:
            return
        try:
            file.write("  " * nivel + str(treeRoot.valor)) 
            print("  " * nivel + str(treeRoot.valor))
        except:
            file.write("  " * nivel + str(treeRoot))
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



