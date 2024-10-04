from rply import LexerGenerator

newline = 0
lg = LexerGenerator()

lg.add('DIGITO' , r'[0-9]' )
lg.add('NUMERO' , r'[0-9]+' )
lg.add('NUMERO_REAL' , r'[0-9]\.[0-9]+')
lg.add('LETRA' , r'[a-zA-Z]')
lg.add('ID' , r'[a-zA-Z]+|[a-zA-Z]+[a-zA-Z][a-zA-Z\w]+' )
lg.add('NEWLINE' , r'\n' )
lg.add('INTEIRO' , r'inteiro' )
lg.add('REAL' , r'real' )
lg.add('SE' , r'se' )
lg.add('ENTAO' , r'entao' )
lg.add('SENAO' , r'senao' )
lg.add('ENQUANTO' , r'enquanto' )
lg.add('REPITA' , r'repita' )
lg.add('ATE' , r'ate' )
lg.add('LER' , r'ler' )
lg.add('MOSTRAR' , r'mostrar' )
lg.add('MAIS' , r'\+' )
lg.add('MENOS' , r'-' )
lg.add('VEZES' , r'\*' )
lg.add('DIVISAO' , r'/' )
lg.add('E' , r'&&' )
lg.add('OU' , r'||' )
lg.add('MENOR' , r'<' )
lg.add('MAIOR' , r'>' )
lg.add('MENORIGUAL' , r'<=' )
lg.add('MAIORIGUAL' , r'>=' )
lg.add('IGUAL' , r'==' )
lg.add('DIFERENTE' , r'!=' )
lg.add('ATRIBUICAO' , r'=' )
lg.add('PONTOVIRGULA' , r';' )
lg.add('ABREPARENTESES' , r'\(' )
lg.add('FECHAPARENTESES' , r'\)' )
lg.add('ABRECH' , r'{' )
lg.add('FECHACH' , r'}' )

lg.ignore(r'[\t]+')

l = lg.build()
#for token in l.lex('1+1+1'):
#    print(token)

with open("texto.txt") as file:
    arquivo = file.read()
    print(arquivo)

for token in l.lex(arquivo):
    print(token)
    if token.name == 'NEWLINE':
        newline += 1

print(newline)
        

