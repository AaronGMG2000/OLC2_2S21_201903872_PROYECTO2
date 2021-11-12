from .instructions.asignacion import Asignacion
from .instructions.etiqueta import Etiqueta
from .instructions.funcion import Funcion
from .instructions.goto import Goto
from .instructions.I_IF import If
from .instructions.I_FUNCION import LlamadaFuncion
from .instructions.I_RETURN import Return
from .Expresiones.acceso import Acceso
from .Expresiones.expresion import Expresion
from .Expresiones.literal import Literal
from .Abstract.optimizador import Optimizador
from .instructions.f_print import Imprimir

rw = {
    "float64": "FLOAT64",
    "int": "INT",
    "func": "FUNC",
    "return": "RETURN",
    "if": "IF",
    "goto" : "GOTO",
    "fmt": "FMT",
    "Printf": "PRINTF",
    "package": "PACKAGE",
    "import": "IMPORT",
    "var": "VAR",
    "math": "MATH",
    "Mod": "MOD"
}

tokens = [
    "ID",
    "INTLITERAL",
    "FLOATLITERAL",
    "STRINGLITERAL",

    "MULTI",
    "DIV",
    "PLUS",
    "MINUS",


    "GREATER",
    "LESS",
    "GREATEREQUAL",
    "LESSEQUAL",
    "EQUALSEQUALS",
    "DISTINT",

    "EQUALS",
    "PTCOMA",
    "COLON",
    "PUNTO",

    "LIZQ",
    "LDER",

    "PIZQ",
    "PDER",

    "CIZQ",
    "CDER",

    "COMMA"
] + list(rw.values())

t_MULTI                 = r'\*'
t_DIV                   = r'/'
t_PLUS                  = r'\+'
t_MINUS                 = r'-'

t_GREATER               = r'>'
t_LESS                  = r'<'
t_GREATEREQUAL          = r'>='
t_LESSEQUAL             = r'<='
t_EQUALSEQUALS          = r'=='
t_DISTINT               = r'!='

t_EQUALS                = r'='
t_PTCOMA             = r';'
t_COLON                 = r':'
t_PUNTO                 = r'\.'

t_LIZQ                 = r'{'
t_LDER                 = r'}'

t_PIZQ                 = r'\('
t_PDER                 = r'\)'

t_CIZQ                = r'\['
t_CDER                 = r'\]'

t_COMMA                 = r','

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = rw.get(t.value, 'ID')
    return t

def t_FLOATLITERAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("ERROR IN PARSE TO FLOAT")
        t.value = 0
    return t

