from enum import Enum

class Tag(Enum):
    '''
    Uma representacao em constante de todos os nomes
    de tokens para a linguagem.
    '''

    # Fim de arquivo
    EOF = -1

    # Palavras-chave
    KW_IF = 1
    KW_ELSE = 2
    KW_PRINT = 3
    KW_CLASS = 4
    KW_DEF = 5
    KW_DEFSTATIC = 6
    KW_BOLL = 7
    KW_INTEGER = 8
    KW_STRING = 9
    KW_DOUBLE = 10
    KW_VOID = 11
    KW_MAIN = 12
    KW_END = 13
    KW_WRITE = 14
    KW_OR = 15
    KW_AND = 16
    KW_TRUE = 17
    KW_FALSE = 18


    # Operadores
    OP_MENOR = 19
    OP_MENOR_IGUAL = 20
    OP_MAIOR_IGUAL = 21
    OP_MAIOR = 22
    OP_IGUAL = 23
    OP_DIFERENTE = 24
    OP_DIVISAO = 25
    OP_MULTIPLICACAO = 26
    OP_SUBTRACAO = 27
    OP_SOMA = 28

    # Identificador
    ID = 29

    # Numeros
    NUM = 30
