import sys
import copy

from ts import TS
from tag import Tag
from token1 import Token
from lexer import Lexer
from no import No

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
        self.token = lexer.proxToken(None) # Leitura inicial obrigatoria do primeiro simbolo
        self.last_token = None
        self.ts = TS()
        if self.token is None: # erro no Lexer
            sys.exit(0)

    def sinalizaErroSemantico(self, message):
      print("[Erro Semantico] na linha " + str(self.token.getLinha()) + " e coluna " + str(self.token.getColuna()) + ": ")
      print(message, "\n")

    def sinalizaErroSintatico(self, message):
        print("[Erro Sintatico] na linha " + str(self.token.getLinha()) + " e coluna " + str(self.token.getColuna()) + ": ")
        print(message, "\n")

    def advance(self):
        #print("[DEBUG] token: ", self.token.toString())
        self.token = self.lexer.proxToken(self.last_token)  
        self.last_token = self.token
        if self.token is None: # erro no Lexer
            sys.exit(0)
   
    def skip(self, message):
      self.sinalizaErroSintatico(message)
      self.advance()

    # verifica token esperado t 
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
        if (self.token.getNome() != Tag.EOF):
            self.sinalizaErroSintatico("Esperado \"EOF\"; encontrado " + "\""+ self.token.getLexema() + "\"")

    def Classe(self):
        # Classe -> "class" ID ":" ListaFuncao Main "end" "." 
        tempToken = copy.copy(self.token) # armazena token corrente (necessario para id da regra)

        if (self.eat(Tag.KW_CLASS)):
            if (not self.eat(Tag.ID)):
                self.sinalizaErroSintatico("Esperado \"ID\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            else:
                self.lexer.ts.removeToken(tempToken.getLexema())
                tempToken.setTipo(Tag.TIPO_VAZIO)
                self.lexer.ts.addToken(tempToken.getLexema(), tempToken)

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
        noTipoPrimitivo = self.TipoPrimitivo()

        tempToken = copy.copy(self.token) # armazena token corrente (necessario para id da regra)

        if (self.eat(Tag.ID)):
            self.ts.setTipo(tempToken.getLexema(), noTipoPrimitivo.tipo)            
            if (not self.eat(Tag.PV)):
                self.sinalizaErroSintatico("Esperado \" ; \"; encontrado " + "\""+ self.token.getLexema() + "\"")
                sys.exit(0)
        else:
            self.sinalizaErroSintatico("Esperado \"ID\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            sys.exit(0)
    
    def ListaFuncao(self):
        # ListaFuncao -> ListaFuncao’ 
        self.ListaFuncaoLinha()
    
    def ListaFuncaoLinha(self):
        # ListaFuncao’ -> Funcao ListaFuncao’ | ε
        if (self.token.getNome() == Tag.KW_DEF):
            self.Funcao()
            self.ListaFuncao()
        else:
            return
    
    def Funcao(self):
        # Funcao -> "def" TipoPrimitivo ID "(" ListaArg ")" ":" RegexDeclaraId ListaCmd Retorno "end" ";" 
        tempToken = copy.copy(self.token) # armazena token corrente (necessario para id da regra)

        if (self.eat(Tag.KW_DEF)):
            noTipoPrimitivo = self.TipoPrimitivo()

            if (not self.eat(Tag.ID)):
                self.sinalizaErroSintatico("Esperado \"ID\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            else:
                self.lexer.ts.removeToken(tempToken.getLexema())
                tempToken.setTipo(noTipoPrimitivo.tipo)
                self.lexer.ts.addToken(tempToken.getLexema(), tempToken)
                
            if (not self.eat(Tag.AP)):
                self.sinalizaErroSintatico("Esperado \"(\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            
            self.ListaArg()

            if (not self.eat(Tag.FP)):
                self.sinalizaErroSintatico("Esperado \")\"; encontrado " + "\""+ self.token.getLexema() + "\"")

            if (not self.eat(Tag.DP)):
                self.sinalizaErroSintatico("Esperado \":\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            
            self.RegexDeclaraId()
            self.ListaCmd()
            noRetorno = self.Retorno()
            if (noRetorno.tipo != noTipoPrimitivo.tipo):
                self.sinalizaErroSemantico("Tipo de retorno incompativel.")

            if (not self.eat(Tag.KW_END)):
                self.sinalizaErroSintatico("Esperado \"end\"; encontrado " + "\""+ self.token.getLexema() + "\"")

            if (not self.eat(Tag.PV)):
                self.sinalizaErroSintatico("Esperado \";\"; encontrado " + "\""+ self.token.getLexema() + "\"")    
        
        else:
            self.sinalizaErroSintatico("Esperado \"def\"; encontrado " + "\""+ self.token.getLexema() + "\"")
        
    def RegexDeclaraId(self):
        # RegexDeclaraId ->  DeclaraID RegexDeclaraId  | ε 
        if (self.token.getNome() == Tag.KW_INTEGER or self.token.getNome() == Tag.KW_STRING or self.token.getNome() == Tag.KW_DOUBLE or self.token.getNome() == Tag.KW_VOID):
            self.DeclaraID()
            self.RegexDeclaraId()
        else:
            return
    
    def ListaArg(self):
        # ListaArg -> Arg ListaArg’
        self.Arg()
        self.ListaArgLinha()
    
    def ListaArgLinha(self):
        # ListaArg’ -> "," ListaArg | ε 
        if (self.eat(Tag.VG)):
            self.ListaArg()
        else:
            return

    def Arg(self):
        # Arg -> TipoPrimitivo ID
        tempToken = copy.copy(self.token) # armazena token corrente (necessario para id da regra)

        noTipoPrimitivo = self.TipoPrimitivo()

        if (not self.eat(Tag.ID)):
            self.sinalizaErroSintatico("Esperado \"ID\"; encontrado " + "\""+ self.token.getLexema() + "\"")
        else:
            self.lexer.ts.removeToken(tempToken.getLexema())
            tempToken.setTipo(noTipoPrimitivo.tipo)
            self.lexer.ts.addToken(tempToken.getLexema(), tempToken)

    def Retorno(self):
        # Retorno -> "return" Expressao ";" | ε 
        noRetorno = No()
        if (self.eat(Tag.KW_RETURN)):
            noExpressao = self.Expressao()
            if (not self.eat(Tag.PV)):
                self.sinalizaErroSintatico("Esperado \";\"; encontrado " + "\""+ self.token.getLexema() + "\"")
                sys.exit(0)
            noRetorno.tipo = noExpressao.tipo

            return noRetorno
        else:
            noRetorno.tipo = Tag.TIPO_VAZIO
            return noRetorno
    
    def Main(self):
        # Main -> "defstatic" "void" "main" "(" "String" "[" "]" ID ")" ":" RegexDeclaraId ListaCmd "end" ";" 
        tempToken = copy.copy(self.token) # armazena token corrente (necessario para id da regra)

        if (self.eat(Tag.KW_DEFSTATIC)):
            if (not self.eat(Tag.KW_VOID)):
                self.sinalizaErroSintatico("Esperado \"void\"; encontrado " + "\""+ self.token.getLexema() + "\"")

            if (not self.eat(Tag.KW_MAIN)):
                self.sinalizaErroSintatico("Esperado \"main\"; encontrado " + "\""+ self.token.getLexema() + "\"")

            if (not self.eat(Tag.AP)):
                self.sinalizaErroSintatico("Esperado \"(\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            
            if (not self.eat(Tag.KW_STRING)):
                self.sinalizaErroSintatico("Esperado \"String\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            
            if (not self.eat(Tag.AT)):
                self.sinalizaErroSintatico("Esperado \"[\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            
            if (not self.eat(Tag.FT)):
                self.sinalizaErroSintatico("Esperado \"]\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            
            if (not self.eat(Tag.ID)):
                self.sinalizaErroSintatico("Esperado \"ID\"; encontrado " + "\""+ self.token.getLexema() + "\"")

            self.lexer.ts.removeToken(tempToken.getLexema())
            tempToken.setTipo(Tag.TIPO_STRING)
            self.lexer.ts.addToken(tempToken.getLexema(), tempToken)

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
        noTipoPrimitivo = No()
        if (self.token.getNome() == Tag.KW_BOOL):
            self.eat(Tag.KW_BOOL)

            noTipoPrimitivo.tipo = Tag.TIPO_LOGICO
            
        elif (self.token.getNome() == Tag.KW_INTEGER):
            self.eat(Tag.KW_INTEGER)

            noTipoPrimitivo.tipo = Tag.TIPO_INT
            
        elif (self.token.getNome() == Tag.KW_STRING):
            self.eat(Tag.KW_STRING)

            noTipoPrimitivo.tipo = Tag.TIPO_STRING
            
        elif (self.token.getNome() == Tag.KW_DOUBLE):
            self.eat(Tag.KW_DOUBLE)

            noTipoPrimitivo.tipo = Tag.TIPO_DOUBLE
            
        elif (self.token.getNome() == Tag.KW_VOID):
            self.eat(Tag.KW_VOID)

            noTipoPrimitivo.tipo = Tag.TIPO_VAZIO
            
        else:
            self.sinalizaErroSintatico("Esperado \"'bool' ou 'integer' ou 'String' ou 'double' ou 'void'\"; encontrado " + "\""+ self.token.getLexema() + "\"")
        
        return noTipoPrimitivo
    
    def ListaCmd(self):
        # ListaCmd -> ListaCmd’ 
        self.ListaCmdLinha()
    
    def ListaCmdLinha(self):
        # ListaCmd’ -> Cmd ListaCmd’ | ε
        if (self.token.getNome() == Tag.KW_IF or self.token.getNome() == Tag.KW_WHILE or self.token.getNome() == Tag.ID or self.token.getNome() == Tag.KW_WRITE):
            self.Cmd()
            self.ListaCmdLinha()
        else:
            return

    def Cmd(self):
        # Cmd -> CmdIF | CmdWhile | ID CmdAtribFunc | CmdWrite
        tempToken = copy.copy(self.token) # armazena token corrente (necessario para id da regra)

        if (self.token.getNome() == Tag.KW_IF):
            self.CmdIF()
        elif (self.token.getNome() == Tag.KW_WHILE):
            self.CmdWhile()
        elif (self.eat(Tag.ID)):
            if (tempToken.getTipo() == None):
                self.sinalizaErroSemantico("ID não declarado")
                sys.exit(0)

            noCmdAtribFunc = self.CmdAtribFunc()

            if (noCmdAtribFunc.tipo != Tag.TIPO_VAZIO and tempToken.getTipo() != noCmdAtribFunc.tipo):
                self.sinalizaErroSemantico("Atribuição incompativel")
                sys.exit(0)
                
        elif (self.token.getNome() == Tag.KW_WRITE):
            self.CmdWrite()
        else:
            self.sinalizaErroSintatico("Esperado \"'if' ou 'while' ou 'ID' ou 'write'\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            sys.exit(0)
        
    def CmdAtribFunc(self):
        # CmdAtribFunc -> CmdAtribui | CmdFuncao
        noCmdAtribFunc = No()

        if (self.token.getNome() == Tag.CP):
            noCmdAtribui = self.CmdAtribui()
            noCmdAtribFunc.tipo = noCmdAtribui.tipo

            return noCmdAtribFunc

        elif (self.token.getNome() == Tag.AP):
            self.CmdFuncao()
            noCmdAtribFunc.tipo = Tag.TIPO_VAZIO

            return noCmdAtribFunc

        else:
            self.sinalizaErroSintatico("Esperado \"'=' ou '('\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            sys.exit(0)
   
    def CmdIF(self):
        # CmdIF -> "if" "(" Expressao ")" ":" ListaCmd CmdIF’
        if (self.eat(Tag.KW_IF)):
            if (not self.eat(Tag.AP)):
                self.sinalizaErroSintatico("Esperado \"(\"; encontrado " + "\""+ self.token.getLexema() + "\"")
                sys.exit(0)
            
            noExpressao = self.Expressao()

            if (not self.eat(Tag.FP)):
                self.sinalizaErroSintatico("Esperado \")\"; encontrado " + "\""+ self.token.getLexema() + "\"")
                sys.exit(0)

            if (noExpressao.tipo != Tag.TIPO_LOGICO):
                self.sinalizaErroSemantico("Erro Semantico")
                sys.exit(0)

            elif (not self.eat(Tag.DP)):
                self.sinalizaErroSintatico("Esperado \":\"; encontrado " + "\""+ self.token.getLexema() + "\"")
                sys.exit(0)
            
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
                sys.exit(0)
            
            noExpressao = self.Expressao()

            if (not self.eat(Tag.FP)):
                self.sinalizaErroSintatico("Esperado \")\"; encontrado " + "\""+ self.token.getLexema() + "\"")
                sys.exit(0)

            if (noExpressao.tipo != Tag.TIPO_LOGICO):
                self.sinalizaErroSemantico("Erro Semantico")
                sys.exit(0)

            elif (not self.eat(Tag.DP)):
                self.sinalizaErroSintatico("Esperado \":\"; encontrado " + "\""+ self.token.getLexema() + "\"")
                sys.exit(0)
            
            self.ListaCmd()

            if (not self.eat(Tag.KW_END)):
                self.sinalizaErroSintatico("Esperado \"end\"; encontrado " + "\""+ self.token.getLexema() + "\"")
                sys.exit(0)
            elif (not self.eat(Tag.PV)):
                self.sinalizaErroSintatico("Esperado \";\"; encontrado " + "\""+ self.token.getLexema() + "\"")
                sys.exit(0)
        else:
            self.sinalizaErroSintatico("Esperado \"while\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            sys.exit(0)
    
    def CmdWrite(self):
        # CmdWrite -> "write" "(" Expressao ")" ";"
        if (self.eat(Tag.KW_WRITE)):
            if (not self.eat(Tag.AP)):
                self.sinalizaErroSintatico("Esperado \"(\"; encontrado " + "\""+ self.token.getLexema() + "\"")
                sys.exit(0)
            
            noExpressao = self.Expressao()

            if (not self.eat(Tag.FP)):
                self.sinalizaErroSintatico("Esperado \")\"; encontrado " + "\""+ self.token.getLexema() + "\"")
                sys.exit(0)
            elif (not self.eat(Tag.PV)):
                self.sinalizaErroSintatico("Esperado \";\"; encontrado " + "\""+ self.token.getLexema() + "\"")
                sys.exit(0)
            
            if (noExpressao.tipo != Tag.TIPO_STRING):
                self.sinalizaErroSemantico("Erro Semantico")
                sys.exit(0)

        else:
            self.sinalizaErroSintatico("Esperado \"write\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            sys.exit(0)
    
    def CmdAtribui(self):
        # CmdAtribui -> "=" Expressao ";"
        noCmdAtribui = No()
        if (self.eat(Tag.CP)):
            
            noExpressao = self.Expressao()

            if (not self.eat(Tag.PV)):
                self.sinalizaErroSintatico("Esperado \";\"; encontrado " + "\""+ self.token.getLexema() + "\"")
                sys.exit(0)

            noCmdAtribui.tipo = noExpressao.tipo

            return noCmdAtribui
        else:
            self.sinalizaErroSintatico("Esperado \"=\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            sys.exit(0)
    
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
        if ((self.token.getNome() == Tag.ID) or (self.token.getNome() == Tag.OP_INVERSOR) or (self.token.getNome() == Tag.OP_NEGACAO) or (self.token.getNome() == Tag.AP) or (self.token.getNome() == Tag.KW_INTEGER) or (self.token.getNome() == Tag.KW_DOUBLE) or (self.token.getNome() == Tag.KW_STRING) or (self.token.getNome() == Tag.KW_TRUE) or (self.token.getNome() == Tag.KW_FALSE)):
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
        
        noExpressao = No()

        noExp1 = self.Exp1()
        noExpLinha = self.ExpLinha()

        if (noExpLinha.tipo == Tag.TIPO_VAZIO):
            noExpressao.tipo = noExp1.tipo
        
        elif (noExpLinha.tipo == noExp1.tipo and noExpLinha.tipo == Tag.TIPO_LOGICO):
            noExpressao.tipo = Tag.TIPO_LOGICO
        
        else:
            noExpressao.tipo = Tag.TIPO_ERRO

        return noExpressao
    
    def ExpLinha(self):
        noExpLinha = No()
        # Exp’ -> "or" Exp1 Exp’ | "and" Exp1 Exp’ | ε
        if (self.eat(Tag.KW_OR) or self.eat(Tag.KW_AND)):
            noExp1 = self.Exp1()
            noExpLinhaFilho = self.ExpLinha()

            if (noExpLinhaFilho.tipo == Tag.TIPO_VAZIO and noExp1.tipo == Tag.TIPO_LOGICO):
                noExpLinha.tipo = Tag.TIPO_LOGICO
            
            elif (noExpLinhaFilho.tipo == noExp1.tipo and noExp1.tipo == Tag.TIPO_LOGICO):
                noExpLinha.tipo = Tag.TIPO_LOGICO
            
            else:
                noExpLinha.tipo = Tag.TIPO_ERRO
            
            return noExpLinha
        else:
            noExpLinha.tipo = Tag.TIPO_VAZIO
            return noExpLinha

    def Exp1(self):
        # Exp1 -> Exp2 Exp1’
        noExp1 = No()

        noExp2 = self.Exp2()
        noExp1Linha = self.Exp1Linha()

        if (noExp1Linha.tipo == Tag.TIPO_VAZIO):
            noExp1.tipo = noExp2.tipo
        
        elif (noExp1Linha.tipo == noExp2.tipo and (noExp1Linha.tipo == Tag.TIPO_INT or noExp1Linha.tipo == Tag.TIPO_DOUBLE ) ):
            noExp1.tipo = Tag.TIPO_LOGICO
        
        else:
            noExp1.tipo = Tag.TIPO_ERRO
        
        return noExp1
    
    def Exp1Linha(self):
        # Exp1’ -> "<" Exp2 Exp1’ | "<=" Exp2 Exp1’ | ">" Exp2 Exp1’ | ">=" Exp2 Exp1’ | "==" Exp2 Exp1’ | "!=" Exp2 Exp1’ | ε
        noExp1Linha = No()

        if (self.eat(Tag.OP_MENOR) or self.eat(Tag.OP_MAIOR_IGUAL) or self.eat(Tag.OP_MENOR_IGUAL) or self.eat(Tag.OP_MAIOR) or self.eat(Tag.OP_IGUAL) or self.eat(Tag.OP_DIFERENTE)):
            noExp2 = self.Exp2()
            noExp1LinhaFilho = self.Exp1Linha()

            if (noExp1LinhaFilho.tipo == Tag.TIPO_VAZIO and noExp2.tipo == Tag.TIPO_INT):
                noExp1Linha.tipo = Tag.TIPO_INT
            
            elif (noExp1LinhaFilho.tipo == Tag.TIPO_VAZIO and noExp2.tipo == Tag.TIPO_DOUBLE):
                noExp1Linha.tipo = Tag.TIPO_DOUBLE
            
            elif (noExp1LinhaFilho.tipo == noExp2.tipo and noExp2.tipo == Tag.TIPO_INT):
                noExp1Linha.tipo = Tag.TIPO_INT

            elif (noExp1LinhaFilho.tipo == noExp2.tipo and noExp2.tipo == Tag.TIPO_DOUBLE):
                noExp1Linha.tipo = Tag.TIPO_DOUBLE
            
            else:
                noExp1Linha.tipo = Tag.TIPO_ERRO
            
            return noExp1Linha

        else:
            noExp1Linha.tipo = Tag.TIPO_VAZIO
            return noExp1Linha
    
    def Exp2(self):
        #Exp2 -> Exp3 Exp2’
        noExp2 = No()

        noExp3 = self.Exp3()
        noExp2Linha = self.Exp2Linha()

        if (noExp2Linha.tipo == Tag.TIPO_VAZIO):
            noExp2.tipo = noExp3.tipo
        
        elif (noExp2Linha.tipo == noExp3.tipo and noExp2Linha.tipo == Tag.TIPO_INT):
            noExp2.tipo = Tag.TIPO_INT

        elif (noExp2Linha.tipo == noExp3.tipo and noExp2Linha.tipo == Tag.TIPO_DOUBLE):
            noExp2.tipo = Tag.TIPO_DOUBLE

        else:
            noExp2.tipo = Tag.TIPO_ERRO

        return noExp2
    
    def Exp2Linha(self):
        # Exp2’ -> "+" Exp3 Exp2’ | "-" Exp3 Exp2’ | ε
        noExp2Linha = No()

        if (self.eat(Tag.OP_SOMA) or self.eat(Tag.OP_MENOR)):
            noExp3 = self.Exp3()
            noExp2LinhaFilho = self.Exp2Linha()

            if (noExp2LinhaFilho.tipo == Tag.TIPO_VAZIO and noExp3.tipo == Tag.TIPO_INT):
                noExp2Linha.tipo = Tag.TIPO_INT
            
            elif (noExp2LinhaFilho.tipo == Tag.TIPO_VAZIO and noExp3.tipo == Tag.TIPO_DOUBLE):
                noExp2Linha.tipo = Tag.TIPO_DOUBLE

            elif (noExp2LinhaFilho.tipo == noExp3.tipo and noExp3.tipo == Tag.TIPO_INT):
                noExp2Linha.tipo = Tag.TIPO_INT

            elif (noExp2LinhaFilho.tipo == noExp3.tipo and noExp3.tipo == Tag.TIPO_DOUBLE):
                noExp2Linha.tipo = Tag.TIPO_DOUBLE
            
            else:
                noExp2Linha.tipo = Tag.TIPO_ERRO
            
            return noExp2Linha

        else:
            noExp2Linha.tipo = Tag.TIPO_VAZIO
            return noExp2Linha
    
    def Exp3(self):
        # Exp3 -> Exp4 Exp3’ 
        noExp3 = No()

        noExp4 = self.Exp4()
        noExp3Linha = self.Exp3Linha()

        if (noExp3Linha.tipo == Tag.TIPO_VAZIO):
            noExp3.tipo = noExp4.tipo
        
        elif (noExp3Linha == noExp4.tipo and noExp3Linha.tipo == Tag.TIPO_INT):
            noExp3.tipo = Tag.TIPO_INT
        
        elif (noExp3Linha == noExp4.tipo and noExp3Linha.tipo == Tag.TIPO_DOUBLE):
            noExp3.tipo = Tag.TIPO_DOUBLE

        else:
            noExp3Linha.tipo = Tag.TIPO_ERRO
        
        return noExp3
    
    def Exp3Linha(self):
        # Exp3’ -> "*" Exp4 Exp3’ | "/" Exp4 Exp3’ | ε
        noExp3Linha = No()

        if (self.eat(Tag.OP_MULTIPLICACAO) or self.eat(Tag.OP_DIVISAO)):
            noExp4 = self.Exp4()
            noExp3LinhaFilho = self.Exp3Linha()

            if (noExp3LinhaFilho.tipo == Tag.TIPO_VAZIO and noExp4.tipo == Tag.TIPO_INT):
                noExp3Linha.tipo = Tag.TIPO_INT
            
            elif (noExp3LinhaFilho.tipo == Tag.TIPO_VAZIO and noExp4.tipo == Tag.TIPO_DOUBLE):
                noExp3Linha.tipo = Tag.TIPO_DOUBLE

            elif (noExp3LinhaFilho.tipo == noExp4.tipo and noExp4.tipo == Tag.TIPO_INT):
                noExp3Linha.tipo = Tag.TIPO_INT
            
            elif (noExp3LinhaFilho.tipo == noExp4.tipo and noExp4.tipo == Tag.TIPO_DOUBLE):
                noExp3Linha.tipo = Tag.TIPO_DOUBLE
            
            else:
                noExp3Linha.tipo = Tag.TIPO_ERRO

            return noExp3Linha 

        else:
            noExp3Linha.tipo = Tag.TIPO_VAZIO
            return noExp3Linha

    def Exp4(self):
        # Exp4 -> ID Exp4’ | ConstInteger | ConstDouble | ConstString | "true" | "false" | OpUnario Exp4 | "(" Expressao")"
        tempToken = copy.copy(self.token) # armazena token corrente (necessario para id da regra)
        noExp4 = No()

        if (self.eat(Tag.ID)):
            self.Exp4Linha()
            
            noExp4.tipo = tempToken.getTipo()
            
            if (noExp4.tipo == None ):
                noExp4.tipo = Tag.TIPO_ERRO
                self.sinalizaErroSemantico("Erro, ID nao declado")
                sys.exit(0)
            

        elif (self.token.getNome() == Tag.OP_INVERSOR or self.token.getNome() == Tag.OP_NEGACAO):
            noOpUnario = self.OpUnario()
            noExp4Filho = self.Exp4()

            if (noExp4Filho.tipo == noOpUnario.tipo and noOpUnario.tipo == Tag.TIPO_INT):
                noExp4Filho.tipo = Tag.TIPO_INT

            elif (noExp4Filho.tipo == noOpUnario.tipo and noOpUnario.tipo == Tag.TIPO_DOUBLE):
                noExp4Filho.tipo = Tag.TIPO_DOUBLE

            elif (noExp4Filho.tipo == noOpUnario.tipo and noOpUnario.tipo == Tag.TIPO_LOGICO):
                noExp4Filho.tipo = Tag.TIPO_LOGICO
            
        elif (self.eat(Tag.AP)):
            noExpressao = self.Expressao()
            if (not self.eat(Tag.FP)):
                self.sinalizaErroSintatico("Esperado \")\"; encontrado " + "\""+ self.token.getLexema() + "\"")
                sys.exit(0)
            noExp4.tipo = noExpressao.tipo
        
        elif (self.eat(Tag.KW_INTEGER)):
            noExp4.tipo = Tag.TIPO_INT
        
        elif (self.eat(Tag.KW_DOUBLE)):
            noExp4.tipo = Tag.TIPO_DOUBLE

        elif (self.eat(Tag.KW_STRING)):
            noExp4.tipo = Tag.TIPO_STRING

        elif (self.eat(Tag.KW_TRUE) or self.eat(Tag.KW_FALSE)):
            noExp4.tipo = Tag.TIPO_LOGICO

        else:            
            self.sinalizaErroSintatico(" Esperado \"'ID' ou 'Constante' ou '(' \"; encontrado " + "\""+ self.token.getLexema() + "\"")
            sys.exit(0)

        return noExp4

    def Exp4Linha(self):    
        # Exp4’ -> "(" RegexExp ")" | ε
        if (self.eat(Tag.AP)):
            self.RegexExp()
            if (not self.eat(Tag.FP)):
                self.sinalizaErroSintatico("Esperado \")\"; encontrado " + "\""+ self.token.getLexema() + "\"")
                sys.exit(0)
        else:
            return
    
    def OpUnario(self):
        #OpUnario -> "-" | "!"
        noOpUnario = No()
        if (self.eat(Tag.OP_INVERSOR)):
            noOpUnario.tipo = Tag.TIPO_LOGICO

        elif (self.eat(Tag.OP_NEGACAO)):
            noOpUnario.tipo = Tag.TIPO_INT

        else:
            self.sinalizaErroSintatico("Esperado \"'-' ou '!'\"; encontrado " + "\""+ self.token.getLexema() + "\"")
            sys.exit(0)
        
        return noOpUnario
