reservadas = {
    "print": "r_print",
    "println": "r_println",
    "true": "r_true",
    "false": "r_false",
    "parse": "r_parse",
    "trunc": "r_trunc",
    "float": "r_float",
    "string": "r_string",
    "String": "r_stringT",
    "nothing": "r_nothing",
    "Nothing": "r_nothingT",
    "Bool": "r_bool",
    "Char": "r_char",
    "typeof": "r_typeof",
    "Int64": "r_int64",
    "Float64": "r_float64",
    "lowercase": "r_lowercase",
    "uppercase": "r_uppercase",
    "log10": "r_log10",
    "log": "r_log",
    "sin": "r_sin",
    "cos": "r_cos",
    "tan": "r_tan",
    "sqrt": "r_sqrt",
    "if": "r_if",
    "elseif": "r_elseif",
    "else": "r_else",
    "end": "r_end",
    "while": "r_while",
    "for": "r_for",
    "in": "r_in"  
}

tokens = [
    "ptcoma",
    "coma",
    "pizq",
    "pder",
    "decimal",
    "int",
    "string",
    "char",
    "id",
    "suma",
    "resta",
    "div",
    "mul",
    "modulo",
    "elevado",
    "igual",
    "diferente",
    "mayor",
    "menor",
    "mayor_igual",
    "menor_igual",
    "or",
    "and",
    "not",
    "igualT",
    "dospuntos",
] + list(reservadas.values())

#condicionales y logicas
t_igual              = r'=='
t_diferente          = r'!='
t_mayor_igual        = r'>='
t_mayor              = r'>'
t_menor_igual        = r'<='
t_menor              = r'<'
t_or                 = r'\|\|'
t_and                = r'&&'
t_not                = r'!'

# tokens
t_coma               = r','
t_ptcoma             = r';'
t_dospuntos          = r':'
t_pizq               = r'\('
t_pder               = r'\)'
t_igualT             = r'='
#aritmetica
t_suma               = r'\+'
t_resta              = r'\-'
t_mul               = r'\*'
t_div                = r'/'
t_modulo             = r'\%'
t_elevado            = r'\^'



