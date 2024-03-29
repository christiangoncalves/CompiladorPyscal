import sys
from ts import TS
from tag import Tag
from token1 import Token

class Lexer():
   '''
   Classe que representa o Lexer:
   
   [1] Voce devera se preocupar quando incremetar as linhas e colunas,
   assim como quando decrementar ou reinicia-las. Lembre-se, ambas 
   comecam em 1.
   [2] Toda vez que voce encontrar um lexema completo, voce deve retornar
   um objeto Token(Tag, "lexema", linha, coluna). Cuidado com as
   palavras reservadas, que ja sao cadastradas na TS. Essa consulta
   voce devera fazer somente quando encontrar um Identificador.
   [3] Se o caractere lido nao casar com nenhum caractere esperado,
   apresentar a mensagem de erro na linha e coluna correspondente.
   Obs.: lembre-se de usar o metodo retornaPonteiro() quando necessario. 
         lembre-se de usar o metodo sinalizaErroLexico() para mostrar
         a ocorrencia de um erro lexico.
   '''
   def __init__(self, input_file):
      try:
         self.input_file = open(input_file, 'rb')
         self.lookahead = 0
         self.n_line = 1
         self.n_column = 1
         self.ts = TS()
         
      except IOError:
         print('Erro de abertura do arquivo. Encerrando execução!')
         sys.exit(0)

   def closeFile(self):
      try:
         self.input_file.close()
      except IOError:
         print('Erro dao fechar arquivo. Encerrando execução!')
         sys.exit(0)

   def sinalizaErroLexico(self, message):
      print("\n[Erro Lexico]: ", message, "\n")

   def retornaPonteiro(self):
      if(self.lookahead.decode('ascii') != ''):
         self.input_file.seek(self.input_file.tell()-1)
         self.n_column-=1

   def printTS(self):
      self.ts.printTS()

   def proxToken(self, last_token):
      estado = 1
      lexema = ""
      c = '\u0000'
      token = None
      
      while(True):
         self.lookahead = self.input_file.read(1)
         c = self.lookahead.decode('ascii')

         #Contando Linhas e Colunas
         if(c == '\n'):
            self.n_line += 1
            self.n_column = 1
         elif (c == '\t'):
            self.n_column += 4
         else:
            self.n_column += 1
         
         if(estado == 1):
            if(c == ''):
               self.ts.addToken("EOF", Token(Tag.EOF, "EOF", self.n_line, self.n_column))
               token = Token(Tag.EOF, "EOF", self.n_line, self.n_column)
            elif(c == ' ' or c == '\t' or c == '\n' or c == '\r'):
               estado = 1
            elif(c == '='):
               estado = 2
            elif(c == '!'):
               estado = 4
            elif(c == '<'):
               estado = 6
            elif(c == '>'):
               estado = 9
            elif(c.isdigit()):
               lexema += c
               estado = 12
            elif(c.isalpha()):
               lexema += c
               estado = 14
            elif(c == '\"'):
               estado = 27
            elif(c == '#'):
               estado = 18
            elif(c == '.'):
               #estado = 16
               #self.ts.addToken(".", Token(Tag.KW_PONTO, ".", self.n_line, self.n_column))
               token = Token(Tag.KW_PONTO, ".", self.n_line, self.n_column)
            elif(c == '/'):
               #estado = 16
               #self.ts.addToken("/", Token(Tag.OP_DIVISAO, "/", self.n_line, self.n_column))
               token = Token(Tag.OP_DIVISAO, "/", self.n_line, self.n_column)
            elif (c == ','):
               #estado = 17
               #self.ts.addToken(",", Token(Tag.VG, ",", self.n_line, self.n_column))
               token = Token(Tag.VG, ",", self.n_line, self.n_column)
            elif (c == '*'):
               #estado = 19
               #self.ts.addToken("*", Token(Tag.OP_MULTIPLICACAO, "*", self.n_line, self.n_column))
               token = Token(Tag.OP_MULTIPLICACAO, "*", self.n_line, self.n_column)
            elif (c == '+'):
               #estado = 20
               #self.ts.addToken("+", Token(Tag.OP_SOMA, "+", self.n_line, self.n_column))
               token = Token(Tag.OP_SOMA, "+", self.n_line, self.n_column)
            elif (c == '-'):
               #estado = 21
                  if(last_token.nome != Tag.KW_INTEGER and last_token.nome != Tag.KW_DOUBLE and last_token.nome != Tag.ID):
                     token = Token(Tag.OP_INVERSOR, "-", self.n_line, self.n_column)
                  #self.ts.addToken("-", Token(Tag.OP_SUBTRACAO, "-", self.n_line, self.n_column))
                  else:
                     token = Token(Tag.OP_SUBTRACAO, "-", self.n_line, self.n_column)
            elif (c == '('):
               #estado = 22
               #self.ts.addToken("(", Token(Tag.AP, "(", self.n_line, self.n_column))
               token = Token(Tag.AP, "(", self.n_line, self.n_column)
            elif (c == ')'):
               #estado = 23
               #self.ts.addToken(")", Token(Tag.FP, ")", self.n_line, self.n_column))
               token = Token(Tag.FP, ")", self.n_line, self.n_column)
            elif (c == '['):
               #estado = 24
               #self.ts.addToken("[", Token(Tag.AT, "[", self.n_line, self.n_column))
               token = Token(Tag.AT, "[", self.n_line, self.n_column)
            elif (c == ':'):
               #estado = 25
               #self.ts.addToken(":", Token(Tag.DP, ":", self.n_line, self.n_column))
               token = Token(Tag.DP, ":", self.n_line, self.n_column)
            elif (c == ']'):
               #estado = 26
               #self.ts.addToken("]", Token(Tag.FT, "]", self.n_line, self.n_column))
               token = Token(Tag.FT, "]", self.n_line, self.n_column)
            elif (c == ';'):
               #estado = 28
               #self.ts.addToken(";", Token(Tag.PV, ";", self.n_line, self.n_column))
               token = Token(Tag.PV, ";", self.n_line, self.n_column)
            else:
               self.sinalizaErroLexico("Caractere invalido [" + c + "] na linha " +
               str(self.n_line) + " e coluna " + str(self.n_column))
               token = None
         elif(estado == 2):
            if(c == '='):
               #estado = 3
               #self.ts.addToken("==", Token(Tag.OP_IGUAL, "==", self.n_line, self.n_column))
               token = Token(Tag.OP_IGUAL, "==", self.n_line, self.n_column)
            else:
               #estado = 34
               self.retornaPonteiro()
               #self.ts.addToken("=", Token(Tag.CP, "=", self.n_line, self.n_column))
               token = Token(Tag.CP, "=", self.n_line, self.n_column)
         elif(estado == 4):
            if(c == '='):
               #estado = 5
               #self.ts.addToken("!=", Token(Tag.OP_DIFERENTE, "!=", self.n_line, self.n_column))
               token = Token(Tag.OP_DIFERENTE, "!=", self.n_line, self.n_column)
            else:
               #estado = 29
               self.retornaPonteiro()
               #self.ts.addToken("!", Token(Tag.OP_NEGACAO, "!", self.n_line, self.n_column))
               token = Token(Tag.OP_NEGACAO, "!", self.n_line, self.n_column)
         elif(estado == 6):
            if(c == '='):
               #estado = 7
               #self.ts.addToken("<=", Token(Tag.OP_MENOR_IGUAL, "<=", self.n_line, self.n_column))
               token = Token(Tag.OP_MENOR_IGUAL, "<=", self.n_line, self.n_column)
            else:
               #estado = 8
               self.retornaPonteiro()
               #self.ts.addToken("<", Token(Tag.OP_MENOR, "<", self.n_line, self.n_column))
               token = Token(Tag.OP_MENOR, "<", self.n_line, self.n_column)
         elif(estado == 9):
            if(c == '='):
               #estado = 10
               #self.ts.addToken(">=", Token(Tag.OP_MAIOR_IGUAL, ">=", self.n_line, self.n_column))
               token = Token(Tag.OP_MAIOR_IGUAL, ">=", self.n_line, self.n_column)
            else:
               #estado = 11
               self.retornaPonteiro()
               #self.ts.addToken(">", Token(Tag.OP_MAIOR, ">", self.n_line, self.n_column))
               token = Token(Tag.OP_MAIOR, ">", self.n_line, self.n_column)
         elif(estado == 12):
            if(c.isdigit()):
               #continua no estado 12 (estado = 12)
               lexema += c           
            elif(c == '.'):
               estado = 31
               lexema += c
            else:
               #estado = 13
               self.retornaPonteiro()
               #self.ts.addToken(lexema, Token(Tag.KW_INTEGER, lexema, self.n_line, self.n_column ))
               token = Token(Tag.KW_INTEGER, lexema, self.n_line, self.n_column )
         elif(estado == 14):
            if(c.isalnum() or c == '_'):
               #continua no estado 14
               lexema += c
            else:
               #estado = 15
               self.retornaPonteiro()
               tokenComp = self.ts.getToken(lexema)        
               if(tokenComp is None):
                  tokenComp = Token(Tag.ID, lexema, self.n_line, self.n_column )
                  self.ts.addToken(lexema, tokenComp)
               else:
                  tokenComp = Token(self.ts.getToken(lexema).nome, lexema, self.n_line, self.n_column )
               token = tokenComp
         elif(estado == 18):
            if(c != '\n'):
               estado = 18 
            else:
               estado = 1
         elif(estado == 27):
            if(c != '\"'):
               estado = 30
               lexema += c
            elif(c == '\"'):
               self.sinalizaErroLexico("String vazia na linha " +
               str(self.n_line) + " e coluna " + str(self.n_column))
               #self.ts.addToken(lexema, Token(Tag.KW_STRING, lexema, self.n_line, self.n_column  ))
               estado = 1
               token = None
            else:
               self.sinalizaErroLexico("Caractere invalido [" + c + "] na linha " +
               str(self.n_line) + " e coluna " + str(self.n_column))
               token = None
         elif(estado == 30): 
            if(c == ''):
               self.sinalizaErroLexico("String não finalizada corretamente na linha " +
               str(self.n_line) + " e coluna " + str(self.n_column) +". Finalizando compilação.")
               token = None
               estado = 1
            elif(c != '\"'):
               #estado permanece no 30 (estado = 30)
               lexema += c
            elif(c == '\"' ):
               #estado = 35
               #self.ts.addToken(lexema, Token(Tag.KW_STRING, lexema, self.n_line, self.n_column  ))
               token = Token(Tag.KW_STRING, lexema, self.n_line, self.n_column )
            else:
               self.sinalizaErroLexico("Caractere invalido [" + c + "] na linha " +
               str(self.n_line) + " e coluna " + str(self.n_column))
               token = None
         elif(estado == 31):
            if(c.isdigit()):
               estado = 32
               lexema +=c
            else:
               self.sinalizaErroLexico("Caractere invalido [" + c + "] na linha " +
               str(self.n_line) + " e coluna " + str(self.n_column))
               token = None
         elif(estado == 32):
            if(c.isdigit()):
               #estado permanece no 32 (estado = 32)
               lexema += c
            else:
               #estado = 33
               self.retornaPonteiro()
               #self.ts.addToken(lexema, Token(Tag.KW_DOUBLE, lexema, self.n_line, self.n_column ))
               token = Token(Tag.KW_DOUBLE, lexema, self.n_line, self.n_column )

         if (token is not None):

            return token
         # fim if's de estados
            
      # fim while
