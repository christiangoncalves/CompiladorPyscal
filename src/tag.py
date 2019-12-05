from enum import Enum

class Tag(Enum):
    '''
    Uma representacao em constante de todos os nomes
    de tokens para a linguagem.
    '''

    # Fim de arquivo
    EOF = -1

    # Palavras-chave
    KW_IF        = 1
    KW_ELSE      = 2
    KW_PRINT     = 3
    KW_CLASS     = 4
    KW_DEF       = 5
    KW_DEFSTATIC = 6
    KW_BOOL      = 7
    KW_INTEGER   = 8
    KW_STRING    = 9
    KW_DOUBLE    = 10
    KW_VOID      = 11
    KW_MAIN      = 12
    KW_END       = 13
    KW_WRITE     = 14
    KW_OR        = 15
    KW_AND       = 16
    KW_TRUE      = 17
    KW_FALSE     = 18
    KW_RETURN    = 19
    KW_WHILE     = 20
    KW_PONTO     = 21

    # Operadores
    OP_MAIOR         = 22
    OP_IGUAL         = 23
    OP_DIFERENTE     = 24
    OP_DIVISAO       = 25
    OP_MULTIPLICACAO = 26
    OP_SUBTRACAO     = 27
    OP_SOMA          = 28
    OP_INVERSOR      = 29
    OP_NEGACAO       = 30
    OP_MENOR         = 31
    OP_MENOR_IGUAL   = 32
    OP_MAIOR_IGUAL   = 33

    # Identificador
    ID = 34

    #Especiais
    FC = 35 #Fecha chaves
    AT = 36 #Abre Colchetes
    FT = 37 #Fecha Colchetes
    CP = 38 #Atribuição '='
    VG = 39 #Virgula
    PV = 40 #Ponto e Virgula
    DP = 41 #Dois Pontos
    AC = 42 #Abre chaves
    AP = 43 #Abre parentesis
    FP = 44 #Fecha parentesis
    
    # Constantes para tipos
    TIPO_VAZIO   = 1000;
    TIPO_LOGICO  = 1001;
    TIPO_INT     = 1002;
    TIPO_DOUBLE  = 1003;
    TIPO_ERRO    = 1004;
    TIPO_STRING  = 1005;
