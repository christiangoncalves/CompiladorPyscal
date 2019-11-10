from tag import Tag
from token1 import Token
from lexer import Lexer

if __name__ == "__main__":
   lexer = Lexer('teste2.pys')

   print("\n=>Lista de tokens:")
   token = lexer.proxToken(None)
   last_token = token
   while(token is not None and token.getNome() != Tag.EOF):
      print(token.toString(), "Linha: " + str(token.getLinha()) + " Coluna: " + str(token.getColuna()))
      token = lexer.proxToken(last_token)
      last_token = token

   print("\n=>Tabela de simbolos:")
   lexer.printTS()
   lexer.closeFile()
    
   print('\n=> Fim da compilacao')
