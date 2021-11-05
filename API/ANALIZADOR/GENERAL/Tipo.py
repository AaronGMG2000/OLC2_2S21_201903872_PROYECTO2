from enum import Enum


class Tipos(Enum):
    ENTERO = 'INT64'
    FLOAT = 'FLOAT64'
    BOOL = 'BOOL'
    CHAR = 'CHAR'
    STRING = 'STRING'
    ARRAY = 'ARREGLO'
    STRUCT = 'STRUCT'
    OBJECT = 'OBJECT'
    FUNCTION = 'FUNCTION'
    NOTHING = 'NOTHING'
    RANGE = 'RANGE'

class CICLICO(Enum):
    BREAK= 'BREAK'
    CONTINUE= 'CONTINUE'
    RETURN= 'RETURN'

class Aritmeticos(Enum):
    SUMA = '+'
    RESTA = '-'
    MULTIPLICACION = '*'
    DIVISION = '/'
    POTENCIA = '^'
    MODULO = '%'
class Relacionales(Enum):
    MAYOR = '>'
    MENOR = '<'
    MAYORIGUAL = '>='
    MENORIGUAL = '<='
    IGUAL = '=='
    DISTINTO = '!='

class Logicas(Enum):
    OR = '||'
    AND = '&&'
    NOT = '!'

class Tipos_Nativa(Enum):
    PARSE = 'PARSE'
    TRUNC = 'TRUNC'
    FLOAT = 'FLOAT'
    STRING = 'STRING'
    # TYPEOF = 'TYPEOF'
    LENGTH = 'LENGTH'
    UPPERCASE = 'UPPERCASE'
    LOWERCASE = 'LOWERCASE'
    # LOG10 = 'LOG10'
    # LOG = 'LOG' 
    # SIN = 'SIN' 
    # COS = 'COS'
    # TAN = 'TAN'
    # SQRT = 'SQRT'