def t_INTLITERAL(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("ERROR IN PARSE TO INT")
        t.value = 0
    return t

def t_STRINGLITERAL(t):
    r'\".*?\"'
    t.value = t.value[1:-1]
    return t

t_ignore = " \t"

def t_MLCOMMENT(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count("\n")

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

from .ply import lex
lexer1 = lex.lex()


def p_start(t):
    '''start :  PACKAGE ID PTCOMA IMPORT PIZQ IMPORTS PDER PTCOMA declarations codeList'''
    t[0] = Optimizador(t[6], t[9], t[10])

def p_imports(t):
    '''IMPORTS : STRINGLITERAL
               | STRINGLITERAL PTCOMA STRINGLITERAL PTCOMA'''
    if len(t) > 2:
        t[0] = [t[1], t[3]]
    else:
        t[0] = [t[1]]

def p_declarations(t):
    '''declarations : declarations declaration
                    | declaration'''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[1].append(t[2])
        t[0] = t[1]

def p_declaration(t):
    '''declaration :    VAR idList CIZQ INTLITERAL CDER FLOAT64 PTCOMA
                    |   VAR idList type PTCOMA'''
    if len(t) == 5:
        t[0] = f'{t[2]} {t[3]};'
    else:
        t[0] = f'{t[2]}[{t[4]}] float64;'

def p_type(t):
    '''type : INT
            | FLOAT64'''
    if t[1] == "int":
        t[0] = "int"
    else:
        t[0] = "float64"

def p_idList(t):
    '''idList :   idList COMMA ID
                | ID'''
    if len(t) == 2:
        t[0] = f'{t[1]}'
    else:
        t[0] = f'{t[1]}, {t[3]}'

def p_codeList(t):
    '''codeList : codeList code
                | code'''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[1].append(t[2])
        t[0] = t[1]

def p_code(t):
    'code : FUNC ID PIZQ PDER statement'
    t[0] = Funcion(t[5], t[2], t.lineno(1), col(t.slice[1]))


def p_statement(t):
    '''statement : LIZQ instructions LDER'''
    t[0] = t[2]


def p_instructions(t):
    '''instructions : instructions instruction
                    | instruction'''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[1].append(t[2])
        t[0] = t[1]

def p_instruction(t):
    '''instruction :  assign PTCOMA
                    | print PTCOMA
                    | if
                    | gotoSt PTCOMA
                    | label
                    | callFunc PTCOMA
                    | retSt PTCOMA'''
    t[0] = t[1]

def p_return(t):
    'retSt : RETURN'
    t[0] = Return(t.lineno(1), col(t.slice[1]))


def p_callFunc(t):
    'callFunc : ID PIZQ PDER'
    t[0] = LlamadaFuncion(t[1], t.lineno(2), col(t.slice[2]))

def p_label(t):
    'label : ID COLON'
    t[0] = Etiqueta(t[1], t.lineno(2), col(t.slice[2]))

def p_goto(t):
    'gotoSt : GOTO ID'
    t[0] = Goto(t[2], t.lineno(1), col(t.slice[1]))

def p_if(t):
    'if : IF expression LIZQ GOTO ID PTCOMA LDER'
    t[0] = If(t[2], t[5], t.lineno(1), col(t.slice[1]))

def p_assign(t):
    'assign : access EQUALS finalExp'
    t[0] = Asignacion(t[1], t[3], t.lineno(2), col(t.slice[2]))

def p_assign2(t):
    '''assign :   ID EQUALS expression
                | ID EQUALS access'''
    n = Literal(t[1], t.lineno(1), col(t.slice[1]))
    t[0] = Asignacion(n, t[3], t.lineno(2), col(t.slice[2]))

def p_print(t):
    'print : FMT PUNTO PRINTF PIZQ STRINGLITERAL COMMA printValue PDER'
    t[0] = Imprimir(t[5], t[7], t.lineno(1), col(t.slice[1]))

def p_printValue(t):
    '''printValue :   INT PIZQ finalExp PDER
                    | finalExp'''
    if len(t) == 2:
        t[0] = t[1]
    else:
        t[3].const = True
        t[0] = t[3]

def p_expression(t):
    '''expression :   finalExp PLUS finalExp
                    | finalExp MINUS finalExp
                    | finalExp MULTI finalExp
                    | finalExp DIV finalExp
                    | finalExp GREATER finalExp
                    | finalExp LESS finalExp
                    | finalExp GREATEREQUAL finalExp
                    | finalExp LESSEQUAL finalExp
                    | finalExp EQUALSEQUALS finalExp
                    | finalExp DISTINT finalExp
                    | MATH PUNTO MOD PIZQ finalExp COMMA finalExp PDER
                    | finalExp'''
    if len(t) == 2:
        t[0] = t[1]
    elif len(t) == 9:
        t[0] = Expresion(t[5], t[7], '%', t.lineno(2), col(t.slice[2]))
    else:
        t[0] = Expresion(t[1], t[3], t[2], t.lineno(2), col(t.slice[2]))


def col(token):
    return (token.lexpos - (to_parse.rfind('\n', 0, token.lexpos) + 1)) + 1

def p_finalExp(t):
    '''finalExp : ID
                | INTLITERAL
                | MINUS INTLITERAL
                | FLOATLITERAL'''
    if len(t) == 3:
        t[0] = Literal(0-t[2], t.lineno(1), col(t.slice[1]))
    else:
        t[0] = Literal(t[1], t.lineno(1), col(t.slice[1]))


def p_access(t):
    '''access :   ID CIZQ INT PIZQ finalExp PDER CDER
                | ID CIZQ finalExp CDER'''
    if len(t) == 5:
        t[0] = Acceso(t[1], t[3], t.lineno(2), col(t.slice[2]))
    else:
        t[0] = Acceso(t[1], t[5], t.lineno(2), col(t.slice[2]))
        t[0].const = True


def p_error(t):
    print(t)
    print("Syntactic error in '%s'" % t.value)

from .ply import yacc
parser2 = yacc.yacc()

def parse(input):
    global to_parse
    lexer1.lineno = 1
    to_parse = input
    return parser2.parse(input, lexer=lexer1)
