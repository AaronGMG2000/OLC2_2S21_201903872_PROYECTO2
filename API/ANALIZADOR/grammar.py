reservadas = {
    "print": "r_print",
    "println": "r_println",
    "true": "r_true",
    "false": "r_false",
    "parse": "r_parse",
    "trunc": "r_trunc",
    "float": "r_float",
    "function": "r_function",
    "string": "r_string",
    "String": "r_stringT",
    "nothing": "r_nothing",
    "Nothing": "r_nothingT",
    "struct" : "r_struct",
    "mutable": "r_mutable",
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
    "in": "r_in",
    "return": "r_return",
    "break": "r_break",
    "continue": "r_continue",  
     "global" : "r_global",
     "local" : "r_local", 
     "length": "r_length",
     "push" : "r_push",
     "pop" : "r_pop",
}

tokens = [
    "punto",
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
    "cizq",
    "cder",
] + list(reservadas.values())
#t_token
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
t_punto               = r'\.'
t_coma               = r','
t_ptcoma             = r';'
t_dospuntos          = r':'
t_pizq               = r'\('
t_pder               = r'\)'
t_igualT             = r'='
t_cizq               = r'\['
t_cder               = r'\]'
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
    errors.append(Error("Lexical", f"This is illegal token {t.value[0]}", t.lexer.lineno, col(t)))
    t.lexer.skip(1)


def col(token):
    return (token.lexpos - (to_parse.rfind('\n', 0, token.lexpos) + 1)) + 1


from .PLY import lex
lexer = lex.lex()


errors = []


