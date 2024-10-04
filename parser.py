from rply import ParserGenerator

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

@pg.production('expression : ')





parser = pg.build()







