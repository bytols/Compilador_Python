from lexer import Lexer
from parser_1 import Parser
from print_tree import print_tree

# defino o analisador léxico!
lex = Lexer()
# defino o analisador sintático!
pars = Parser()
#definindo os lexemas dentro do analisador léxico!
lex.add_lexems()
#enviando para o analisador léxico o código
tokens = lex.lexer("texto.txt")
# etapas necessárias para criação do analisador sintático
pars.parse()
syntax = pars.get_parser()
# enviando os tokens do léxico para o parser e atribuindo o nó raiz em tree
tree = syntax.parse(tokens)
# deleta o conteudo vigiente no results.txt
open("results.txt" , 'w').close()
# printa a arvore no texto...
print_tree(tree)



