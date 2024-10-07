from rply import ParserGenerator
from arvore_abstrata import Programa, DeclaracaoVariaveis , SeqComando,Declaracoes, Comando, ListaIdentificador, ComandoAtribuir, ComandoEnquanto, ComandoLer, ComandoMostrar, ComandoRepita,ComandoSe, Acao, ExpEOu, Exsp
from lexer import Lexer

lex = Lexer()
lex.add_lexems()

class Parser():

   def __init__(self):
      self.pg = ParserGenerator(
         ['INTEIRO','REAL','SE','ENTAO','SENAO','ENQUANTO','REPITA','ATE','LER','MOSTRAR','MAIS','MENOS',
         'VEZES','DIVISAO','E','OU','MENOR','MENORIGUAL', 'MAIOR', 'MAIORIGUAL', 'IGUAL','DIFERENTE','ATRIBUICAO','DIGITO', 'VIRGULA',
         'NUMERO','NUMERO_REAL','LETRA','ID','NEWLINE','PONTOVIRGULA','ABREPARENTESES','FECHAPARENTESES','ABRECH', 'FECHACH', 'SEPARADOR'],
         
         precedence=[
            ('left', ['OU']),
            ('left', ['E']),
            ('left', ['MENOR','MAIOR','MENORIGUAL','MAIORIGUAL','IGUAL','DIFERENTE']),
            ('left', ['MAIS' , 'MENOS']),
            ('left', ['VEZES', 'DIVISAO']),        
         ])



   def parse(self):
      @self.pg.production('programa : declaracaoVariaveis seqComando')
      def programa(p):
         programa = Programa(p[0] , p[1])
         programa.filhos.append(p[0])
         programa.filhos.append(p[1])
         print("AA",programa.filhos)
         return programa
      @self.pg.production('declaracaoVariaveis : declaracaoVariaveis declaracoes PONTOVIRGULA')
      @self.pg.production('declaracaoVariaveis : declaracoes PONTOVIRGULA')
      def declaracaoVariaveis(p):
         if len(p) == 3:
            declaracaoVariaveis = p[0]
            declaracaoVariaveis.filhos.append(p[1])
            return(declaracaoVariaveis)
         else:
            declaracaoVariaveis = DeclaracaoVariaveis(p[0])
            declaracaoVariaveis.filhos.append(p[0])
            return(declaracaoVariaveis)

      @self.pg.production('declaracoes : INTEIRO declaracoes listaIdentificador')
      @self.pg.production('declaracoes : REAL declaracoes listaIdentificador')
      @self.pg.production('declaracoes : INTEIRO listaIdentificador')
      @self.pg.production('declaracoes : REAL listaIdentificador')
      def declaracoes(p):
         if len(p) == 3:
            declaracoes = p[1]
            declaracoes.valor = (p[0])
            declaracoes.filhos.append(p[2])
            return(declaracoes) 
         else:
            declaracoes = Declaracoes(p[1])
            declaracoes.valor = (p[0])
            declaracoes.filhos.append(p[1])
            print("final da arvore2:",p)
            return(declaracoes)
      
      @self.pg.production('listaIdentificador : listaIdentificador VIRGULA ID')
      @self.pg.production('listaIdentificador : ID')
      def listaIdentificador(p):
         if len(p) == 3:
            listaIdentificador = p[0]
            listaIdentificador.irmaos.append(p[2])
            return (listaIdentificador)
         else:
            listaIdentificador = ListaIdentificador(p[0])
            if p[0] != None:
               listaIdentificador.valor = p[0]
            return(listaIdentificador)

      @self.pg.production('seqComando : seqComando comando')
      @self.pg.production('seqComando : comando')
      def seqComando(p):
         if len(p) == 2:
            seqComando = p[0]
            seqComando.filhos.append(p[1])
            return(seqComando)
         else:
            seqComando = SeqComando(p[0])
            seqComando.filhos.append(p[0])
            return(seqComando)
         
      @self.pg.production('comando : SE  exp  ENTAO acao | SE  exp  ENTAO acao SENAO acao')
      @self.pg.production('comando : ENQUANTO ABREPARENTESES exp FECHAPARENTESES acao')
      @self.pg.production('comando : REPITA exp ATE acao ')
      @self.pg.production('comando : LER ABREPARENTESES ID FECHAPARENTESES PONTOVIRGULA')
      @self.pg.production('comando : MOSTRAR ABREPARENTESES ID FECHAPARENTESES PONTOVIRGULA')
      @self.pg.production('comando : ID ATRIBUICAO exp PONTOVIRGULA')
      def comando(p):
         if p[0].value == 'se':
            if len(p) == 3:
               seentaosenao = ComandoSe(p[1], p[3], p[5])
               seentaosenao.filho.append(p[1])
               seentaosenao.filho.append(p[3])
               seentaosenao.filho.append(p[5])
               return(seentaosenao)
            else:
               seentaosenao = ComandoSe(p[1], p[3])
               seentaosenao.tipo = 'se-entao'
               seentaosenao.filho.append(p[1])
               seentaosenao.filho.append(p[3])
               return(seentaosenao)
         elif p[0].value == 'enquanto':
            comandoEnquanto = ComandoEnquanto(p[2],p[4])
            comandoEnquanto.filhos.append(p[2])
            comandoEnquanto.filhos.append(p[4])
            return(comandoEnquanto)
         elif p[0].value == 'repita':
            comandoRepita = ComandoRepita(p[1],p[3])
            comandoRepita.filhos.append(p[1])
            comandoRepita.filhos.append(p[3])
            return(comandoEnquanto)
         elif p[0].value == 'ler':
            comandoLer = ComandoLer(p[2])
            return(comandoLer)
         elif p[0].value == 'mostrar':
            comandoMostrar = ComandoMostrar(p[2])
            return(comandoMostrar)
         elif p[1].value == '=':
            comandoAtribuir = ComandoAtribuir(p[0], p[2])
            comandoAtribuir.filhos.append(p[2])
            return(comandoAtribuir)
         
      @self.pg.production('acao : ABREPARENTESES seqComando FECHAPARENTESES')
      @self.pg.production('acao : comando')
      def acao(p):
         if len(p) == 3:
            acao = p[0]
            return(acao)
         else:
            acao = Acao(p[0])
            acao.filhos.append(p[0])
            return(acao)
         
      @self.pg.production('exp : NUMERO MAIS NUMERO | DIGITO MAIS NUMERO | NUMERO MAIS DIGITO | DIGITO MAIS DIGITO')
      @self.pg.production('exp : NUMERO MENOS NUMERO | DIGITO MENOS NUMERO | NUMERO MENOS DIGITO | DIGITO MENOS DIGITO')
      @self.pg.production('exp : NUMERO VEZES NUMERO | DIGITO VEZES NUMERO | NUMERO VEZES DIGITO | DIGITO VEZES DIGITO')
      @self.pg.production('exp : NUMERO DIVISAO NUMERO | DIGITO DIVISAO NUMERO | NUMERO DIVISAO DIGITO | DIGITO DIVISAO DIGITO')
      @self.pg.production('exp : NUMERO MENOR NUMERO | DIGITO MENOR NUMERO | NUMERO MENOR DIGITO | DIGITO MENOR DIGITO')
      @self.pg.production('exp : NUMERO MENORIGUAL NUMERO | DIGITO MENORIGUAL NUMERO | NUMERO MENORIGUAL DIGITO | DIGITO MENORIGUAL DIGITO')
      @self.pg.production('exp : NUMERO MAIOR NUMERO | DIGITO MAIOR NUMERO | NUMERO MAIOR DIGITO | DIGITO MAIOR DIGITO')
      @self.pg.production('exp : NUMERO MAIORIGUAL NUMERO | DIGITO MAIORIGUAL NUMERO | NUMERO MAIORIGUAL DIGITO | DIGITO MAIORIGUAL DIGITO')
      @self.pg.production('exp : NUMERO IGUAL NUMERO | DIGITO IGUAL NUMERO | NUMERO IGUAL DIGITO | DIGITO IGUAL DIGITO')
      @self.pg.production('exp : NUMERO DIFERENTE NUMERO | DIGITO DIFERENTE NUMERO | NUMERO DIFERENTE DIGITO | DIGITO DIFERENTE DIGITO')
      @self.pg.production('exp : exp OU exp | exp OU exp | exp OU exp | exp OU exp')
      @self.pg.production('exp : exp E exp | exp E exp | exp E exp | exp E exp')
      def exp(p):
         if p[0].name == 'OU' or p[0].name == 'E':
            exp = ExpEOu(p[0], p[2], p[1])
            exp.valor = p[1]
            exp.filhos.append(p[0])
            exp.filhos.append(p[2])
            return(exp)
         else:
            exp = Exsp(p[0], p[2])
            exp.valor = p[1]
            return(exp)

   def get_parser(self):
      return self.pg.build()
   
   
   #parser.parse(lex.lexer("texto.txt")).eval()







