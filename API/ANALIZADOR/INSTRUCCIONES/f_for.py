# from ..INSTRUCCIONES.BREAK import BREAK
# from ..INSTRUCCIONES.CONTINUE import CONTINUE
# from ..GENERAL.Lista_Simbolo import Lista_Simbolo
# from ..INSTRUCCIONES.RETURN import RETURN
import re

from ..GENERAL.generator import Generador

from ..ABSTRACT.Retorno import Retorno
from ..GENERAL.Simbolo import Simbolo
from ..EXPRESIONES.variable import Variable
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.table import Tabla
from ..GENERAL.Tipo import CICLICO, Tipos
from ..GENERAL.error import Error

class FOR(Instruccion):

    def __init__(self, id, expresion, instruciones,fila, columna):
        super().__init__(Tipos.NOTHING, fila, columna)
        self.id = id
        self.expresion = expresion
        self.instruciones = instruciones

    def Ejecutar(self, arbol: Arbol, tabla: Tabla):
        genAux = Generador()
        generador = genAux.get_instance()
        variable = tabla.get_variable(self.id)
        tip = None
        ciclo = self.expresion.Ejecutar(arbol, tabla)
        if isinstance(ciclo, Error):
            generador.error_code()
            return ciclo
        if isinstance(ciclo, Retorno):
            types = None
            aux = None
            if self.expresion.type == Tipos.STRING:
                tip = Tipos.CHAR
            elif self.expresion.type == Tipos.ARRAY:
                types = ciclo.types
                heap = generador.new_temporal()
                size = generador.new_temporal()
                generador.get_heap(heap, ciclo.value)
                generador.place_operation(size, heap, ciclo.value, '+')
                generador.set_unused_temp(heap)
                posicion = generador.new_temporal()
                generador.place_operation(posicion,ciclo.value,  1, '+')
                if type(types[0]) == type([]):
                    tip = Tipos.ARRAY
                    types = ciclo.types[0]
                else:
                    tip = types[0]
            elif self.expresion.type == Tipos.RANGE:
                tip = ciclo.auxiliar_type
                aux = ciclo.auxiliar_type
                t1 = generador.new_temporal()
                t2 = generador.new_temporal()
                generador.get_heap(t1, ciclo.value)
                generador.place_operation(ciclo.value, ciclo.value, 1, '+')
                generador.get_heap(t2, ciclo.value)
                generador.set_unused_temp(ciclo.value)
            elif self.expresion.type == Tipos.ENTERO or self.expresion.type == Tipos.FLOAT:
                tip = self.expresion.type
                t1 = generador.new_temporal()
                t2 = generador.new_temporal()
                generador.place_operation(t1, ciclo.value, '','')
                generador.place_operation(t2, ciclo.value, '','')
            else:
                generador.error_code()
                return Error("Semantico","El for no puede efectuarse con el tipo "+str(self.expresion.tipo.value), self.fila, self.columna)
            nuevaTabla = Tabla(tabla, "FOR")
            var:Simbolo = None
            if variable == None:
                nuevaTabla.set_variable(self.id, tip, False)
                var = nuevaTabla.get_variable(self.id)
                var.types = types
            else:
                nuevaTabla.set_variable(variable.id, variable.type, variable.in_Heap)
                var = nuevaTabla.get_variable(variable.id)
                var.auxiliar_type = variable.auxiliar_type
                var.types = ciclo.types
            pos_temp = generador.new_temporal()
            if len(arbol.function)>0:
                generador.place_operation(pos_temp, 'P', var.position-tabla.previous.size, '+')
            else:
                generador.place_operation(pos_temp, 'P', var.position, '+')
            w = generador.new_label()
            true_tag = generador.new_label()
            generador.place_label(w)
            
            
            if types != None:
                generador.place_if(posicion, size, '>', true_tag)
                tempo = generador.new_temporal()
                generador.get_heap(tempo, posicion)
                generador.insert_stack(pos_temp, tempo)
            elif aux != None:
                generador.place_if(t1, t2, '>', true_tag)
                generador.insert_stack(pos_temp, t1)
            elif tip == Tipos.CHAR:
                heap = generador.new_temporal()
                generador.get_heap(heap, ciclo.value)
                generador.place_if(heap, -1, '==', true_tag)
                generador.insert_stack(pos_temp, heap)
                generador.set_unused_temp(heap)
            else:
                generador.place_if(t1, t2, '>', true_tag)
                generador.insert_stack(pos_temp, t1)
            
            #for-------------------------
            for ins in self.instruciones:
                res = ins.Ejecutar(arbol, nuevaTabla)
                if isinstance(res, Error):
                    arbol.errors.append(res)
            ####
            if types != None:
                generador.place_operation(posicion, posicion, 1, '+')
                generador.set_unused_temp(ciclo.value)
                generador.set_unused_temp(size)
                generador.set_unused_temp(tempo)
                generador.set_unused_temp(posicion)
            elif aux != None:
                generador.place_operation(t1, t1, 1, '+')
                generador.set_unused_temp(t1)
                generador.set_unused_temp(t2)
            elif tip == Tipos.CHAR:
                generador.place_operation(ciclo.value, ciclo.value, 1,'+')
                generador.set_unused_temp(ciclo.value)
            else:
                generador.place_operation(t1, t1, 1, '+')
                generador.set_unused_temp(t1)
                generador.set_unused_temp(t2)
            ###
            generador.set_unused_temp(pos_temp)
            generador.place_goto(w)
            generador.place_label(true_tag)
            generador.set_anterior()
            return True
        
    def getNodo(self) -> NodoAST:
        nodo = NodoAST('FOR')
        nodo.agregarHijo(self.id)
        nodo.agregarHijoNodo(self.expresion.getNodo())
        inst = NodoAST('INSTRUCCIONES')
        for ins in self.instruciones:
            insts = NodoAST("INSTRUCCION")
            insts.agregarHijoNodo(ins.getNodo())
            inst.agregarHijoNodo(insts)
        nodo.agregarHijoNodo(inst)
        return nodo