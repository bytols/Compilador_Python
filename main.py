from lexer import Lexer
from parser_1 import Parser
from print_tree import print_tree
from semantic_parser import Semantic

#lista de simbolos
lista_de_simbolos = []
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
#print_tree(tree)
semantic = Semantic(tree)
semantic.preencher_tabela(tree)
semantic.checkar_variavel_nao_declarada(tree)
semantic.checkar_expressao_booleana(tree)
semantic.ajustar_arvore(tree)
#acho que não tem como ser invalido, pois, a variavel já foi declarada e uma atribuição só pode receber uma exp que é somente numeros e ints
semantic.avaliar_atribuicao(tree)
semantic.verificar_mostrar(tree)
semantic.verificar_ler(tree)
print_tree(tree)
semantic.salvar_matriz_em_arquivo()
# a ultima parte seria sobre o ler e mostrar mas não tem como ser invalida as expressões se chegou até aqui...



