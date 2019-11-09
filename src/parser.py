import sys

from ts import TS
from tag import Tag
from token import Token
from lexer import Lexer

"""
 * *
 * [TODO]: tratar retorno 'None' do Lexer que esta sem Modo Panico
 *
 *
 * Modo Pânico do Parser: 
    * Para tomar a decisao de escolher uma das regras (quando mais de uma disponivel),
    * o parser usa incialmente o FIRST(), e para alguns casos, FOLLOW(). Essa informacao eh dada pela TP.
    * Caso nao existe a regra na TP que corresponda ao token da entrada,
    * informa-se uma mensagem de erro e inicia-se o Modo Panico:
    * [1] calcula-se o FOLLOW do NAO-TERMINAL (a esquerda) da regra atual: esse NAO-TERMINAL estara no topo da pilha;
    * [2] se o token da entrada estiver neste FOLLOW, desempilha-se o nao-terminal atual - metodo synch() - retorna da recursao;
    * [3] caso contrario, a entrada eh avancada para uma nova comparacao e mantem-se o nao-terminal no topo da pilha 
    * (se for a pilha recursiva, mantem o procedimento no topo da recursao) - metodo skip().
    * 
    * O Modo Panico encerra-se, 'automagicamente', quando um token esperado aparece.
    * Para NAO implementar o Modo Panico, basta sinalizar erro quando nao
    * for possivel utilizar alguma das regras. Em seguida, encerrar a execucao usando sys.exit(0).
"""
class Parser():
    def __init__(self, lexer):
      self.lexer = lexer
      self.token = lexer.proxToken() # Leitura inicial obrigatoria do primeiro simbolo

   def sinalizaErroSintatico(self, message):
      print("[Erro Sintatico] na linha " + str(self.token.getLinha()) + " e coluna " + str(self.token.getColuna()) + ": ")
      print(message, "\n")

   def advance(self):
      print("[DEBUG] token: ", self.token.toString())
      self.token = self.lexer.proxToken()
   
   def skip(self, message):
      self.sinalizaErroSintatico(message)
      self.advance()

    def eat(self, t):
        if (self.token.getNome() == t):
            self.advance()
            return True
        else:
            return False

    """
    LEMBRETE:
    Todas as decisoes do Parser, sao guiadas pela Tabela Preditiva (TP)
    """

    # Programa -> Classe EOF
    def Programa(self):
        self.Classe()
        if (self.token1.getNome() != Tag.EOF):
            self.sinalizaErroSintatico("Esperado \"EOF\"; encontrado " + "\""+ self.token.getLexema() + "\"")

    def Classe(self):
        # Classe -> "class" ID ":" ListaFuncao Main "end" "." 
        if (self.eat(Tag.KW_CLASS)):
            if (not self.eat(Tag.ID)):
                self.sinalizaErroSintatico("Esperado \"ID\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            
            if (not self.eat(Tag.DP)):
                self.sinalizaErroSintatico("Esperado \":\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            
            self.ListaFuncao()
            self.Main()

            if (not self.eat(Tag.KW_END)):
                self.sinalizaErroSintatico("Esperado \"END\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            
            if (not self.eat(Tag.KW_PONTO)):
                self.sinalizaErroSintatico("Esperado \".\"; encontrado " + "\""+ self.token.getLexema() + "\"")
        else:
            self.sinalizaErroSintatico("Esperado \"class\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            
    def DeclaraID(self):
        # DeclaraID -> TipoPrimitivo ID ";"
        self.TipoPrimitivo()
        if (self.eat(Tag.ID)):
            if (not self.eat(Tag.DP)):
                self.sinalizaErroSintatico("Esperado \";\"; encontrado " + "\""+ self.token.getLexema() + "\"")
        else:
            self.sinalizaErroSintatico("Esperado \"ID\"; encontrado " + "\""+ self.token.getLexema() + "\"")
    
    def ListaFuncao(self):
        # ListaFuncao -> ListaFuncao’ 
        self.ListaFuncaoLinha()
    
    def ListaFuncaoLinha(self):
        # ListaFuncao’ → Funcao ListaFuncao’ | ε
        if (self.eat(Tag.KW_DEF)):
            Funcao()
            ListaFuncao()
        else:
            return
    
    def Funcao(self):
        # Funcao -> "def" TipoPrimitivo ID "(" ListaArg ")" ":" RegexDeclaraId ListaCmd Retorno "end" ";" 
        if (self.eat(Tag.KW_DEF)):
            TipoPrimitivo()
            if (not self.eat(Tag.ID)):
                self.sinalizaErroSintatico("Esperado \"ID\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            
            if (not self.eat(Tag.AP)):
                self.sinalizaErroSintatico("Esperado \"(\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            
            self.ListaArg()

            if (not self.eat(Tag.FP)):
                self.sinalizaErroSintatico("Esperado \")\"; encontrado " + "\""+ self.token.getLexema() + "\"")

            if (not self.eat(Tag.DP)):
                self.sinalizaErroSintatico("Esperado \":\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            
            self.RegexDeclaraId()
            self.ListaCmd()
            self.Retorno()

            if (not self.eat(Tag.KW_END)):
                self.sinalizaErroSintatico("Esperado \"end\"; encontrado " + "\""+ self.token.getLexema() + "\"")

            if (not self.eat(Tag.PV)):
                self.sinalizaErroSintatico("Esperado \";\"; encontrado " + "\""+ self.token.getLexema() + "\"")    
        
        else:
            self.sinalizaErroSintatico("Esperado \"def\"; encontrado " + "\""+ self.token.getLexema() + "\"")
        
    def RegexDeclaraId(self):
        # RegexDeclaraId ->  DeclaraID RegexDeclaraId  | ε 
        if (self.eat(Tag.KW_INTEGER) or self.eat(Tag.KW_STRING) or self.eat(Tag.KW_DOUBLE) or self.eat(Tag.KW_VOID)):
            self.DeclaraID()
            self.RegexDeclaraId()
        else:
            return
    
    def ListaArg(self):
        # ListaArg -> Arg ListaArg’
        self.Arg()
        self.ListaArgLinha
    
    def ListaArgLinha(self):
        # ListaArg’ -> "," ListaArg | ε 
        if (self.eat(Tag.VG)):
            self.ListaArg()
        else:
            return

    def Arg(self):
        # Arg -> TipoPrimitivo ID
        self.TipoPrimitivo()
        if(not self.eat(Tag.ID))
            self.sinalizaErroSintatico("Esperado \"ID\"; encontrado " + "\""+ self.token.getLexema() + "\"")
        
    def Retorno():
        # Retorno -> "return" Expressao ";" | ε 
        if (self.eat(Tag.KW_RETURN)):
            self.Expressao()
            if (not self.eat(Tag.PV)):
                self.sinalizaErroSintatico("Esperado \";\"; encontrado " + "\""+ self.token.getLexema() + "\"")
        else:
            return
    
    def Main(self):
        # Main -> "defstatic" "void" "main" "(" "String" "[" "]" ID ")" ":" RegexDeclaraId ListaCmd "end" ";" 
        if (self.eat(Tag.KW_DEFSTATIC)):
            if (not self.eat(Tag.KW_VOID)):
                self.sinalizaErroSintatico("Esperado \"void\"; encontrado " + "\""+ self.token.getLexema() + "\"")

            if (not self.eat(Tag.KW_MAIN)):
                self.sinalizaErroSintatico("Esperado \"main\"; encontrado " + "\""+ self.token.getLexema() + "\"")

            if (not self.eat(Tag.AP)):
                self.sinalizaErroSintatico("Esperado \"(\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            
            if (not self.eat(Tag.KW_STRING)):
                self.sinalizaErroSintatico("Esperado \"String\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            
            if (not self.eat(Tag.AC)):
                self.sinalizaErroSintatico("Esperado \"[\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            
            if (not self.eat(Tag.FC)):
                self.sinalizaErroSintatico("Esperado \"]\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            
            if (not self.eat(Tag.ID))
                self.sinalizaErroSintatico("Esperado \"ID\"; encontrado " + "\""+ self.token.getLexema() + "\"")

             if (not self.eat(Tag.FP)):
                self.sinalizaErroSintatico("Esperado \")\"; encontrado " + "\""+ self.token.getLexema() + "\"")

            if (not self.eat(Tag.DP)):
                self.sinalizaErroSintatico("Esperado \":\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            
            self.RegexDeclaraId()
            self.ListaCmd()

            if (not self.eat(Tag.KW_END)):
                self.sinalizaErroSintatico("Esperado \"end\"; encontrado " + "\""+ self.token.getLexema() + "\"")

            if (not self.eat(Tag.PV)):
                self.sinalizaErroSintatico("Esperado \";\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            
        else:
            self.sinalizaErroSintatico("Esperado \"defstatic\"; encontrado " + "\""+ self.token.getLexema() + "\"")
    
    def TipoPrimitivo(self):
        # TipoPrimitivo -> "bool" | "integer" | "String" | "double" | "void"
        if (not self.eat(Tag.KW_BOLL) or not self.eat(Tag.KW_INTEGER) or not self.eat(Tag.KW_STRING) or not self.eat(Tag.KW_DOUBLE) or not self.eat(Tag.KW_VOID)):
            self.sinalizaErroSintatico("Esperado \"'boll' ou 'integer' ou 'String' ou 'double' ou 'void'\"; encontrado " + "\""+ self.token.getLexema() + "\"")
    
    def ListaCmd(self):
        # ListaCmd -> ListaCmd’ 
        self.ListaCmdLinha()
    
    def ListaCmdLinha(self):
        # ListaCmd’ -> Cmd ListaCmd’ | ε
        if (self.eat(Tag.KW_IF) or self.eat(Tag.KW_WHILE) or self.eat(Tag.ID) or self.eat(Tag.KW_WRITE)):
            self.Cmd()
            self.ListaCmdLinha()
        else:
            return

    def Cmd(self):
        # Cmd -> CmdIF | CmdWhile | ID CmdAtribFunc | CmdWrite
        if (self.eat(Tag.KW_IF)):
            self.CmdIf()
        elif (self.eat(Tag.KW_WHILE)):
            self.CmdWhile()
        elif (self.eat(Tag.ID)):
            self.CmdAtribFunc()
        elif (self.eat(Tag.KW_WRITE)):
            self.CmdWrite
        else:
            self.sinalizaErroSintatico("Esperado \"'if' ou 'while' ou 'ID' ou 'write'\"; encontrado " + "\""+ self.token.getLexema() + "\"")
        
    def CmdAtribFunc(self):
        # CmdAtribFunc -> CmdAtribui | CmdFuncao
        if (self.eat(Tag.CP)):
            self.CmdAtribui()
        elif (self.eat(Tag.AP)):
            self.CmdFuncao()
        else:
            self.sinalizaErroSintatico("Esperado \"'=' ou '('\"; encontrado " + "\""+ self.token.getLexema() + "\"")
    def CmdIF(self):
        # CmdIF -> "if" "(" Expressao ")" ":" ListaCmd CmdIF’
        if (self.eat(Tag.KW_IF)):
            if (not self.eat(Tag.AP)):
                self.sinalizaErroSintatico("Esperado \"(\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            
            self.Expressao()

            if (not self.eat(Tag.FP)):
                self.sinalizaErroSintatico("Esperado \")\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            elif (self.eat(Tag.DP)):
                self.sinalizaErroSintatico("Esperado \":\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            
            self.ListaCmd()
            self.CmdIFLinha()
        else:
            self.sinalizaErroSintatico("Esperado \"if\"; encontrado " + "\""+ self.token.getLexema() + "\"")
    
    def CmdIFLinha(self):
        # CmdIF-> "end" ";" | "else" ":" ListaCmd "end" ";"
        if (self.eat(Tag.KW_END)):
            if (not self.eat(Tag.PV)):
                self.sinalizaErroSintatico("Esperado \";\"; encontrado " + "\""+ self.token.getLexema() + "\"")
        elif (self.eat(Tag.KW_ELSE)):
            if (not self.eat(Tag.DP)):
                self.sinalizaErroSintatico("Esperado \":\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            
            self.ListaCmd()

            if (not self.eat(Tag.KW_END)):
                self.sinalizaErroSintatico("Esperado \"end\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            elif (not self.eat(Tag.PV)):
                self.sinalizaErroSintatico("Esperado \";\"; encontrado " + "\""+ self.token.getLexema() + "\"")
        else:
            self.sinalizaErroSintatico("Esperado \"'end' ou 'else'\"; encontrado " + "\""+ self.token.getLexema() + "\"")
    
    def CmdWhile(self):
        # CmdWhile -> "while" "(" Expressao ")" ":" ListaCmd "end" ";"
        if (self.eat(Tag.KW_WHILE)):
            if (not self.eat(Tag.AP)):
                self.sinalizaErroSintatico("Esperado \"(\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            
            self.Expressao()

            if (not self.eat(Tag.FP)):
                self.sinalizaErroSintatico("Esperado \")\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            elif (not self.eat(Tag.DP)):
                self.sinalizaErroSintatico("Esperado \":\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            
            self.ListaCmd()

            if (not self.eat(Tag.KW_END)):
                self.sinalizaErroSintatico("Esperado \"end\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            elif (not self.eat(Tag.PV)):
                self.sinalizaErroSintatico("Esperado \";\"; encontrado " + "\""+ self.token.getLexema() + "\"")
        else:
            self.sinalizaErroSintatico("Esperado \"while\"; encontrado " + "\""+ self.token.getLexema() + "\"")
    
    def CmdWrite(self):
        # CmdWrite -> "write" "(" Expressao ")" ";"
        if (self.eat(Tag.KW_WRITE)):
            if (not self.eat(Tag.AP)):
                self.sinalizaErroSintatico("Esperado \"(\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            
            self.Expressao()

            if (not self.eat(Tag.FP)):
                self.sinalizaErroSintatico("Esperado \")\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            elif (not self.eat(Tag.PV)):
                self.sinalizaErroSintatico("Esperado \";\"; encontrado " + "\""+ self.token.getLexema() + "\"")
        else:
             self.sinalizaErroSintatico("Esperado \"write\"; encontrado " + "\""+ self.token.getLexema() + "\"")
    
    def CmdAtribui(self):
        # CmdAtribui -> "=" Expressao ";"
        if (self.eat(Tag.CP)):
            
            self.Expressao()

            if (not self.eat(Tag.PV)):
                self.sinalizaErroSintatico("Esperado \";\"; encontrado " + "\""+ self.token.getLexema() + "\"")
        else:
            self.sinalizaErroSintatico("Esperado \"=\"; encontrado " + "\""+ self.token.getLexema() + "\"")
    
    def CmdFuncao(self):
        # CmdFuncao → "(" RegexExp ")" ";"
        if(self.eat(Tag.AP)):
            self.RegexExp()

            if(not self.eat(Tag.FP)):
                self.sinalizaErroSintatico("Esperado \")\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            elif (not self.eat(Tag.PV)):
                self.sinalizaErroSintatico("Esperado \";\"; encontrado " + "\""+ self.token.getLexema() + "\"")
        else:
            self.sinalizaErroSintatico("Esperado \"(\"; encontrado " + "\""+ self.token.getLexema() + "\"")

    def RegexExp(self):
        # RegexExp → Expressao RegexExp’ | ε
        if (self.eat(Tag.ID)):
            self.Expressao()
            self.RegexExpLinha()
        else:
            return
    
    def RegexExpLinha(self):
        # RegexExp’ → "," Expressao RegexExp’ | ε
        if (self.eat(Tag.VG)):
            self.Expressao()
            self.RegexExpLinha()
        else:
            return

    def Expressao(self):
        # Expressao -> Exp1 Exp’ 
        self.Exp1()
        self.ExpLinha()
    
    def ExpLinha(self):
        # Exp’ -> "or" Exp1 Exp’ | "and" Exp1 Exp’ | ε
        if (self.eat(Tag.KW_OR) or self.eat(Tag.KW_AND)):
            self.Exp1()
            self.ExpLinha()
        else:
            return

    def Exp1(self):
        # Exp1 -> Exp2 Exp1’
        self.Exp2()
        self.Exp1Linha()
    
    def Exp1Linha(self):
        # Exp1’ -> "<" Exp2 Exp1’ | "<=" Exp2 Exp1’ | ">" Exp2 Exp1’ | ">=" Exp2 Exp1’ | "==" Exp2 Exp1’ | "!=" Exp2 Exp1’ | ε
        if (self.eat(Tag.OP_MENOR) or self.eat(Tag.OP_MAIOR_IGUAL) or self.eat(Tag.OP_MENOR_IGUAL) or self.eat(Tag.OP_MAIOR) or self.eat(Tag.OP_IGUAL) or self.eat(Tag.OP_DIFERENTE)):
            self.Exp2()
            self.Exp1Linha()
        else:
            return
    
    def Exp2(self):
        #Exp2 -> Exp3 Exp2’
        self.Exp3()
        self.Exp2Linha()
    
    def Exp2Linha(self):
        # Exp2’ -> "+" Exp3 Exp2’ | "-" Exp3 Exp2’ | ε
        if (self.eat(Tag.OP_SOMA) or self.eat(Tag.OP_MENOR)):
            self.Exp3()
            self.Exp2Linha()
        else:
            return
    
    def Exp3(self):
        # Exp3 -> Exp4 Exp3’ 
        self.Exp4()
        self.Exp3Linha()
    
    def Exp3Linha(self):
        # Exp3’ -> "*" Exp4 Exp3’ | "/" Exp4 Exp3’ | ε
        if (self.eat(Tag.OP_MULTIPLICACAO) or self.eat(Tag.OP_DIVISAO)):
            self.Exp4()
            self.Exp3Linha()
        else:
            return

    def Exp4(self):
        # Exp4 -> ID Exp4’ | ConstInteger | ConstDouble | ConstString | "true" | "false" | OpUnario Exp4 | "(" Expressao")"
        if (self.eat(Tag.ID) or self.eat(Tag.OP_SUBTRACAO)):
            self.Exp4linha()
        elif ()


            