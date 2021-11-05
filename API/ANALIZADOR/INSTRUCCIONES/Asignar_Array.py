from typing import List


from ..GENERAL.generator import Generador

from ..ABSTRACT.Retorno import Retorno
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.table import Tabla
from ..GENERAL.Tipo import Tipos
from ..GENERAL.error import Error
from ..GENERAL.Simbolo import Simbolo

class Asignar_Array(Instruccion):

    def __init__(self, id, numbers:List,expresion, fila, columna, required_type=None):
        super().__init__(Tipos.STRING, fila, columna)
        self.id = id
        self.expresion = expresion
        self.required_type = required_type
        self.numbers:List = numbers
        
    def Ejecutar(self, arbol: Arbol, tabla: Tabla):
        genAux = Generador()
        generador = genAux.get_instance()
        if isinstance(generador, Generador):
            generador.comment("Asignación de variable "+self.id+"[n]")
            if isinstance(self.expresion, Instruccion):
                valor = self.expresion.Ejecutar(arbol, tabla)
                if isinstance(valor, Error):
                    generador.error_code()
                    return valor
                if type(self.required_type) == type([]):
                    if self.expresion.types != self.required_type:
                        generador.error_code()
                        return Error("Sintactico", "tipo de Arreglo Invalido", self.row, self.column)
                elif self.expresion.type != self.required_type and self.required_type != None:
                    generador.error_code()
                    return Error("Sintactico", "Se esperaba un valor tipo "+self.required_type.value+" y se obtuvo un valor tipo "+self.expresion.type.value, self.row, self.column)
                self.type = self.expresion.type
                if tabla.get_variable(self.id) == None:
                    generador.error_code()
                    return Error("Sintactico","La variable indicada no existe", self.row, self.column)
                else:
                    variable = tabla.get_variable(self.id)
                    if isinstance(variable, Simbolo):
                        generador.comment("Inicio de llamado de array")
                        a = 0
                        t_type = Tipos.ARRAY
                        aux = variable.types
                        temp = None
                        error = False
                        if tabla.previous == None:
                            temp = variable.position
                        else:
                            temp = generador.new_temporal()
                            if len(arbol.function)>0:
                                generador.place_operation(temp, 'P', variable.position-tabla.previous.size, '+')
                            else:
                                generador.place_operation(temp, 'P', variable.position,'+')
                        
                        exit = generador.new_label()
                        for x in self.numbers:
                            number = x.Ejecutar(arbol, tabla)
                            if isinstance(number,Error):
                                return number
                            if x.type != Tipos.ENTERO:
                                generador.error_code()
                                return Error("Sintactico", "La posición de un array debe ser un valor Int64", self.row, self.column)
                            temp_number = number.valor-1
                            if a == 0:
                                aux = aux[0]
                            if temp_number <0:
                                error = True
                            if a != len(self.numbers)-1 and type(aux)!=type([]):
                                generador.error_code()
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
                            generador.set_unused_temp(temp)
                            if a == 1:
                                if a == len(self.numbers):
                                    temp = self.get_position_array(number.value, temp, exit, True, True, valor.value)
                                else:
                                    temp = self.get_position_array(number.value, temp, exit, True, False, valor.value)
                            else:
                                if a == len(self.numbers):
                                     temp = self.get_position_array(number.value, temp, exit, False, True, valor.value)
                                else:
                                     temp = self.get_position_array(number.value, temp, exit, False, False, valor.value)
                            #fin de codigo para hacer array#
                    generador.place_label(exit)
                    generador.comment("Fin de llamado de array")
                variable.struct_type = self.expresion.struct_type
                generador.set_anterior()
                generador.comment("Terminando asignación de variable "+self.id)
                
    def get_position_array(self, num, valor, exit, in_stack, final, value):
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
        generador.place_if(number, 1, '<',false_tag)
        generador.place_if(number, comp, '<=',true_tag)
        generador.place_label(false_tag)
        generador.print_BoundsError()
        if final:
            generador.place_operation(number, -1, '','')
            generador.call_function("BoundsError")
            generador.place_goto(exit)
            generador.place_label(true_tag)
            generador.insert_heap(number, value)
            generador.set_unused_temp(number)
            generador.set_unused_temp(comp)
            return number
        else:
            temp_ret = generador.new_temporal()
            generador.place_operation(temp_ret, -1, '','')
            generador.call_function("BoundsError")
            generador.place_goto(exit)
            generador.place_label(true_tag)
            generador.get_heap(temp_ret, number)
            generador.set_unused_temp(number)
            generador.set_unused_temp(comp)
            generador.comment("terminando obtención valor dentro de array")
            
            return temp_ret
        
    def getNodo(self) -> NodoAST:
        nodo = NodoAST('PRINT')
        
        return nodo