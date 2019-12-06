from tag import Tag
from token1 import Token

class TS:
   '''
   Classe para a tabela de simbolos representada por um dicionario: {'chave' : 'valor'}
   '''
   def __init__(self):
      self.ts = {}

      self.ts['if'] = Token(Tag.KW_IF, 'if', 0, 0)
      self.ts['else'] = Token(Tag.KW_ELSE, 'else', 0, 0)
      self.ts['print'] = Token(Tag.KW_PRINT, 'print', 0, 0)
      self.ts['class'] = Token(Tag.KW_CLASS, 'class', 0, 0)
      self.ts['def'] = Token(Tag.KW_DEF, 'def', 0, 0)
      self.ts['defstatic'] = Token(Tag.KW_DEFSTATIC, 'defstatic', 0, 0)
      self.ts['bool'] = Token(Tag.KW_BOOL, 'bool', 0, 0)
      self.ts['integer'] = Token(Tag.KW_INTEGER, 'integer', 0, 0)
      self.ts['String'] = Token(Tag.KW_STRING, 'String', 0, 0)
      self.ts['double'] = Token(Tag.KW_DOUBLE, 'double', 0, 0)
      self.ts['void'] = Token(Tag.KW_VOID, 'void', 0, 0)
      self.ts['main'] = Token(Tag.KW_MAIN, 'main', 0, 0)
      self.ts['end'] = Token(Tag.KW_END, 'end', 0, 0)
      self.ts['write'] = Token(Tag.KW_WRITE, 'write', 0, 0)
      self.ts['or'] = Token(Tag.KW_OR, 'or', 0, 0)
      self.ts['and'] = Token(Tag.KW_AND, 'and', 0, 0)
      self.ts['true'] = Token(Tag.KW_TRUE, 'true', 0, 0)
      self.ts['false'] = Token(Tag.KW_FALSE, 'false', 0, 0)
      self.ts['return'] = Token(Tag.KW_RETURN, 'return', 0, 0)
      self.ts['.'] = Token(Tag.KW_PONTO, '.', 0, 0)

   def getToken(self, lexema):
      token = self.ts.get(lexema)
      return token

   def addToken(self, lexema, token):
      self.ts[lexema] = token

   def removeToken(self, lexema):
      self.ts.pop(lexema)
   
   def printTS(self):
      for k, t in (self.ts.items()):
         print(k, ":", t.toString())

   def setTipo(self, lexema, tipo):
      self.ts.get(lexema).setTipo(tipo)