from typing import Dict, List

from ..EXPRESIONES.variable_struct import Variable_Struct

from ..GENERAL.generator import Generador

from ..ABSTRACT.Retorno import Retorno
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.table import Tabla
from ..GENERAL.Tipo import Tipos
from ..GENERAL.error import Error
from ..GENERAL.Simbolo import Simbolo

class Asignar_Objeto(Instruccion):

    def __init__(self, variable, id, expresion, fila, columna):
        super().__init__(Tipos.STRING, fila, columna)
        self.variable:Instruccion = variable
        self.id = id
        self.expresion:Instruccion = expresion
        
    def Ejecutar(self, arbol: Arbol, tabla: Tabla):
        genAux = Generador()
        generador = genAux.get_instance()
        if isinstance(generador, Generador):
            expre = self.expresion.Ejecutar(arbol, tabla)
            if isinstance(expre, Error):
                generador.error_code()
                return expre
            valor:Retorno = self.variable.Ejecutar(arbol, tabla)
            if  isinstance(valor, Retorno):
                if self.variable.type != Tipos.OBJECT and type(self.variable.type) != type("") :
                    generador.error_code()
                    return Error("Sintactico", "Se esperaba una variable tipo Struct", self.row, self.column)
                if type(self.variable.type) == type(""):
                    dic:Simbolo = tabla.get_variable(self.variable.type)
                else:
                    dic:Simbolo = tabla.get_variable(self.variable.struct_type)
                dic:Dict = dic.value
                if not dic[2]:
                    generador.error_code()
                    return Error("Sintactico", "El objeto tipo struct indicado no es mutable", self.row, self.column)
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
                    exit = generador.new_label()
                    generador.place_if(valor.value, -1, "==", exit)
                    generador.place_operation(valor.value, valor.value, posicion, '+')
                    generador.insert_heap(valor.value, expre.value)
                    generador.place_label(exit)
                    
                    generador.set_unused_temp(valor.value)
                    if expre.is_temporal:
                        generador.set_unused_temp(expre.value)
                    generador.set_anterior()
                    return
                except:
                    generador.error_code()
                    return Error("Sintactico", "Error en la Asignacion de struct", self.row, self.column)
            else:
                generador.error_code()
                return valor

    def getNodo(self) -> NodoAST:
        nodo = NodoAST('PRINT')
        
        return nodo