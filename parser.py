from rply import ParserGenerator
from arvore_abstrata import Programa
from lexer import Lexer

lex = Lexer()
lex.add_lexems()

pg = ParserGenerator(
    ['INTEIRO','REAL','SE','ENTAO','SENAO','ENQUANTO','REPITA','ATE','LER','MOSTRAR','MAIS','MENOS',
     'VEZES','DIVISAO','E','OU','MENOR','MENORIGUAL', 'MAIOR', 'MAIORIGUAL', 'IGUAL','DIFERENTE','ATRIBUICAO','DIGITO',
     'NUMERO','NUMERO_REAL','LETRA','ID','NEWLINE','PONTOVIRGULA','ABREPARENTESES','FECHAPARENTESES','ABRECH', 'FECHACH'],
     
     precedence=[
        ('left', ['OU']),
        ('left', ['E']),
        ('left', ['MENOR','MAIOR','MENORIGUAL','MAIORIGUAL','IGUAL','DIFERENTE']),
        ('left', ['MAIS' , 'MENOS']),
        ('left', ['VEZES', 'DIVISAO']),        
     ])




@pg.production('programa : DIGITO')
def program(p):
   print("aqui aqui eu" , p[0])
   return program(p[0])





parser = pg.build()
parser.parse(lex.lexer("texto.txt")).eval()







