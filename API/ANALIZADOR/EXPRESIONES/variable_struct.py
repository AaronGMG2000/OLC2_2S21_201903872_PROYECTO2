from typing import Dict, List

from ..GENERAL.generator import Generador

from ..ABSTRACT.Retorno import Retorno
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.table import Tabla
from ..GENERAL.Tipo import Tipos
from ..GENERAL.error import Error
from ..GENERAL.Simbolo import Simbolo

class Variable_Struct(Instruccion):

    def __init__(self, variable, id, fila, columna):
        super().__init__(Tipos.STRING, fila, columna)
        self.variable:Instruccion = variable
        self.id = id
        
    def Ejecutar(self, arbol: Arbol, tabla: Tabla):
        genAux = Generador()
        generador = genAux.get_instance()
        if isinstance(generador, Generador):
            valor:Retorno = self.variable.Ejecutar(arbol, tabla)
            if  isinstance(valor, Retorno):
                if self.variable.type != Tipos.OBJECT:
                    return Error("Sintactico", "Se esperaba una variable tipo Struct", self.row, self.column)
                dic:Simbolo = tabla.get_variable(self.variable.struct_type)
                dic:Dict = dic.value
                try:
                    array = dic[self.id]
                    if type(array[0]) == type([]):
                        self.type = Tipos.ARRAY
                        self.types = array[0]
                    elif type(array[2]) == type([]) and array[0] == Tipos.ARRAY:
                        self.type = Tipos.ARRAY
                        self.types = array[2]
                    else:
                        self.type = array[0]
                    
                    self.struct_type = array[1]
                    posicion = array[3]
                    generador.place_operation(valor.value, valor.value, posicion, '+')
                    generador.get_heap(valor.value, valor.value)
                    ret = Retorno(valor.value, self.type, True)
                    ret.valor = valor.valor
                    if type(array[0]) == type([]) or array[0] == Tipos.ARRAY:
                        ret.types = self.types
                    else:
                        ret.types = valor.types
                        self.types = valor.types
                    ret.auxiliar_type = valor.auxiliar_type
                    if self.type == Tipos.OBJECT:
                        
                        ret.auxiliar_type = array[1]
                        if not valor.valor[self.id][4]:
                            ret.auxiliar_type = None
                            ret.types = []
                            ret.valor = -1
                            ret.type = Tipos.NOTHING
                            self.type = Tipos.NOTHING
                            self.types = []
                            self.struct_type = None
                        else:
                            ret.valor = valor.valor[self.id][4]
                    return ret
                except:
                    return Error("Sintactico", "Error en el Struct", self.row, self.column)
            else:
                return valor

    def getNodo(self) -> NodoAST:
        nodo = NodoAST('PRINT')
        
        return nodo