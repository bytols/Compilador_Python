from rply import ParserGenerator
from arvore_abstrata import Programa, DeclaracaoVariaveis , SeqComando,Declaracoes, Comando
from lexer import Lexer

lex = Lexer()
lex.add_lexems()

pg = ParserGenerator(
    ['INTEIRO','REAL','SE','ENTAO','SENAO','ENQUANTO','REPITA','ATE','LER','MOSTRAR','MAIS','MENOS',
     'VEZES','DIVISAO','E','OU','MENOR','MENORIGUAL', 'MAIOR', 'MAIORIGUAL', 'IGUAL','DIFERENTE','ATRIBUICAO','DIGITO',
     'NUMERO','NUMERO_REAL','LETRA','ID','NEWLINE','PONTOVIRGULA','ABREPARENTESES','FECHAPARENTESES','ABRECH', 'FECHACH', 'SEPARADOR'],
     
     precedence=[
        ('left', ['OU']),
        ('left', ['E']),
        ('left', ['MENOR','MAIOR','MENORIGUAL','MAIORIGUAL','IGUAL','DIFERENTE']),
        ('left', ['MAIS' , 'MENOS']),
        ('left', ['VEZES', 'DIVISAO']),        
     ])


#Arvore = Pro()

@pg.production('programa : declaracaoVariaveis seqComando')
def programa(p):
   print("aqui aqui eu" , p[0] , p [1])
   print(p[1].value)
   return Programa(p[0] , p[1])

@pg.production('declaracaoVariaveis : declaracaoVariaveis declaracoes PONTOVIRGULA')
@pg.production('declaracaoVariaveis : declaracoes PONTOVIRGULA')
def declaracaoVariaveis(p):
   if len(p) == 3:
      return(DeclaracaoVariaveis(p[1], p[0]))
   else:
      return(DeclaracaoVariaveis(p[0]))

@pg.production('seqComando : seqComando comando PONTOVIRGULA')
@pg.production('seqComando : comando PONTOVIRGULA ')
def seqComando(p):
   if len(p) == 3:
      print( p[0].eval())
      return(SeqComando(p[1], p[0], value=p[0].eval()))
   else:
      print( p[0].eval())
      return(SeqComando(p[0], value=p[0].eval()))

@pg.production('declaracoes : INTEIRO ID ATRIBUICAO NUMERO')
def declaracoes(p):
   print(f'declaracoes: {p[1]} + {p[3]} ')
   return(Declaracoes(p[1], p[3]))

@pg.production('comando : NUMERO MAIS NUMERO')
def comando(p):
   print(f'comando: {p[0]} + {p[2]}')
   return(Comando(p[0], p[2]))

parser = pg.build()
parser.parse(lex.lexer("texto.txt")).eval()







