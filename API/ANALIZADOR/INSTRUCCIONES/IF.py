# from ..INSTRUCCIONES.BREAK import BREAK
# from ..INSTRUCCIONES.CONTINUE import CONTINUE
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

class IF(Instruccion):

    def __init__(self, expresionIf, instrucionesIf,fila, columna, elseif=None):
        super().__init__(Tipos.NOTHING, fila, columna)
        self.ExpresionIf = expresionIf
        self.InstrucionesIf = instrucionesIf
        self.elseif = elseif
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
                    nuevo.auxiliar_type = x.auxiliar_type
                    nuevo.types = x.types
                    nuevo.struct_type = x.struct_type
                    aux_tabla[x.id] = nuevo
        
        if self.elseif is not None:
                self.elseif.els = self.els
                res = self.elseif.Ejecutar(arbol, tabla)
                if isinstance(res, Error):
                    generador.error_code() 
                    return res
                if isinstance(res, Retorno):
                    generador.set_unused_temp(res.value)
                self.exit = self.elseif.exit
        
        if not generador.in_function:
            tabla.variables = aux_tabla
        condicion = self.ExpresionIf.Ejecutar(arbol, tabla)
        if isinstance(condicion, Error):
            generador.error_code() 
            return condicion 
        if isinstance(condicion, Retorno):
            if self.ExpresionIf.type == Tipos.BOOL:
                if self.exit == "":
                    self.exit = generador.new_label()
                generador.place_label(condicion.true_tag)
                generador.set_anterior()    
                for ins in self.InstrucionesIf:
                    res = ins.Ejecutar(arbol, tabla)
                    if isinstance(res, Error):
                        generador.error_code()
                        arbol.errors.append(res)
                    if isinstance(res, Retorno):
                        generador.set_unused_temp(res.value)
                if self.els:
                    generador.place_goto(self.exit)
                generador.place_label(condicion.false_tag)
                generador.set_unused_temp(condicion.value)
                if condicion.valor and self.new_tabla == None and not generador.in_function:
                    self.new_tabla = {}
                    for x in list(tabla.variables.values()):
                        if isinstance(x, Simbolo):
                            nuevo = Simbolo(x.id, x.type, x.position, x.is_global, x.in_Heap)           
                            nuevo.value = x.value
                            nuevo.auxiliar_type = x.auxiliar_type
                            nuevo.types = x.types
                            nuevo.struct_type = x.struct_type
                            self.new_tabla[x.id] = nuevo
            else:
                generador.error_code()
                return Error("Semantico","La condición de la función if debe ser un booleano",self.fila, self.columna)
        if self.new_tabla is not None and not generador.in_function:
            tabla.variables = self.new_tabla
        
        generador.set_anterior()
        
        
    def getNodo(self) -> NodoAST:
        nodo = NodoAST('IF')
        if self.elseif is None:
            nodo.agregarHijo("if")
        else:
            nodo.agregarHijoNodo(self.elseif.getNodo())
            nodo.agregarHijo("elseif")
        nodo.agregarHijoNodo(self.ExpresionIf.getNodo())
        
        nodoInst = NodoAST('INSTRUCIONES')
        for ins in self.InstrucionesIf:
            inst = NodoAST("INSTRUCION")
            inst.agregarHijoNodo(ins.getNodo())
            nodoInst.agregarHijoNodo(inst)
        nodo.agregarHijoNodo(nodoInst)
        return nodo
        