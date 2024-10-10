from lexer import Lexer
from parser_1 import Parser
from print_tree import print_tree

lex = Lexer()
pars = Parser()
lex.add_lexems()
tokens = lex.lexer("texto.txt")
pars.parse()
syntax = pars.get_parser()
tree = syntax.parse(tokens)
open("results.txt" , 'w').close()
print_tree(tree)



