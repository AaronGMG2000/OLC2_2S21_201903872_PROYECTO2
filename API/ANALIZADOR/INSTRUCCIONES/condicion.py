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
        self.els = False


    def Ejecutar(self, arbol: Arbol, tabla: Tabla):
        aux_tabla = {}
        genAux = Generador()
        generador = genAux.get_instance()
        if not generador.in_function:
            for x in list(tabla.variables.values()):
                if isinstance(x, Simbolo):
                    nuevo = Simbolo(x.id, x.type, x.position, x.is_global, x.in_Heap)
                    nuevo.value = x.value
                    nuevo.value = x.value
                    nuevo.auxiliar_type = x.auxiliar_type
                    nuevo.types = x.types
                    nuevo.struct_type = x.struct_type
                    aux_tabla[x.id] = nuevo
            
        if self.InstrucionesElse is not None:
            self.funcion_if.els = True
            self.els = True
        
        res = self.funcion_if.Ejecutar(arbol, tabla)
        if isinstance(res, Error): 
            generador.error_code()
            return res
        if isinstance(res, Retorno):
            generador.set_unused_temp(res)
        
        self.new_tabla = self.funcion_if.new_tabla
        self.exit = self.funcion_if.exit
        if not generador.in_function:        
            tabla.variables = aux_tabla
        if self.InstrucionesElse is not None:
            for ins in self.InstrucionesElse:
                res = ins.Ejecutar(arbol, tabla)
                if isinstance(res, Error):
                    generador.error_code()
                    arbol.errors.append(res)
                if isinstance(res, Retorno):
                    generador.set_unused_temp(res.value)
            generador.place_label(self.exit)
            if self.new_tabla == None and not generador.in_function:
                self.new_tabla = {}
                for x in list(tabla.variables.values()):
                    if isinstance(x, Simbolo):
                        nuevo = Simbolo(x.id, x.type, x.position, x.is_global, x.in_Heap)
                        nuevo.value = x.value
                        nuevo.value = x.value
                        nuevo.auxiliar_type = x.auxiliar_type
                        nuevo.types = x.types
                        nuevo.struct_type = x.struct_type
                        self.new_tabla[x.id] = nuevo
        if self.new_tabla is not None and not generador.in_function:
            tabla.variables = self.new_tabla
        generador.set_anterior()
        if isinstance(res, Simbolo):
            generador.set_unused_temp(res.value)
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