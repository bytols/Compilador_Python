from typing import Type
from arvore_abstrata import Programa, DeclaracaoVariaveis, SeqComando

# função que printa a arvore sintática
#recebe a raiz da arvore, um nivel, e o nome do arquivo em que ela ira escrever a arvore
def print_tree(treeRoot, nivel = 0, file:str = "results.txt") -> None:
    # abri o arquivo txt em que a arvore será escrito
    with open("results.txt" , "a") as file:

        # caso a raiz seja vazia
        if treeRoot is None:
            return
        try:
            #prita o atributo valor do nó atual, precedido de espaço baseado no nivel hierarquico da arvore
            file.write("  " * nivel + str(treeRoot.valor) + "\n")
            # o flush é para o write não ficar preso no buffer e printar direto
            file.flush() 
            # printa também no terminal..
            print("  " * nivel + str(treeRoot.valor))
            # mesma lógica do de cima, mas caso falhe printa a representação do objeto...
        except:
            file.write("  " * nivel + str(treeRoot) + "\n")
            file.flush() 
            print("  " * nivel + str(treeRoot))

        # aqui acontece a recursão que fica rechamando a mesma função para os filhos e irmãos dos nós, mas aumentato o nivel hierárquico
        try:
            for filho in treeRoot.filhos:
                print_tree(filho, nivel + 1)
        except AttributeError:
            pass

        try:
            for irmao in treeRoot.irmaos:
                print_tree(irmao , nivel)
        except :
            pass



