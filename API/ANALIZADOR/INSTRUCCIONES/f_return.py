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

class RETURN(Instruccion):

    def __init__(self, fila, columna, expresion=None):
        super().__init__(CICLICO.RETURN, fila, columna)
        self.expresion = expresion
        
    def Ejecutar(self, arbol: Arbol, tabla: Tabla):
        genAux = Generador()
        generador = genAux.get_instance()
        if len(arbol.PilaFunc):
            if self.expresion is not None:
                valor = self.expresion.Ejecutar(arbol, tabla)
                if isinstance(valor, Error):
                    generador.error_code()
                    return valor
                pila = arbol.PilaFunc[-1]
                if valor.type == Tipos.BOOL:
                    if valor.is_temporal:
                        generador.insert_stack('P', valor.value)
                    else:
                        exit = generador.new_label()
                        generador.place_label(valor.true_tag)
                        generador.insert_stack('P', 1)
                        generador.place_goto(exit)
                        generador.place_label(valor.false_tag)
                        generador.insert_stack('P', 0)
                        generador.place_label(exit)
                else:
                    generador.insert_stack('P', valor.value)
                generador.set_unused_temp(valor.value)
                generador.place_goto(pila[2])
                generador.set_anterior()
                arbol.PilaFunc[-1] = [True, valor.valor, pila[2]]
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