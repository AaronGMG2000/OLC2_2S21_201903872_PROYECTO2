from ..GENERAL.Simbolo import Simbolo
from ..EXPRESIONES.variable import Variable
from typing import List
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.table import Tabla
from ..GENERAL.Tipo import CICLICO, Tipos
from ..GENERAL.error import Error
from ..GENERAL.generator import Generador
from ..ABSTRACT.Retorno import Retorno

class CONTINUE(Instruccion):

    def __init__(self, fila, columna, expresion=None):
        super().__init__(CICLICO.RETURN, fila, columna)
        self.expresion = expresion
        
    def Ejecutar(self, arbol: Arbol, tabla: Tabla):
        genAux = Generador()
        generador = genAux.get_instance()
        if len(arbol.PilaCiclo):
            arr = arbol.PilaCiclo[-1]
            generador.place_goto(arr[0])
            return
        generador.error_code()
        return Error("Sintactico","La funcion RETURN unicamente se puede usar en Funciones", self.row, self.column)

        
    def getNodo(self) -> NodoAST:
        nodo = NodoAST('RETURN')
        nodo.agregarHijo("return")
        if type(self.expresion)!=type(True):
            nodo.agregarHijoNodo(self.expresion.getNodo())
        nodo.agregarHijo(";")
        return nodo