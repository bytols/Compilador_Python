from rply import ParserGenerator
from arvore_abstrata import Programa, DeclaracaoVariaveis , SeqComando,Declaracoes, ListaIdentificador, ComandoAtribuir, ComandoEnquanto, ComandoLer, ComandoMostrar, ComandoRepita,ComandoSe, Acao, ExpEOu, Exsp, ExpNum, ExpParenteses
from lexer import Lexer

lex = Lexer()
lex.add_lexems()

# classe que representa o parser (analisador sintático)
class Parser():

   def __init__(self):
      # definindo a tabela de simbolos!
      self.pg = ParserGenerator(
         ['INTEIRO','REAL','SE','ENTAO','SENAO','ENQUANTO','REPITA','ATE','LER','MOSTRAR','MAIS','MENOS',
         'VEZES','DIVISAO','E','OU','MENOR','MENORIGUAL', 'MAIOR', 'MAIORIGUAL', 'IGUAL','DIFERENTE','ATRIBUICAO','DIGITO', 'VIRGULA',
         'NUMERO','NUMERO_REAL','LETRA','ID','NEWLINE','PONTOVIRGULA','ABREPARENTESES','FECHAPARENTESES','ABRECH', 'FECHACH', 'SEPARADOR'],
         
         #definindo a precedência, a ordem de precedência é ascendente, e é lida pela esquerda
         precedence=[
            ('left', ['ABREPARENTESES']),
            ('left', ['OU']),
            ('left', ['E']),
            ('left', ['MENOR','MAIOR','MENORIGUAL','MAIORIGUAL','IGUAL','DIFERENTE']),
            ('left', ['VEZES', 'DIVISAO']),   
            ('left', ['MAIS' , 'MENOS']), 
         ])



   # aqui são definidas as regras de produção, que vieram da gramática
   def parse(self):

      # decorador que representa a gramática
      # toda função recebe um parametro p, que representa os valores a esquerda da regra de produção que podem ser um terminal ou um nó
      @self.pg.production('programa : declaracaoVariaveis seqComando')
      def programa(p):
         # o conceito é que eu retorno um nó, que sera usada para manter uma arvoré do proprio rply, que é a arvore que avalia a sintática
         
         # o no é representado por uma classe que sempre recebe seus não terminais de sua regra de produção
         programa = Programa(p[0] , p[1])
         #e seus nós não terminasi também são adicionaods ao nó pai como filhos e em outros caos irmão
         programa.filhos.append(p[0])
         programa.filhos.append(p[1])
         #retorno do nó
         return programa
      
      # podem ser declarados mais de um decorador , para várias regras de produção para um mesmo não terminal
      @self.pg.production('declaracaoVariaveis : declaracaoVariaveis declaracoes PONTOVIRGULA')
      @self.pg.production('declaracaoVariaveis : declaracoes PONTOVIRGULA')
      @self.pg.production('declaracaoVariaveis : ')
      def declaracaoVariaveis(p):
         if len(p) == 3:
            declaracaoVariaveis = p[0]
            declaracaoVariaveis.filhos.append(p[1])
            return(declaracaoVariaveis)
         elif len(p) == 2:
            declaracaoVariaveis = DeclaracaoVariaveis(p[0])
            declaracaoVariaveis.filhos.append(p[0])
            return(declaracaoVariaveis)
         else:
            declaracaoVariaveis = DeclaracaoVariaveis(p)
            return(declaracaoVariaveis)

      # o resto do código segue a mesma lógica apartir daqui!
      @self.pg.production('declaracoes : INTEIRO declaracoes listaIdentificador')
      @self.pg.production('declaracoes : REAL declaracoes listaIdentificador')
      @self.pg.production('declaracoes : INTEIRO listaIdentificador')
      @self.pg.production('declaracoes : REAL listaIdentificador')
      def declaracoes(p):
         if len(p) == 3:
            declaracoes = p[1]
            declaracoes.valor = (p[0])
            declaracoes.filhos.append(p[2])
            declaracoes.lineno = p[0].getsourcepos().lineno
            return(declaracoes) 
         else:
            declaracoes = Declaracoes(p[1])
            declaracoes.valor = (p[0])
            declaracoes.filhos.append(p[1])
            declaracoes.lineno = p[0].getsourcepos().lineno
            return(declaracoes)
      
      @self.pg.production('listaIdentificador : listaIdentificador VIRGULA ID')
      @self.pg.production('listaIdentificador : ID')
      def listaIdentificador(p):
         if len(p) == 3:
            listaIdentificador = p[0]
            listaIdentificador.irmaos.append(p[2])
            listaIdentificador.lineno = p[2].getsourcepos().lineno
            return (listaIdentificador)
         else:
            listaIdentificador = ListaIdentificador(p[0])
            if p[0] != None:
               listaIdentificador.valor = p[0]
               listaIdentificador.lineno = p[0].getsourcepos().lineno
            return(listaIdentificador)

      @self.pg.production('seqComando : seqComando comando')
      @self.pg.production('seqComando : comando')
      @self.pg.production('seqComando :')
      def seqComando(p):
         if len(p) == 2:
            seqComando = p[0]
            seqComando.filhos.append(p[1])
            return(seqComando)
         elif len(p) == 1:
            seqComando = SeqComando(p[0])
            seqComando.filhos.append(p[0])
            return(seqComando)
         else:
            seqComando = SeqComando(p)
            return(seqComando)
            
         
      @self.pg.production('comando : SE  exp  ENTAO acao SENAO acao')
      @self.pg.production('comando : SE ABREPARENTESES exp FECHAPARENTESES ENTAO acao SENAO acao')
      @self.pg.production('comando : SE  exp  ENTAO acao')
      @self.pg.production('comando : SE ABREPARENTESES exp FECHAPARENTESES ENTAO acao')
      @self.pg.production('comando : ENQUANTO ABREPARENTESES exp FECHAPARENTESES acao')
      @self.pg.production('comando : REPITA acao ATE exp ')
      @self.pg.production('comando : REPITA acao ATE ABREPARENTESES exp FECHAPARENTESES')
      @self.pg.production('comando : LER ABREPARENTESES ID FECHAPARENTESES PONTOVIRGULA')
      @self.pg.production('comando : MOSTRAR ABREPARENTESES ID FECHAPARENTESES PONTOVIRGULA')
      @self.pg.production('comando : ID ATRIBUICAO exp PONTOVIRGULA')
      def comando(p):
         if p[0].value == 'se':
            if p[1].valor == '(':
               if len(p) > 6:
                  seentaosenao = ComandoSe(p[2], p[4], p[6])
                  seentaosenao.filhos.append(p[2])
                  seentaosenao.filhos.append(p[4])
                  seentaosenao.filhos.append(p[6])
                  seentaosenao.lineno = p[0].getsourcepos().lineno
                  return(seentaosenao)
               else:
                  seentaosenao = ComandoSe(p[2], p[4])
                  seentaosenao.tipo = 'se-entao'
                  seentaosenao.valor = 'se-entao'
                  seentaosenao.filhos.append(p[2])
                  seentaosenao.filhos.append(p[4])
                  seentaosenao.lineno = p[0].getsourcepos().lineno
                  return(seentaosenao)
            else:
               if len(p) > 4:
                  seentaosenao = ComandoSe(p[1], p[3], p[5])
                  seentaosenao.filhos.append(p[1])
                  seentaosenao.filhos.append(p[3])
                  seentaosenao.filhos.append(p[5])
                  seentaosenao.lineno = p[0].getsourcepos().lineno
                  return(seentaosenao)
               else:
                  seentaosenao = ComandoSe(p[1], p[3])
                  seentaosenao.tipo = 'se-entao'
                  seentaosenao.valor = 'se-entao'
                  seentaosenao.filhos.append(p[1])
                  seentaosenao.filhos.append(p[3])
                  seentaosenao.lineno = p[0].getsourcepos().lineno
                  return(seentaosenao)
         elif p[0].value == 'enquanto':
            comandoEnquanto = ComandoEnquanto(p[2],p[4])
            comandoEnquanto.filhos.append(p[2])
            comandoEnquanto.filhos.append(p[4])
            comandoEnquanto.lineno = p[0].getsourcepos().lineno
            return(comandoEnquanto)
         elif p[0].value == 'repita':
            if p[3].value == '(':
               comandoRepita = ComandoRepita(p[1],p[4])
               comandoRepita.filhos.append(p[1])
               comandoRepita.filhos.append(p[4])
               comandoRepita.lineno = p[0].getsourcepos().lineno
               return(comandoRepita)
            else :
               comandoRepita = ComandoRepita(p[1],p[3])
               comandoRepita.filhos.append(p[1])
               comandoRepita.filhos.append(p[3])
               comandoRepita.lineno = p[0].getsourcepos().lineno
               return(comandoRepita)
         elif p[0].value == 'ler':
            comandoLer = ComandoLer(p[2])
            comandoLer.filhos.append(p[2])
            comandoLer.lineno = p[0].getsourcepos().lineno
            return(comandoLer)
         elif p[0].value == 'mostrar':
            comandoMostrar = ComandoMostrar(p[2])
            comandoMostrar.filhos.append(p[2])
            comandoMostrar.lineno = p[0].getsourcepos().lineno
            return(comandoMostrar)
         elif p[1].value == '=':
            comandoAtribuir = ComandoAtribuir(p[0], p[2])
            comandoAtribuir.filhos.append(p[0])
            #comandoAtribuir.filhos.append(p[1]) será que precisa?
            comandoAtribuir.filhos.append(p[2])
            comandoAtribuir.lineno = p[0].getsourcepos().lineno
            return(comandoAtribuir)
         
      @self.pg.production('acao : ABRECH seqComando FECHACH')
      @self.pg.production('acao : comando')
      def acao(p):
         if len(p) == 3:
            acao = p[1]
            return(acao)
         else:
            acao = Acao(p[0])
            acao.filhos.append(p[0])
            return(acao)
      
      # aqui a precedência é definida lá emcima no primeiro metodo
      @self.pg.production('exp : ABREPARENTESES exp FECHAPARENTESES')
      @self.pg.production('exp : DIGITO | NUMERO | NUMERO_REAL | ID')
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
         if len(p) == 3 and (isinstance(p[0], ExpNum) or isinstance(p[0], ExpEOu) or isinstance(p[0], Exsp )): 
            if p[1].name == 'OU' or p[1].name == 'E':
               exp = ExpEOu(p[0], p[2], p[1])
               exp.valor = p[1]
               exp.filhos.append(p[0])
               exp.filhos.append(p[2])
               exp.lineno = p[1].getsourcepos().lineno
               return(exp)
            else:
               exp = Exsp(p[0], p[2], p[1])
               exp.valor = p[1]
               exp.filhos.append(p[0])
               exp.filhos.append(p[2])
               exp.lineno = p[1].getsourcepos().lineno
               return(exp)
         else:
            if len(p) == 3:
               exp = ExpParenteses(p[1], p[0])
               exp.valor = p[0]
               exp.filhos.append(p[1])
               exp.lineno = p[0].getsourcepos().lineno
               return (exp)
            else:
               exp = ExpNum(p[0])
               exp.valor = p[0]
               exp.lineno = p[0].getsourcepos().lineno
               return(exp)

   # ultimo metodo para criar a arvore sintática!
   def get_parser(self):
      return self.pg.build()







