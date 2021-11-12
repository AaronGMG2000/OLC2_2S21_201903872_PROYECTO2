from ..GENERAL.Tipo import Tipos
from ..GENERAL.Tipo import Aritmeticos

D_Aritmetica = {
    #UMENOS
    "-INT64":[Tipos.ENTERO,Aritmeticos.RESTA],
    "-FLOAT64":[Tipos.FLOAT, Aritmeticos.RESTA],
    #SUMA
    "INT64+INT64":[Tipos.ENTERO, Aritmeticos.SUMA],
    "INT64+FLOAT64":[Tipos.FLOAT, Aritmeticos.SUMA],
    "FLOAT64+INT64":[Tipos.FLOAT, Aritmeticos.SUMA],
    "FLOAT64+FLOAT64":[Tipos.FLOAT, Aritmeticos.SUMA],
    "STRING*STRING":[Tipos.STRING, Aritmeticos.SUMA],
    "STRING^INT64":[Tipos.STRING, Aritmeticos.MULTIPLICACION],
    #RESTA
    "INT64-INT64":[Tipos.ENTERO, Aritmeticos.RESTA],
    "INT64-FLOAT64":[Tipos.FLOAT, Aritmeticos.RESTA],
    "FLOAT64-INT64":[Tipos.FLOAT, Aritmeticos.RESTA],
    "FLOAT64-FLOAT64":[Tipos.FLOAT, Aritmeticos.RESTA],
    #multiplicacion
    "INT64*INT64":[Tipos.ENTERO, Aritmeticos.MULTIPLICACION],
    "INT64*FLOAT64":[Tipos.FLOAT, Aritmeticos.MULTIPLICACION],
    "FLOAT64*INT64":[Tipos.FLOAT, Aritmeticos.MULTIPLICACION],
    "FLOAT64*FLOAT64":[Tipos.FLOAT, Aritmeticos.MULTIPLICACION],
    #división
    "INT64/INT64":[Tipos.FLOAT, Aritmeticos.DIVISION],
    "INT64/FLOAT64":[Tipos.FLOAT, Aritmeticos.DIVISION],
    "FLOAT64/INT64":[Tipos.FLOAT, Aritmeticos.DIVISION],
    "FLOAT64/FLOAT64":[Tipos.FLOAT, Aritmeticos.DIVISION],
    #modulo
    "INT64%INT64":[Tipos.ENTERO, Aritmeticos.MODULO],
    "INT64%FLOAT64":[Tipos.FLOAT, Aritmeticos.MODULO],
    "FLOAT64%INT64":[Tipos.FLOAT, Aritmeticos.MODULO],
    "FLOAT64%FLOAT64":[Tipos.FLOAT, Aritmeticos.MODULO],
    #elevado
    "INT64^INT64":[Tipos.ENTERO, Aritmeticos.POTENCIA],
    "INT64^FLOAT64":[Tipos.FLOAT, Aritmeticos.POTENCIA],
    "FLOAT64^INT64":[Tipos.FLOAT, Aritmeticos.POTENCIA],
    "FLOAT64^FLOAT64":[Tipos.FLOAT, Aritmeticos.POTENCIA]
}