def t_id(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reservadas.get(t.value, 'id')

    return t


def t_decimal(t):
    r'\d+\.\d+'

    try:
        t.value = float(t.value)
    except ValueError:
        print(f"Float value too large {t.value}")
        t.value = 0
    return t


def t_int(t):
    r'\d+'
    
    try:
        t.value = int(t.value)
    except ValueError:
        print(f"Int value too large {t.value}")
        t.value = 0
    return t


def t_string(t):
    r'\".*?\"'
    t.value = t.value[1:-1]
    return t


def t_char(t):
    r'\'.?\''
    t.value = t.value[1:-1]
    return t


# Comentario de múltiples líneas /* .. */
def t_COMENTARIO_MULTIfila(t):
    r'\#=(.|\n)*?=\#'
    t.lexer.lineno += t.value.count('\n')


# Comentario simple // ...
def t_COMENTARIO_SIMPLE(t):
    r'\#.*'
    t.lexer.lineno += 1


#Ignorated chararcter
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    errors.append(Error("Lexical", f"This is illegal token {t.value[0]}", t.lexer.lineno, column(input, t)))
    t.lexer.skip(1)


def column(input_token, token):
    line_start = input_token.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1



from .PLY import lex
lexer = lex.lex()


errors = []


# precedencias 
precedence = (
    # ('left', 'TERNARIO'),
    ('left', 'or'),
    ('left', 'and'),
    ('right', 'not'),
    ('left', 'igual', 'diferente', 'mayor', 'mayor_igual', 'menor', 'menor_igual'),
    ('left', 'suma', 'resta'),
    ('left', 'mul', 'div', 'modulo'),
    ('left', 'elevado'),
    ('right', 'UMENOS')
    # ('right', 'FCAST'),
    # ('right', 'PLUS', 'MIN')
)

# Gramatica 


# Importaciones
import re
from .INSTRUCCIONES.print import Imprimir
from .INSTRUCCIONES.println import ImprimirEnter
from .INSTRUCCIONES.WHILE import WHILE
from .INSTRUCCIONES.Asignacion import Asignacion
from .INSTRUCCIONES.IF import IF
from .INSTRUCCIONES.condicion import CONDICION
from .EXPRESIONES.primitivo import Primitivo
from .EXPRESIONES.aritmetica import Aritmetica
from .EXPRESIONES.relacional import Relacional
from .EXPRESIONES.nativa import Nativas
from .EXPRESIONES.logica import Logica
from .GENERAL.Tipo import Tipos_Nativa, Tipos
from .GENERAL.Tipo import Relacionales
from .GENERAL.Tipo import Logicas
from .GENERAL.Tipo import Aritmeticos
from .GENERAL.error import Error
from .EXPRESIONES.variable import Variable
start = 'init'
lista = []

# *****************PRODUCCIONES ***********

def p_init(t):
    'init   : instrucciones'
    t[0] = t[1]

def p_instrucciones(t):
    'instrucciones  : instrucciones instruccion'
    if t[2] != None:
        t[1].append(t[2])
    t[0] = t[1]

def p_instrucciones_ins(t):
    'instrucciones  : instruccion'
    if t[1] == None:
        t[0] = []
    else:
        t[0] = [t[1]]

def p_instruccion(t):
    '''instruccion  : print ptcoma
                    | println ptcoma
                    | asignacion ptcoma
                    | condicional r_end ptcoma
                    | while r_end ptcoma
                    | for r_end ptcoma'''
    t[0] = t[1]

# Condicionales
def p_condicional_else(t):
    'condicional    : if r_else instrucciones'
    t[0] = CONDICION(t[1], t.lineno(1), column(input, t.slice[2]), t[3])

def p_condicional(t):
    'condicional    : if'
    t[0] = t[1]
 
  
def p_if(t):
    'if : r_if expresion instrucciones'
    t[0] = IF(t[2], t[3], t.lineno(1), column(input, t.slice[1]))
    
def p_if_elseif(t):
    'if : if r_elseif expresion instrucciones'
    t[0] = IF(t[3], t[4], t.lineno(1), column(input, t.slice[2]), t[1])

##impresiones
def p_print(t):
    'print  : r_print pizq parametro_print pder'
    t[0] = Imprimir(t[3], t.lineno(1), column(input, t.slice[1]))

#ciclos

def p_ins_while(t):
    'while : r_while expresion instrucciones'
    t[0] = WHILE(t[2], t[3], t.lineno(1), column(input, t.slice[1]))

def p_ins_for(t):
    'for : r_for id r_in expresion instrucciones'

#asignaciones 
def p_asignacion(t):
    '''asignacion : id igualT expresion'''
    t[0] = Asignacion(None, t.lineno(1), column(input, t.slice[2]),t[3], t[1])

def p_asignacionTipo(t):
    '''asignacion : id igualT expresion dospuntos dospuntos tipo'''
    t[0] = Asignacion(t[6], t.lineno(1), column(input, t.slice[2]),t[3], t[1])

#impresiones
def p_println(t):
    'println  : r_println pizq parametro_print pder'
    t[0] = ImprimirEnter(t[3], t.lineno(1), column(input, t.slice[1]))

def p_parametro_print(t):
    'parametro_print  : parametro_print coma expresion'
    if t[3] != None:
        t[1].append(t[3])
    t[0] = t[1]

def p_parametro_print_exp(t):
    'parametro_print    : expresion'
    if t[1] == None:
        t[0] = []
    else:
        t[0] = [t[1]]
#tipos
def p_tipo(t):
    '''tipo : r_int64
            | r_float64
            | r_stringT
            | r_bool
            | r_nothingT
            | r_char'''
    t[0] = Tipos(t[1].upper())

#nativas
def p_nativa(t):
    '''expresion : r_parse pizq tipo coma expresion pder
                 | r_trunc pizq tipo coma expresion pder
                 | r_log pizq expresion coma expresion pder
                 '''
    t[0] = Nativas(t.lineno(1), column(input, t.slice[6]), t[3], Tipos_Nativa(t[1].upper()),t[5])

def p_nativa_individual(t):
    '''expresion    : r_trunc pizq expresion pder
                    | r_float pizq expresion pder
                    | r_string pizq expresion pder
                    | r_typeof pizq expresion pder
                    | r_uppercase pizq expresion pder
                    | r_lowercase pizq expresion pder
                    | r_log10 pizq expresion pder
                    | r_sin pizq expresion pder
                    | r_cos pizq expresion pder
                    | r_tan pizq expresion pder
                    | r_sqrt pizq expresion pder'''    
    t[0] = Nativas(t.lineno(1), column(input, t.slice[4]), t[3], Tipos_Nativa(t[1].upper()))
    
#expresiones
def p_expresion(t):
    '''expresion : expresion suma expresion
                 | expresion resta expresion
                 | expresion mul expresion
                 | expresion div expresion
                 | expresion elevado expresion
                 | expresion modulo expresion
                 | expresion igual expresion
                 | expresion diferente expresion
                 | expresion mayor expresion
                 | expresion menor expresion
                 | expresion mayor_igual expresion
                 | expresion menor_igual expresion
                 | expresion and expresion
                 | expresion or expresion'''
    if t[2] == '+' or t[2] == '-' or t[2] == '*' or t[2] == '/' or t[2] == '%' or t[2] == '^':
        t[0] = Aritmetica(Aritmeticos(t[2]),t.lineno(1), column(input, t.slice[2]),t[1],t[3])
    elif t[2] == '==' or t[2] == '!=' or t[2] == '>' or t[2] == '>=' or t[2] == '<' or t[2] == '>=':
        t[0] = Relacional(Relacionales(t[2]),t.lineno(1), column(input, t.slice[2]),t[1],t[3])
    elif t[2] == '&&' or t[2] == '||':
        t[0] = Logica(Logicas(t[2]),t.lineno(1), column(input, t.slice[2]),t[1],t[3])

def p_expresion_unaria(t):
    '''expresion    :   resta expresion %prec UMENOS
                    |   not expresion'''
    if t[1] == '-':
        t[0] = Aritmetica(Aritmeticos(t[1]),t.lineno(1), column(input, t.slice[1]),t[2])
    else:
        t[0] = Logica(Logicas(t[1]),t.lineno(1), column(input, t.slice[1]),t[2])
        
def p_expresion_primitiva_int(t):
    'expresion    : int'
    t[0] = Primitivo(Tipos.ENTERO, t[1], t.lineno(1), column(input, t.slice[1]))

def p_expresion_primitiva_float(t):
    'expresion    : decimal'
    t[0] = Primitivo(Tipos.FLOAT, t[1], t.lineno(1), column(input, t.slice[1]))

def p_expresion_primitiva_char(t):
    'expresion    : char'
    t[0] = Primitivo(Tipos.CHAR, t[1], t.lineno(1), column(input, t.slice[1]))

def p_expresion_primitiva_string(t):
    'expresion    : string'    
    t[0] = Primitivo(Tipos.STRING, t[1], t.lineno(1), column(input, t.slice[1]))

def p_expresion_primitiva_bool(t):
    '''expresion    : r_false
                    | r_true'''
    if t[1]=='true':
        t[0] = Primitivo(Tipos.BOOL, True, t.lineno(1), column(input, t.slice[1]))
    else:
        t[0] = Primitivo(Tipos.BOOL, False, t.lineno(1), column(input, t.slice[1]))

def p_variable(t):
    '''expresion : id'''
    t[0] = Variable(t[1], t.lineno(1), column(input, t.slice[1]))

# Definicion de expresiones 
def p_agrupacion_expresion(t):
    'expresion : pizq expresion pder'
    t[0] = t[2]
    
###################################
def p_error(p):
    if p:
        errors.append(Error('Syntax',
                   f'error at token {p.value}', p.lineno,  column(input, p)))
        print(f'Syntax error at token {p.value}', p.lineno, p.lexpos)
        parser.errok()
    else:
        print("Syntax error at EOF")


from .PLY import yacc
parser = yacc.yacc()


input = ''

def get_errors():
    return errors


def parse(i):
    global to_parse
    to_parse = i
    return parser.parse(i)