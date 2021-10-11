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
    # "INT64^FLOAT64":[Tipos.FLOAT, Aritmeticos.POTENCIA],
    "FLOAT64^INT64":[Tipos.FLOAT, Aritmeticos.POTENCIA],
    # "FLOAT64^FLOAT64":[Tipos.FLOAT, Aritmeticos.POTENCIA]
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
    'PARSE-INT64-STRING':['int(valor)', Tipos.ENTERO],
    'PARSE-FLOAT64-STRING':['float(valor)', Tipos.FLOAT],
    #trunc
    'TRUNC-INT64-FLOAT64':['math.trunc(valor)', Tipos.ENTERO],
    'TRUNC-FLOAT64':['float(math.trunc(valor))', Tipos.FLOAT],
    #float
    'FLOAT-INT64':['float(valor)', Tipos.FLOAT],
    #string
    'STRING-INT64':['str(valor)',Tipos.STRING],
    'STRING-FLOAT64':['str(valor)',Tipos.STRING],
    'STRING-BOOL':['str(valor)',Tipos.STRING],
    'STRING-NOTHING':['str(valor)',Tipos.STRING],
    'STRING-CHAR':['str(valor)',Tipos.STRING],
    'STRING-ARREGLO':['str(valor)',Tipos.STRING],
    'STRING-STRING':['str(valor)',Tipos.STRING],
    'STRING-STRUCT':['str(valor)',Tipos.STRING],
    
    #TYPEOF    
    'TYPEOF-INT64':['"Int64"',Tipos.STRING],
    'TYPEOF-FLOAT64':['"Float64"',Tipos.STRING],
    'TYPEOF-BOOL':['"Bool"',Tipos.STRING],
    'TYPEOF-NOTHING':['"NOTHING"',Tipos.STRING],
    'TYPEOF-CHAR':['"Char"',Tipos.STRING],
    'TYPEOF-ARREGLO':['"Arreglo"',Tipos.STRING],
    'TYPEOF-STRING':['"String"',Tipos.STRING],
    'TYPEOF-STRUCT':['"Struct"',Tipos.STRING],
    'TYPEOF-RANGO':['"Struct"',Tipos.RANGE],
    'TYPEOF-OBJECT':['"Struct"',Tipos.STRUCT],
    
    #uppercase y lowercase
    'UPPERCASE-STRING':['valor.upper()',Tipos.STRING],
    'LOWERCASE-STRING':['valor.lower()',Tipos.STRING],
    
    #NUMERICAS
    'LOG10-INT64':['math.log10(valor)',Tipos.FLOAT],
    'LOG10-FLOAT64':['math.log10(valor)',Tipos.FLOAT],
    'LOG-INT64-INT64' :['math.log(valor2, valor)',Tipos.FLOAT],
    'LOG-FLOAT64-INT64' :['math.log(valor2, valor)',Tipos.FLOAT],
    'LOG-INT64-FLOAT64' :['math.log(valor2, valor)',Tipos.FLOAT],
    'LOG-FLOAT64-FLOAT64' :['math.log(valor2, valor)',Tipos.FLOAT],
    'SIN-INT64' :['math.sin(valor)',Tipos.FLOAT],
    'SIN-FLOAT64' :['math.sin(valor)',Tipos.FLOAT],
    'COS-INT64':['math.cos(valor)',Tipos.FLOAT],
    'COS-FLOAT64':['math.cos(valor)',Tipos.FLOAT],
    'TAN-INT64':['math.tan(valor)',Tipos.FLOAT],
    'TAN-FLOAT64':['math.tan(valor)',Tipos.FLOAT],
    'SQRT-INT64':['math.sqrt(valor)',Tipos.FLOAT],
    'SQRT-FLOAT64':['math.sqrt(valor)',Tipos.FLOAT],
    #ARREGLOS
    'PUSH-ARREGLO':['h'],
    'POP-ARREGLO':['hh'],
    'LENGTH-ARREGLO':['hhh']
}