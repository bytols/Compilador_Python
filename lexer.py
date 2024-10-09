from rply import LexerGenerator


class Lexer():

    def __init__(self) -> None:
        self.newline = 0
        self.lg = LexerGenerator()

    def add_lexems(self) -> None:

        self.lg.add('VIRGULA' , r'\,')
        self.lg.add('INTEIRO' , r'inteiro' )
        self.lg.add('REAL' , r'real' )
        self.lg.add('SENAO' , r'senao' )
        self.lg.add('SE' , r'se' )
        self.lg.add('ENTAO' , r'entao' )
        self.lg.add('ENQUANTO' , r'enquanto' )
        self.lg.add('REPITA' , r'repita' )
        self.lg.add('ATE' , r'ate' )
        self.lg.add('LER' , r'ler' )
        self.lg.add('MOSTRAR' , r'mostrar' )
        self.lg.add('SEPARADOR' , r'\$\$')
        self.lg.add('DIGITO' , r'\b[0-9]\b' )
        self.lg.add('NUMERO' , r'[0-9]+' )
        self.lg.add('NUMERO_REAL' , r'[0-9]\.[0-9]+')
        self.lg.add('LETRA' , r'\b[a-zA-Z]\b')
        self.lg.add('ID' , r'[a-zA-Z]+|[a-zA-Z]+[a-zA-Z][a-zA-Z\w]+' )
        self.lg.add('NEWLINE' , r'\n' )
        self.lg.add('MAIS' , r'\+' )
        self.lg.add('MENOS' , r'-' )
        self.lg.add('VEZES' , r'\*' )
        self.lg.add('DIVISAO' , r'/' )
        self.lg.add('E' , r'&&' )
        self.lg.add('OU' , r'\|\|' )
        self.lg.add('MENOR' , r'<' )
        self.lg.add('MAIOR' , r'>' )
        self.lg.add('MENORIGUAL' , r'<=' )
        self.lg.add('MAIORIGUAL' , r'>=' )
        self.lg.add('IGUAL' , r'==' )
        self.lg.add('DIFERENTE' , r'!=' )
        self.lg.add('ATRIBUICAO' , r'=' )
        self.lg.add('PONTOVIRGULA' , r';' )
        self.lg.add('ABREPARENTESES' , r'\(' )
        self.lg.add('FECHAPARENTESES' , r'\)' )
        self.lg.add('ABRECH' , r'{' )
        self.lg.add('FECHACH' , r'}' )
        self.lg.ignore(r'\s+')

    def lexer(self, txt:str) -> None:

        l = self.lg.build()
        with open(txt) as file:
            arquivo = file.read()
            print(arquivo)
        for token in l.lex(arquivo):
            print(token)
            if token.name == 'NEWLINE':
                self.newline += 1
        print(self.newline)
        return(l.lex(arquivo))
        

