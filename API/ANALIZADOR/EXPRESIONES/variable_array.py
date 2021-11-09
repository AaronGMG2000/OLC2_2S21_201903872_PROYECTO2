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

    def __init__(self, variable, numbers:List, fila, columna):
        super().__init__(Tipos.ARRAY, fila, columna)
        self.variable = variable
        self.numbers:List = numbers
        self.types = []
        
    def Ejecutar(self, arbol: Arbol, tabla: Tabla):
        genAux = Generador()
        generador = genAux.get_instance()
        if isinstance(generador, Generador):
            # valor = tabla.get_variable(self.id)
            valor = self.variable.Ejecutar(arbol, tabla)
            self.id = self.variable.id
            if  isinstance(valor, Retorno):
                if self.variable.type != Tipos.ARRAY:
                    return Error("Sintactico","Se esperaba una variable tipo array", self.row, self.column)
                generador.comment("Inicio de llamado de array")
                a = 0
                t_type = Tipos.ARRAY
                types = []
                aux = valor.types
                temp = valor.value
                error = False
                exit = generador.new_label()
                valor_nuevo = None
                for x in self.numbers:
                    number = x.Ejecutar(arbol, tabla)
                    if isinstance(number,Error):
                        return number
                    if x.type != Tipos.ENTERO and x.type != Tipos.RANGE:
                        return Error("Sintactico", "La posición de un array debe ser un valor Int64", self.row, self.column)
                    if (x.type == Tipos.RANGE and number.auxiliar_type!=Tipos.ENTERO):
                        return Error("Sintactico", "La posición de un array con un rango debe ser un valor Int64", self.row, self.column)
                    if type(number.valor) == type(1) and type(valor.valor)==type([]):
                        try:
                            valor_nuevo = valor.valor[number.valor-1]
                            valor.valor = valor.valor[number.valor-1]
                        except:
                            valor_nuevo = -1
                    if x.type!=Tipos.RANGE:
                        if a == 0:
                            aux = aux[0]
                        if a != len(self.numbers)-1 and type(aux)!=type([]):
                            return Error("Sintactico","Se esperaba un Array", self.row, self.column)
                    
                    types = number.types
                    if type(aux)==type([]) and a > 0:
                        t_type = aux[0]
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
                        if number.type == Tipos.RANGE:  
                            temp = self.get_position_array_range(number.value, temp, exit, False)
                            types = aux
                        else:
                            temp = self.get_position_array(number.value, temp, exit, False)
                    else:
                        temp = self.get_position_array(number.value, temp, exit, False)
                    #fin de codigo para hacer array#
                    generador.set_unused_temp(number.value)
                if type(t_type) != type([]):
                    self.type = t_type
                    if type(t_type) == type(""):
                        self.type = Tipos.OBJECT
                        self.struct_type = t_type
                if error:
                    self.type = Tipos.NOTHING
                generador.place_label(exit)
                generador.comment("Fin de llamado de array")
                ret = Retorno(temp, self.type, True)
                ret.types = types
                ret.valor = valor_nuevo
                self.types = types
                if self.type  == Tipos.OBJECT:
                    ret.auxiliar_type = self.struct_type
                else:
                    ret.auxiliar_type = None
                    self.struct_type = self.variable.struct_type
                return ret
            else:
                return valor
                                          
    
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
        generador.set_unused_temp(number)
        generador.set_unused_temp(comp)
        generador.comment("terminando obtención valor dentro de array")
        return temp_ret
    
    def get_position_array_range(self, num, valor, exit, in_stack):
        genAux = Generador()
        generador = genAux.get_instance()
        generador.comment("iniciando obtención valor dentro de array")
        if in_stack:
            heap = generador.new_temporal()
        w = generador.new_label()
        size = generador.new_temporal()
        comp = generador.new_temporal()
        if in_stack:
            generador.get_stack(heap, valor)
        else:
            heap = valor
        generador.get_heap(size, heap)
        generador.place_operation(comp, heap, size, '+')
        generador.set_unused_temp(size)
        exit_2 = generador.new_label()
        t1 = generador.new_temporal()
        t2 = generador.new_temporal()
        generador.get_heap(t1, num)
        generador.place_operation(num, num,1,'+')
        generador.get_heap(t2, num)
        #inicio de while
        temp_ret = generador.new_temporal()
        generador.place_operation(temp_ret, 'H','','')
        suma = generador.new_temporal()
        generador.place_operation(suma, t2, t1, '-')
        generador.place_operation(suma, suma, 1, '+')
        generador.insert_heap('H', suma)
        generador.set_unused_temp(suma)
        generador.next_heap()
        generador.place_label(w)
        generador.place_if(t1, t2, '>', exit_2)
        number = generador.new_temporal()
        generador.place_operation(number, heap, t1,'+')
        true_tag = generador.new_label()
        false_tag = generador.new_label()
        generador.place_if(number, 1, '<',false_tag)
        generador.place_if(number, comp, '<=',true_tag)
        generador.place_label(false_tag)
        generador.print_BoundsError()
        generador.place_operation(temp_ret, -1, '','')
        generador.call_function("BoundsError")
        generador.place_goto(exit)
        generador.place_label(true_tag)
        tempo = generador.new_temporal()
        generador.get_heap(tempo, number)
        generador.insert_heap('H', tempo)
        generador.next_heap()
        generador.set_unused_temp(tempo)
        generador.place_operation(t1, t1, 1, '+')
        generador.place_goto(w)
        generador.set_unused_temp(number)
        generador.set_unused_temp(comp)
        generador.place_label(exit_2)
        generador.comment("terminando obtención valor dentro de array")
        return temp_ret
    
    
    def getNodo(self) -> NodoAST:
        nodo = NodoAST('PRINT')
        
        return nodo