# precedencias 
precedence = (
    # ('left', 'TERNARIO'),
    ('left', 'or'),
    ('left', 'and'),
    ('right', 'nnot'),
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
from .EXPRESIONES.Logico import Logico
from .EXPRESIONES.Relacional import Relacional
from .GENERAL.error import Error
from .INSTRUCCIONES.f_for import FOR
from .INSTRUCCIONES.f_while import WHILE
from .INSTRUCCIONES.print import Imprimir
from .INSTRUCCIONES.Asignar_Array import Asignar_Array
from .INSTRUCCIONES.Asignacion_Variable import Asignar_Variable
from .GENERAL.Tipo import Logicas, Relacionales, Tipos, Tipos_Nativa
from .EXPRESIONES.variable_array import Variable_Array
from .GENERAL.Tipo import Aritmeticos
from .EXPRESIONES.variable import Variable
from .EXPRESIONES.primitivo import Primitivo
from .EXPRESIONES.Aritmetica import Aritmetica
from .EXPRESIONES.Nativa import Nativas
from .EXPRESIONES.Rango import Rango
from .INSTRUCCIONES.IF import IF
from .INSTRUCCIONES.condicion import CONDICION
from .EXPRESIONES.Array import ARRAY

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
                    | whilee r_end ptcoma
                    | forr r_end ptcoma
                    | struct ptcoma
                    | funtionn r_end ptcoma
                    | llamada ptcoma
                    | array ptcoma
                    | BREAKk ptcoma
                    | RETURNN ptcoma
                    | CONTINUEE ptcoma
                    | GLOBAL ptcoma
                    | LOCAL ptcoma
                    | PUSHH ptcoma
                    | POPP ptcoma
                    | LENGHTT ptcoma'''
    t[0] = t[1]

#push, pop, lenght

def p_pushh(t):
    '''PUSHH : r_push not pizq expresion coma expresion pder'''

def p_popp(t):
    '''POPP : r_pop not pizq expresion pder'''
    
def p_lengthh(t):
    '''LENGHTT : r_length pizq expresion pder'''

#Global y Local
def p_global(t):
    '''GLOBAL : r_global id'''

def p_global_exp(t):
    '''GLOBAL : r_global id igualT expresion'''

def p_global_tipo(t):
    '''GLOBAL : r_global id igualT expresion dospuntos dospuntos tipo'''

def p_global_tipo_id(t):
    '''GLOBAL : r_global id igualT expresion dospuntos dospuntos id'''

def p_local(t):
    '''LOCAL : r_local id'''
    
def p_local_exp(t):
    '''LOCAL : r_local id igualT expresion'''

def p_local_tipo(t):
    '''LOCAL : r_local id igualT expresion dospuntos dospuntos tipo'''
    
def p_local_tipo_id(t):
    '''LOCAL : r_local id igualT expresion dospuntos dospuntos id'''
    
# Condicionales
def p_condicional_else(t):
    'condicional    : if r_else instrucciones'
    t[0] = CONDICION(t[1], t.lineno(1), col(t.slice[2]), t[3])

def p_if(t):
    'if : r_if expresion instrucciones'
    t[0] = IF(t[2], t[3], t.lineno(1), col(t.slice[1]))

def p_if_elseif(t):
    'if : if r_elseif expresion instrucciones'
    t[0] = IF(t[3], t[4], t.lineno(1), col(t.slice[2]), t[1])
    
def p_condicional(t):
    'condicional    : if'
    t[0] = t[1]
 
def p_break(t):
    '''BREAKk : r_break'''

def p_continue(t):
    '''CONTINUEE : r_continue'''

def p_return(t):
    '''RETURNN : r_return'''

def p_return_expresion(t):
    '''RETURNN : r_return expresion'''

  




#ciclos


def p_ins_while(t):
    'whilee : r_while expresion instrucciones'
    t[0] = WHILE(t[2], t[3], t.lineno(1), col(t.slice[1]))
    
def p_ins_for(t):
    'forr : r_for id r_in expresion instrucciones'
    t[0] = FOR(t[2], t[4],t[5],t.lineno(1), col(t.slice[1]))
    
#asignaciones 
def p_asignacion(t):
    '''asignacion : id igualT expresion'''
    t[0] = Asignar_Variable(t[1], t[3], t.lineno(1), col(t.slice[1]))
def p_asignacionTipo(t):
    '''asignacion : id igualT expresion dospuntos dospuntos tipo'''
    t[0] = Asignar_Variable(t[1], t[3], t.lineno(1), col(t.slice[1]), t[6])
    
def p_asignacionTipo_id(t):
    '''asignacion : id igualT expresion dospuntos dospuntos id'''
    t[0] = Asignar_Variable(t[1], t[3], t.lineno(1), col(t.slice[1]), t[6])

#ASIGNACION ARRAY
#Arrays
def p_asignacion_array_struct(t):
    '''array : id number_array lista_id igualT expresion'''

def p_asignacion_array(t):
    '''array : id number_array igualT expresion'''
    t[0] = Asignar_Array(t[1], t[2], t[4], t.lineno(1), col(t.slice[1]))
    
#Asignacion STRUCT
def p_asignacion_STRUCT_variable(t):
    '''asignacion : id lista_id igualT expresion'''

def p_lista_id(t):
    '''lista_id : lista_id punto id'''
    if t[3] != None:
        t[1].append([t[3], None])
    t[0] = t[1]
    
def p_lista_id_array(t):
    '''lista_id : lista_id punto id number_array'''
    if t[3] != None:
        t[1].append([t[3], t[4]])
    t[0] = t[1]
    
def p_lista_id_u(t):
    '''lista_id : punto id'''
    if t[2] == None:
        t[0] = []
    else:
        t[0] = [[t[2], None]]

def p_lista_id_u_lista(t):
    '''lista_id : punto id number_array'''
    if t[2] == None:
        t[0] = []
    else:
        t[0] = [[t[2], t[3]]]
        
def p_llamada(t):
    '''llamada : id pizq parametro_print pder '''

def p_llamada_Solo(t):
    '''llamada : id pizq pder '''
#function

def p_function(t):
    '''funtionn : r_function id pizq pder instrucciones'''

def p_function_parametro(t):
    '''funtionn : r_function id pizq parametros_function pder instrucciones'''
    
def p_parametros_function(t):
    '''parametros_function : parametros_function coma id'''
    if t[3] != None:
        t[1].append([t[3], Tipos.NOTHING])
    t[0] = t[1]
    
def p_parametros_function2(t):
    '''parametros_function : parametros_function coma id dospuntos dospuntos tipo'''
    if t[3] != None:
        t[1].append([t[3], t[6]])
    t[0] = t[1]
    
def p_parametros_function2_id(t):
    '''parametros_function : parametros_function coma id dospuntos dospuntos id'''
    if t[3] != None:
        t[1].append([t[3], Tipos.OBJECT])
    t[0] = t[1]
    
def p_parametros_function_unico(t):
    '''parametros_function : id'''
    if t[1] == None:
        t[0] = []
    else:
        t[0] = [[t[1], Tipos.NOTHING]]
    
    
def p_parametros_function_tipo(t):
    '''parametros_function : id dospuntos dospuntos tipo'''
    if t[1] == None:
        t[0] = []
    else:
        t[0] = [[t[1], t[4]]]
def p_parametros_function_tipo_id(t):
    '''parametros_function : id dospuntos dospuntos id'''
    if t[1] == None:
        t[0] = []
    else:
        t[0] = [[t[1], Tipos.OBJECT]]

#Structs

def p_struct(t):
    '''struct : r_struct id parametros_struct r_end'''

def p_mutable_struct(t):
    '''struct : r_mutable r_struct id parametros_struct r_end'''
    
def p_parametros_struct(t):
    '''parametros_struct : parametros_struct parametro_struct'''
    if t[2] != None:
        t[1].append(t[2])
    t[0] = t[1]

def p_parametros_struct_unico(t):
    '''parametros_struct : parametro_struct'''
    if t[1] == None:
        t[0] = []
    else:
        t[0] = [t[1]]

def p_parametro_struct_nulo(t):
    '''parametro_struct : id ptcoma'''
    if t[1] == None:
        t[0] = []
    else:
        t[0] = [t[1],None]
        
def p_parametro_struct(t):
    '''parametro_struct : id dospuntos dospuntos tipo ptcoma'''
    if t[1] == None:
        t[0] = []
    else:
        t[0] = [t[1], t[4]]
        
def p_parametro_struct_id(t):
    '''parametro_struct : id dospuntos dospuntos id ptcoma'''
    if t[1] == None:
        t[0] = []
    else:
        t[0] = [t[1], Tipos.OBJECT]

#impresiones
##impresiones
def p_print(t):
    'print  : r_print pizq parametro_print pder'
    t[0] = Imprimir(t[3], False, t.lineno(1), col(t.slice[1]))
    
def p_println(t):
    'println  : r_println pizq parametro_print pder'
    t[0] = Imprimir(t[3], True, t.lineno(1), col(t.slice[1]))

def p_print_v(t):
    'print  : r_print pizq pder'
    t[0] = Imprimir([], False, t.lineno(1), col(t.slice[1]))
    
def p_println_v(t):
    'println  : r_println pizq pder'
    t[0] = Imprimir([], True, t.lineno(1), col(t.slice[1]))

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

#Struct Exp
def p_variable(t):
    '''expresion : exp_struct'''
    t[0] = t[1]

def p_Expresion_Struct(t):
    '''exp_struct : exp_struct punto id'''


def p_Expresion_Struct_lista(t):
    '''exp_struct : exp_struct punto id number_array''' 
    

def p_expresion_struct_id(t):
    '''exp_struct : id'''
    t[0] = Variable(t[1], t.lineno(1), col(t.slice[1]))
#Arrays
#id array
def p_expresion_array_id(t):
    '''exp_struct : id number_array'''
    t[0] = Variable_Array(t[1], t[2], t.lineno(1), col(t.slice[1]))
#number array

def p_expresion_id_content_unico(t):
    '''number_array : cizq expresion cder'''
    if t[2] == None:
        t[0] = []
    else:
        t[0] = [t[2]]
        
def p_expresion_id_content(t):
    '''number_array : number_array cizq expresion cder'''
    if t[3] != None:
        t[1].append(t[3])
    t[0] = t[1]

#Expresion_Array
def p_expresion_Array(t):
    '''expresion : cizq expresion_exp cder'''
    t[0] = ARRAY(t[2], t.lineno(1), col(t.slice[1]))
    
def p_coma_expresion(t):
    '''expresion_exp : expresion_exp coma expresion'''
    if t[3] != None:
        t[1].append(t[3])
    t[0] = t[1]
    
def p_coma_expresion_unico(t):
    '''expresion_exp : expresion'''
    if t[1] == None:
        t[0] = []
    else:
        t[0] = [t[1]]
        
    
        
#Llamada EXP



def p_expresion_llamada(t):
    '''expresion : id pizq parametro_print pder'''
#nativas
def p_nativa(t):
    '''expresion : r_parse pizq tipo coma expresion pder
                 | r_trunc pizq tipo coma expresion pder
                 '''

    
def p_length_expresion(t):
    '''expresion : r_length pizq expresion pder'''

def p_nativa_individual(t):
    '''expresion    : r_trunc pizq expresion pder
                    | r_float pizq expresion pder
                    | r_string pizq expresion pder
                    | r_uppercase pizq expresion pder
                    | r_lowercase pizq expresion pder'''    
    t[0] = Nativas(t.lineno(1), col(t.slice[4]), t[3], Tipos_Nativa(t[1].upper()))  
#Expresion Rango
def p_expresion_rango(t):
    '''expresion : expresion dospuntos expresion'''
    t[0] = Rango(t[1], t[3], t.lineno(1), col(t.slice[2]))
#Expresion Rango completo
def p_expresion_rango_Todo(t):
    '''expresion : dospuntos'''
    t[0] = Rango(None, None, t.lineno(1), col(t.slice[1]))
    
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
        t[0] = Aritmetica(Aritmeticos(t[2]),t.lineno(1), col(t.slice[2]),t[1],t[3])
    elif t[2] == '==' or t[2] == '!=' or t[2] == '>' or t[2] == '>=' or t[2] == '<' or t[2] == '<=':
        t[0] = Relacional(Relacionales(t[2]),t.lineno(1), col(t.slice[2]),t[1],t[3])
    elif t[2] == '&&' or t[2] == '||':
        t[0] = Logico(Logicas(t[2]),t.lineno(1), col(t.slice[2]),t[1],t[3])

def p_expresion_unaria(t):
    '''expresion    :   resta expresion %prec UMENOS
                    |   not expresion %prec nnot'''
    if t[1] == '-':
        t[0] = Aritmetica(Aritmeticos(t[1]),t.lineno(1), col(t.slice[1]),t[2])
    else:
        t[0] = Logico(Logicas(t[1]),t.lineno(1), col(t.slice[1]),t[2])


   
def p_expresion_primitiva_int(t):
    'expresion    : int'
    t[0] = Primitivo(Tipos.ENTERO, t[1], t.lineno(1), col(t.slice[1]))

def p_expresion_primitiva_float(t):
    'expresion    : decimal'
    t[0] = Primitivo(Tipos.FLOAT, t[1], t.lineno(1), col(t.slice[1]))

def p_expresion_primitiva_char(t):
    'expresion    : char'
    t[0] = Primitivo(Tipos.CHAR, t[1], t.lineno(1), col(t.slice[1]))

def p_expresion_primitiva_string(t):
    'expresion    : string'    
    t[0] = Primitivo(Tipos.STRING, t[1], t.lineno(1), col(t.slice[1]))

def p_expresion_primitiva_bool(t):
    '''expresion    : r_false
                    | r_true'''
    if t[1]=='true':
        t[0] = Primitivo(Tipos.BOOL, True, t.lineno(1), col(t.slice[1]))
    else:
        t[0] = Primitivo(Tipos.BOOL, False, t.lineno(1), col(t.slice[1]))

def p_expresion_primitiva_nothing(t):
    '''expresion : r_nothing'''
    t[0] = Primitivo(Tipos.NOTHING, "nothing", t.lineno(1), col(t.slice[1]))

# def p_variable(t):
#     '''expresion : id'''
#     t[0] = Variable(t[1], t.lineno(1), col(t.slice[1]))

# Definicion de expresiones 
def p_agrupacion_expresion(t):
    'expresion : pizq expresion pder'
    t[0] = t[2]
    
###################################
def p_error(p):
    if p:
        errors.append(Error('Syntax',
                   f'error at token {p.value}', p.lineno,  col(p)))
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
    lexer.lineno = 1
    return parser.parse(i)