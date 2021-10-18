# from ..INSTRUCCIONES.CONTINUE import CONTINUE
# from ..INSTRUCCIONES.BREAK import BREAK
# from ..INSTRUCCIONES.RETURN import RETURN
from typing import List

from ..GENERAL.Simbolo import Simbolo
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.table import Tabla
from ..GENERAL.Tipo import CICLICO, Tipos
from ..GENERAL.error import Error
from ..GENERAL.generator import Generador
from ..ABSTRACT.Retorno import Retorno

class CONDICION(Instruccion):

    def __init__(self, funcion_if,fila, columna, instrucionesElse=None):
        super().__init__(Tipos.NOTHING, fila, columna)
        self.funcion_if = funcion_if
        self.InstrucionesElse = instrucionesElse
        self.exit = ""
        self.new_tabla = None


    def Ejecutar(self, arbol: Arbol, tabla: Tabla):
        aux_tabla = {}
        for x in list(tabla.variables.values()):
            if isinstance(x, Simbolo):
                nuevo = Simbolo(x.id, x.type, x.position, x.is_global, x.in_Heap)
                nuevo.value = x.value
                aux_tabla[x.id] = nuevo
        genAux = Generador()
        generador = genAux.get_instance()
        res = self.funcion_if.Ejecutar(arbol, tabla)
        if isinstance(res, Error): 
            generador.error_code()
            return res
        self.new_tabla = self.funcion_if.new_tabla
        self.exit = self.funcion_if.exit        
        tabla.variables = aux_tabla
        if self.InstrucionesElse is not None:
            for ins in self.InstrucionesElse:
                res = ins.Ejecutar(arbol, tabla)
                if isinstance(res, Error):
                    arbol.errors.append(res)
            generador.place_label(self.exit)
            if self.new_tabla == None:
                self.new_tabla = {}
                for x in list(tabla.variables.values()):
                    if isinstance(x, Simbolo):
                        nuevo = Simbolo(x.id, x.type, x.position, x.is_global, x.in_Heap)
                        nuevo.value = x.value
                        self.new_tabla[x.id] = nuevo
        tabla.variables = self.new_tabla
        return True
                  
    def getNodo(self) -> NodoAST:
        nodo = NodoAST('IF')
        nodo.agregarHijoNodo(self.funcion_if.getNodo())
        nodo.agregarHijo("Else")
        nodoInst = NodoAST('INSTRUCIONES')
        for ins in self.InstrucionesElse:
            inst = NodoAST("INSTRUCCION")
            inst.agregarHijoNodo(ins.getNodo())
            nodoInst.agregarHijoNodo(inst)
        nodo.agregarHijoNodo(nodoInst)
        nodo.agregarHijo("end")
        nodo.agregarHijo(";")
        return nodo