from typing import List

from starlette.routing import get_name

from ..GENERAL.generator import Generador

from ..ABSTRACT.Retorno import Retorno
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.table import Tabla
from ..GENERAL.Tipo import Tipos
from ..GENERAL.error import Error
from ..GENERAL.Simbolo import Simbolo

class Variable_Array(Instruccion):

    def __init__(self, id, numbers:List, fila, columna):
        super().__init__(Tipos.ARRAY, fila, columna)
        self.id = id
        self.numbers:List = numbers
        self.types = []
        
    def Ejecutar(self, arbol: Arbol, tabla: Tabla):
        genAux = Generador()
        generador = genAux.get_instance()
        if isinstance(generador, Generador):
            valor = tabla.get_variable(self.id)
            if  isinstance(valor, Simbolo):
                if valor.type!= Tipos.ARRAY:
                    return Error("Sintactico","Se esperaba una variable tipo array", self.row, self.column)
                value = self.numbers[0].Ejecutar(arbol, tabla)
                if isinstance(value, Error):
                    return value
                if value.type != Tipos.ENTERO:
                    return Error("Sintactico","La posición indicada de un array debe ser un entero", self.row, self.column)
                generador.comment("Inicio de llamado de array")
                a = 0
                t_type = Tipos.ARRAY
                types = []
                aux = valor.types
                temp = None
                error = False
                if tabla.previous == None:
                    temp = valor.position
                else:
                    temp = generador.new_temporal()
                    if len(arbol.function)>0:
                        generador.place_operation(temp, 'P', valor.position-tabla.previous.size, '+')
                    else:
                        generador.place_operation(temp, 'P', valor.position,'+')
                
                exit = generador.new_label()
                for x in self.numbers:
                    number = x.Ejecutar(arbol, tabla)
                    if isinstance(number,Error):
                        return number
                    if x.type != Tipos.ENTERO:
                        return Error("Sintactico", "La posición de un array debe ser un valor Int64", self.row, self.column)
                    temp_number = number.valor-1
                    if a == 0:
                        if temp_number > len(aux)-1:
                            error = True
                        else:
                            aux = aux[temp_number]
                    if temp_number <0:
                        error = True
                    if a != len(self.numbers)-1 and type(aux)!=type([]):
                        return Error("Sintactico","Se esperaba un Array", self.row, self.column)
                    types = number.types
                    if type(aux)==type([]) and a > 0:
                        if temp_number > len(aux)-1:
                            error = True
                            if a!=len(valor.types)-1:
                                t_type = [Tipos.NOTHING]
                            else:
                                t_type = Tipos.NOTHING
                        else:
                            t_type = aux[temp_number]
                    else:
                        t_type = aux
                    aux = t_type
                    a +=1
                    #codigo para hacer el array#
                    if type(aux) == type([]):
                        types = aux
                    else:
                        types = None
                    if a == 1:
                        temp = self.get_position_array(number.value, temp, exit, True)
                    else:
                        temp = self.get_position_array(number.value, temp, exit, False)
                    #fin de codigo para hacer array#
                if type(t_type) != type([]):
                    self.type = t_type
                if error:
                    self.type = Tipos.NOTHING
                generador.place_label(exit)
                generador.comment("Fin de llamado de array")
                ret = Retorno(temp, self.type, True)
                ret.types = types
                self.types = types
                return ret
            else:
                return Error("Sintactico","La variable indicada no existe", self.row, self.column)
                                          
    
    def get_position_array(self, num, valor, exit, in_stack):
        genAux = Generador()
        generador = genAux.get_instance()
        generador.comment("iniciando obtención valor dentro de array")
        if in_stack:
            heap = generador.new_temporal()
        size = generador.new_temporal()
        comp = generador.new_temporal()
        if in_stack:
            generador.get_stack(heap, valor)
        else:
            heap = valor
        generador.get_heap(size, heap)
        generador.place_operation(comp, heap, size, '+')
        number = generador.new_temporal()
        generador.place_operation(number, heap,num,'+')
        generador.set_unused_temp(heap)
        generador.set_unused_temp(size)
        true_tag = generador.new_label()
        false_tag = generador.new_label()
        temp_ret = generador.new_temporal()
        generador.place_if(number, 1, '<',false_tag)
        generador.place_if(number, comp, '<=',true_tag)
        generador.place_label(false_tag)
        generador.print_BoundsError()
        generador.place_operation(temp_ret, -1, '','')
        generador.call_function("BoundsError")
        generador.place_goto(exit)
        generador.place_label(true_tag)
        generador.get_heap(temp_ret, number)
        
        generador.comment("terminando obtención valor dentro de array")
        return temp_ret
        
    def getNodo(self) -> NodoAST:
        nodo = NodoAST('PRINT')
        
        return nodo