D_Relacional = {
    # ==
    "INT64==INT64": Tipos.BOOL,
    "FLOAT64==INT64": Tipos.BOOL,
    "FLOAT64==FLOAT64": Tipos.BOOL,
    "INT64==FLOAT64": Tipos.BOOL,
    
    "NOTHING==NOTHING": Tipos.BOOL,
    "RANGE==RANGE": Tipos.BOOL,
    "STRUCT==STRUCT": Tipos.BOOL,
    "ARRAY==ARRAY": Tipos.BOOL,
    "OBJECT==NOTHING": Tipos.BOOL,
    "OBJECT==OBJECT": Tipos.BOOL,
    
    "STRING==STRING": Tipos.BOOL,
    "BOOL==BOOL": Tipos.BOOL,
    # !=
    "INT64!=INT64": Tipos.BOOL,
    "FLOAT64!=INT64": Tipos.BOOL,
    "FLOAT64!=FLOAT64": Tipos.BOOL,
    "INT64!=FLOAT64": Tipos.BOOL,
    "STRING!=STRING": Tipos.BOOL,
    "BOOL!=BOOL": Tipos.BOOL,
    "NOTHING!=NOTHING": Tipos.BOOL,
    "RANGE!=RANGE": Tipos.BOOL,
    "STRUCT!=STRUCT": Tipos.BOOL,
    "ARRAY!=ARRAY": Tipos.BOOL,
    "OBJECT!=NOTHING": Tipos.BOOL,
    "OBJECT!=OBJECT": Tipos.BOOL,
    # >=
    "INT64>=INT64": Tipos.BOOL,
    "FLOAT64>=INT64": Tipos.BOOL,
    "FLOAT64>=FLOAT64": Tipos.BOOL,
    "INT64>=FLOAT64": Tipos.BOOL,
    "STRING>=STRING": Tipos.BOOL,
    "BOOL>=BOOL": Tipos.BOOL,
    # <=
    "INT64<=INT64": Tipos.BOOL,
    "FLOAT64<=INT64": Tipos.BOOL,
    "FLOAT64<=FLOAT64": Tipos.BOOL,
    "INT64<=FLOAT64": Tipos.BOOL,
    "STRING<=STRING": Tipos.BOOL,
    "BOOL<=BOOL": Tipos.BOOL,
    # >
    "INT64>INT64": Tipos.BOOL,
    "FLOAT64>INT64": Tipos.BOOL,
    "FLOAT64>FLOAT64": Tipos.BOOL,
    "INT64>FLOAT64": Tipos.BOOL,
    "STRING>STRING": Tipos.BOOL,
    "BOOL>BOOL": Tipos.BOOL,
    # <
    "INT64<INT64": Tipos.BOOL,
    "FLOAT64<INT64": Tipos.BOOL,
    "FLOAT64<FLOAT64": Tipos.BOOL,
    "INT64<FLOAT64": Tipos.BOOL,
    "STRING<STRING": Tipos.BOOL,
    "BOOL<BOOL": Tipos.BOOL
}

D_LOGICA = {
    'BOOL&&BOOL': 'and',
    'BOOL||BOOL': 'or',
    '!BOOL': 'not'
}


D_NATIVA = {
    #parse
    'PARSE-INT64-STRING':['int(valor.valor)', Tipos.ENTERO],
    'PARSE-FLOAT64-STRING':['float(valor.valor)', Tipos.FLOAT],
    #trunc
    'TRUNC-INT64-FLOAT64':['math.trunc(valor.valor)', Tipos.ENTERO],
    'TRUNC-FLOAT64':['float(math.trunc(valor.valor))', Tipos.ENTERO],
    #float
    'FLOAT-INT64':['float(valor.valor)', Tipos.FLOAT],
    #string
    'STRING-INT64':['str(valor.valor)',Tipos.STRING],
    'STRING-FLOAT64':['str(valor.valor)',Tipos.STRING],
    'STRING-BOOL':['str(valor.valor)',Tipos.STRING],
    'STRING-NOTHING':['str(valor.valor)',Tipos.STRING],
    'STRING-CHAR':['str(valor.valor)',Tipos.STRING],
    'STRING-ARREGLO':['str(valor.valor)',Tipos.STRING],
    'STRING-STRING':['str(valor.valor)',Tipos.STRING],
    'STRING-STRUCT':['str(valor.valor)',Tipos.STRING],
    'STRING-RANGE':['str(valor.valor)',Tipos.STRING],
    
    #uppercase y lowercase
    'UPPERCASE-STRING':['valor.valor.upper()',Tipos.STRING],
    'LOWERCASE-STRING':['valor.valor.lower()',Tipos.STRING],
    
    'LENGTH-ARREGLO':['0', Tipos.ENTERO]
}