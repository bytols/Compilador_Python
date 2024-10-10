from rply import ParserGenerator
from arvore_abstrata import Programa, DeclaracaoVariaveis , SeqComando,Declaracoes, ListaIdentificador, ComandoAtribuir, ComandoEnquanto, ComandoLer, ComandoMostrar, ComandoRepita,ComandoSe, Acao, ExpEOu, Exsp, ExpNum
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
            ('left', ['MAIS' , 'MENOS']),
            ('left', ['VEZES', 'DIVISAO']),    
            ('left', ['MENOR','MAIOR','MENORIGUAL','MAIORIGUAL','IGUAL','DIFERENTE']),
            ('left', ['E']),
            ('left', ['OU']),
         ])



   def parse(self):
      @self.pg.production('programa : declaracaoVariaveis seqComando')
      def programa(p):
         programa = Programa(p[0] , p[1])
         programa.filhos.append(p[0])
         programa.filhos.append(p[1])
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
         
      @self.pg.production('comando : SE  exp  ENTAO acao SENAO acao')
      @self.pg.production('comando : SE  exp  ENTAO acao ')
      @self.pg.production('comando : ENQUANTO ABREPARENTESES exp FECHAPARENTESES acao')
      @self.pg.production('comando : REPITA acao ATE exp ')
      @self.pg.production('comando : LER ABREPARENTESES ID FECHAPARENTESES PONTOVIRGULA')
      @self.pg.production('comando : MOSTRAR ABREPARENTESES ID FECHAPARENTESES PONTOVIRGULA')
      @self.pg.production('comando : ID ATRIBUICAO exp PONTOVIRGULA')
      def comando(p):
         if p[0].value == 'se':
            if len(p) > 4:
               seentaosenao = ComandoSe(p[1], p[3], p[5])
               seentaosenao.filhos.append(p[1])
               seentaosenao.filhos.append(p[3])
               seentaosenao.filhos.append(p[5])
               return(seentaosenao)
            else:
               seentaosenao = ComandoSe(p[1], p[3])
               seentaosenao.tipo = 'se-entao'
               seentaosenao.valor = 'se-entao'
               seentaosenao.filhos.append(p[1])
               seentaosenao.filhos.append(p[3])
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
            return(comandoRepita)
         elif p[0].value == 'ler':
            comandoLer = ComandoLer(p[2])
            comandoLer.filhos.append(p[2])
            return(comandoLer)
         elif p[0].value == 'mostrar':
            comandoMostrar = ComandoMostrar(p[2])
            comandoMostrar.filhos.append(p[2])
            return(comandoMostrar)
         elif p[1].value == '=':
            comandoAtribuir = ComandoAtribuir(p[0], p[2])
            comandoAtribuir.filhos.append(p[0])
            #comandoAtribuir.filhos.append(p[1]) será que precisa?
            comandoAtribuir.filhos.append(p[2])
            return(comandoAtribuir)
         
      @self.pg.production('acao : ABRECH seqComando FECHACH')
      @self.pg.production('acao : comando')
      def acao(p):
         if len(p) == 3:
            acao = p[0]
            return(acao)
         else:
            acao = Acao(p[0])
            acao.filhos.append(p[0])
            return(acao)
      
      @self.pg.production('exp : DIGITO | NUMERO')
      @self.pg.production('exp : exp MAIS exp')
      @self.pg.production('exp : exp MENOS exp')
      @self.pg.production('exp : exp VEZES exp ')
      @self.pg.production('exp : exp DIVISAO exp')
      @self.pg.production('exp : exp MENOR exp')
      @self.pg.production('exp : exp MENORIGUAL exp')
      @self.pg.production('exp : exp MAIOR exp')
      @self.pg.production('exp : exp MAIORIGUAL exp')
      @self.pg.production('exp : exp IGUAL exp ')
      @self.pg.production('exp : exp DIFERENTE exp')
      @self.pg.production('exp : exp OU exp ')
      @self.pg.production('exp : exp E exp')
      def exp(p):
         if len(p) > 1:
            if p[1].name == 'OU' or p[1].name == 'E':
               exp = ExpEOu(p[0], p[2], p[1])
               exp.valor = p[1]
               exp.filhos.append(p[0])
               exp.filhos.append(p[2])
               return(exp)
            else:
               exp = Exsp(p[0], p[2], p[1])
               exp.valor = p[1]
               exp.filhos.append(p[0])
               exp.filhos.append(p[2])
               return(exp)
         else:
            exp = ExpNum(p[0])
            exp.valor = p[0]
            return(exp)

   def get_parser(self):
      return self.pg.build()
   
   
   #parser.parse(lex.lexer("texto.txt")).eval()







