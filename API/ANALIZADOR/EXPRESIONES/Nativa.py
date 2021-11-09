import re
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.table import Tabla
from ..GENERAL.Tipo import Tipos, Tipos_Nativa
from ..GENERAL.error import Error
from ..DICCIONARIO.Diccionario import D_NATIVA
from ..ABSTRACT.Retorno import Retorno
from ..GENERAL.generator import Generador
import math

class Nativas(Instruccion):

    def __init__(self, row, column, expresion, Nativa, valor2=None):
        super().__init__(Tipos.ENTERO, row, column)
        self.expresion = expresion
        self.Nativa = Nativa
        self.valor2 = valor2
        self.anterior = None

    def Ejecutar(self, arbol: Arbol, tabla: Tabla):
        genAux = Generador()
        generador = genAux.get_instance()
        if isinstance(generador, Generador):
            inst = None
            if self.valor2 is not None:
                valor = self.valor2.Ejecutar(arbol, tabla)
                if isinstance(valor, Error): return valor
                try:
                    inst = D_NATIVA[self.Nativa.value+"-"+self.expresion.value+"-"+self.valor2.type.value]
                except:
                    if self.Nativa == Tipos_Nativa.PARSE:
                        return Error('Semantico', 'No se puede convertir ' + valor + ' a Float64', self.row, self.column)
                    if self.Nativa == Tipos_Nativa.TRUNC:
                        return Error('Semantico', 'No es posible realizar trunc de ' + valor, self.row, self.column)
            else:
                valor = self.expresion.Ejecutar(arbol, tabla)
                if isinstance(valor, Error): return valor
                try:
                    inst = D_NATIVA[self.Nativa.value+"-"+self.expresion.type.value]
                except:
                    if self.Nativa == Tipos_Nativa.UPPERCASE:
                        return Error('Semantico', 'La función uppercase unicamente acepta String', self.row, self.column)
                    elif self.Nativa == Tipos_Nativa.LOWERCASE:
                        return Error('Semantico', 'La función lowercase unicamente acepta String', self.row, self.column)
                    elif self.Nativa == Tipos_Nativa.STRING:
                        return Error('Semantico', 'No es posible convertir '+valor+" a string", self.row, self.column)
                    else:
                        return Error('Semantico', 'La función '+self.Nativa.value.lower()+" requiere valores numericos", self.row, self.column)
            if self.Nativa == Tipos_Nativa.STRING:
                if valor.type == Tipos.STRING:
                    ret_temp = valor.value
                elif valor.type == Tipos.ARRAY:
                    generador.concat_string()
                    generador.comment("inicio de to_string(array)")
                    heap = generador.new_temporal()
                    temp = generador.new_temporal()
                    size = generador.new_temporal()
                    generador.get_heap(heap, valor.value)
                    generador.place_operation(size, heap, valor.value, '+')
                    generador.place_operation(temp, size, '1', '-')
                    #generamos [
                    self.anterior = generador.new_temporal()
                    generador.place_operation(self.anterior, 'H', '', '')
                    generador.insert_heap('H', 91)
                    generador.next_heap()
                    generador.insert_heap('H',-1)
                    generador.next_heap()
                    ####
                    
                    w = generador.new_label()
                    true_tag = generador.new_label()
                    comp = generador.new_temporal()
                    generador.place_operation(comp, valor.value, '1','+')
                    generador.set_unused_temp(valor.value)
                    generador.set_unused_temp(heap)
                    generador.set_unused_temp(size)
                    generador.place_label(w)
                    generador.place_if(comp, temp, '>', true_tag)
                    tipo = self.print_array(valor.types, valor, comp, tabla)
                    generador.place_operation(comp, comp, 1, '+')
                    if type(valor.types[0]) == type([]):
                        #generamos la , 
                        temp_num = generador.new_temporal()
                        generador.place_operation(temp_num, 'H', '', '')
                        generador.insert_heap('H', 44)
                        generador.next_heap()
                        generador.insert_heap('H',-1)
                        generador.next_heap()
                        ret_temp = generador.new_temporal()
                        generador.set_unused_temp(temp_num)
                        generador.set_unused_temp(ret_temp)
                        generador.set_unused_temp(self.anterior)
                        generador.set_unused_temp(comp)
                        generador.set_unused_temp(temp)
                        generador.set_unused_temp(comp)
                        generador.set_unused_temp(valor.value)
                        #combinamos con el self.anterior
                        generador.temporary_storage()
                        if tabla.previous is not None and tabla.previous!=arbol.global_table or generador.in_function:
                            generador.place_operation(ret_temp, 'P',tabla.size-tabla.previous.size,'+')
                        else:
                            generador.place_operation(ret_temp, 'P',tabla.size,'+')
                        generador.place_operation(ret_temp, ret_temp, 1, '+')
                        generador.insert_stack(ret_temp, self.anterior)
                        generador.place_operation(ret_temp, ret_temp, 1, '+')
                        generador.insert_stack(ret_temp, temp_num)
                        
                        generador.new_env(tabla.size, tabla.previous)      
                        generador.call_function("concat_string")
                        generador.use_temps[self.anterior] = self.anterior
                        generador.get_stack(self.anterior, 'P')
                        generador.return_evn(tabla.size, tabla.previous)
                        generador.take_temporary()
                        ####
                    generador.place_goto(w)
                    generador.place_label(true_tag)
                    if type(valor.types[0]) == type([]):
                        generador.use_temps[comp] = comp
                        tipo = self.print_array(valor.types, valor, comp, tabla)
                        generador.set_unused_temp(comp)
                    else:
                        generador.use_temps[comp] = comp
                        tipo = self.print_primitive(tipo, comp,  False, tabla)
                        generador.set_unused_temp(comp)
                    #generamos ]
                    temp_arr = generador.new_temporal()
                    generador.place_operation(temp_arr, 'H', '', '')
                    generador.insert_heap('H', 93)
                    generador.next_heap()
                    generador.insert_heap('H',-1)
                    generador.next_heap()
                    #unimos esto con lo self.anterior
                    ret_temp = generador.new_temporal()
                    generador.set_unused_temp(ret_temp)
                    generador.set_unused_temp(temp_arr)
                    generador.set_unused_temp(self.anterior)
                    generador.temporary_storage()
                    if tabla.previous is not None and tabla.previous!=arbol.global_table or generador.in_function:
                        generador.place_operation(ret_temp, 'P',tabla.size-tabla.previous.size,'+')
                    else:
                        generador.place_operation(ret_temp, 'P',tabla.size,'+')
                    generador.insert_stack(ret_temp, self.anterior)
                    generador.place_operation(ret_temp, ret_temp, 1, '+')
                    generador.insert_stack(ret_temp, temp_arr)
                    
                    generador.new_env(tabla.size, tabla.previous)
                    generador.call_function("concat_string")
                    generador.use_temps[self.anterior] = self.anterior
                    generador.get_stack(self.anterior, 'P')
                    generador.return_evn(tabla.size, tabla.previous)
                    generador.take_temporary()
                    ##
                    ret_temp = self.anterior
                    generador.comment("final to_string(array)")
                elif valor.type ==Tipos.BOOL:
                    ret_temp = generador.new_temporal()
                    exit = generador.new_label()
                    generador.place_label(valor.true_tag)
                    generador.place_operation(ret_temp, 'H', '','')
                    generador.insert_heap('H', ord('t'))
                    generador.next_heap()
                    generador.insert_heap('H', ord('r'))
                    generador.next_heap()
                    generador.insert_heap('H', ord('u'))
                    generador.next_heap()
                    generador.insert_heap('H', ord('e'))
                    generador.next_heap()
                    generador.insert_heap('H', -1)
                    generador.next_heap()
                    generador.place_goto(exit)
                    generador.place_label(valor.false_tag)
                    generador.place_operation(ret_temp, 'H', '','')
                    generador.insert_heap('H', ord('f'))
                    generador.next_heap()
                    generador.insert_heap('H', ord('a'))
                    generador.next_heap()
                    generador.insert_heap('H', ord('l'))
                    generador.next_heap()
                    generador.insert_heap('H', ord('s'))
                    generador.next_heap()
                    generador.insert_heap('H', ord('e'))
                    generador.next_heap()
                    generador.insert_heap('H', -1)
                    generador.next_heap()
                    generador.place_label(exit)
                elif valor.type == Tipos.RANGE:
                    if valor.auxiliar_type == Tipos.FLOAT:
                        generador.to_string_float()
                    else:
                        generador.to_string_int()
                        
                    t1 = generador.new_temporal()
                    t2 = generador.new_temporal()
                    ret_temp = generador.new_temporal()
                    generador.concat_string()
                    generador.get_heap(t1, valor.value)
                    generador.place_operation(valor.value, valor.value, 1, '+')
                    generador.get_heap(t2, valor.value)
                    generador.set_unused_temp(t1)
                    generador.set_unused_temp(valor.value)
                    generador.set_unused_temp(ret_temp)
                    generador.temporary_storage()
                    #volviendo t1 a string
                    if tabla.previous is not None and tabla.previous!=arbol.global_table or generador.in_function:
                        generador.place_operation(ret_temp, 'P',tabla.size-tabla.previous.size,'+')
                    else:
                        generador.place_operation(ret_temp, 'P',tabla.size,'+')
                    generador.place_operation(ret_temp, ret_temp, 1, '+')
                    generador.insert_stack(ret_temp, t1)
                    generador.new_env(tabla.size, tabla.previous)
                    if valor.auxiliar_type == Tipos.FLOAT:
                        generador.call_function("to_string")
                    else:
                        generador.call_function("to_string_int")
                    t1 = generador.new_temporal()
                    generador.get_stack(t1, 'P')
                    generador.return_evn(tabla.size, tabla.previous)
                    generador.take_temporary()
                    ####
                    #generando el :
                    dp = generador.new_temporal()
                    ret_temp = generador.new_temporal()
                    
                    generador.place_operation(dp, 'H', '', '')
                    generador.insert_heap('H', ord(':'))
                    generador.next_heap()
                    generador.insert_heap('H', -1)
                    generador.next_heap()
                    ###
                    generador.set_unused_temp(ret_temp)
                    generador.set_unused_temp(dp)
                    generador.set_unused_temp(t1)
                    generador.temporary_storage()
                    ##
                    ##concatenando t1 y :
                    if tabla.previous is not None and tabla.previous!=arbol.global_table or generador.in_function:
                        generador.place_operation(ret_temp, 'P',tabla.size-tabla.previous.size,'+')
                    else:
                        generador.place_operation(ret_temp, 'P',tabla.size,'+')
                    generador.place_operation(ret_temp, ret_temp, 1, '+')
                    generador.insert_stack(ret_temp, t1)
                    generador.place_operation(ret_temp, ret_temp, 1, '+')
                    generador.insert_stack(ret_temp, dp)
                    generador.new_env(tabla.size, tabla.previous)
                    generador.call_function("concat_string")
                    t1 = generador.new_temporal()
                    generador.get_stack(t1, 'P')
                    generador.return_evn(tabla.size, tabla.previous)
                    generador.take_temporary()
                    ###
                    ###enviando t2 a convertir a string
                    ret_temp = generador.new_temporal()
                    generador.set_unused_temp(t2)
                    generador.set_unused_temp(ret_temp)
                    generador.temporary_storage()
                    if tabla.previous is not None and tabla.previous!=arbol.global_table or generador.in_function:
                        generador.place_operation(ret_temp, 'P',tabla.size-tabla.previous.size,'+')
                    else:
                        generador.place_operation(ret_temp, 'P',tabla.size,'+')
                    generador.place_operation(ret_temp, ret_temp, 1, '+')
                    generador.insert_stack(ret_temp, t2)
                    generador.new_env(tabla.size, tabla.previous)    
                    if valor.auxiliar_type == Tipos.FLOAT:
                        generador.call_function("to_string")
                    else:
                        generador.call_function("to_string_int")
                    t2 = generador.new_temporal()
                    generador.get_stack(t2, 'P')
                    generador.return_evn(tabla.size, tabla.previous)
                    generador.take_temporary()
                    ###
                    ret_temp = generador.new_temporal()
                    generador.set_unused_temp(ret_temp)
                    generador.set_unused_temp(t1)
                    generador.set_unused_temp(t2)
                    generador.temporary_storage()
                    if tabla.previous is not None and tabla.previous!=arbol.global_table or generador.in_function:
                        generador.place_operation(ret_temp, 'P',tabla.size-tabla.previous.size,'+')
                    else:
                        generador.place_operation(ret_temp, 'P',tabla.size,'+')
                    generador.place_operation(ret_temp, ret_temp, 1, '+')
                    generador.insert_stack(ret_temp, t1)
                    generador.place_operation(ret_temp, ret_temp, 1, '+')
                    generador.insert_stack(ret_temp, t2)
                    ###concatenando t2
                    generador.new_env(tabla.size, tabla.previous)
                    generador.call_function("concat_string")
                    ret_temp = generador.new_temporal()
                    generador.get_stack(ret_temp, 'P')
                    generador.return_evn(tabla.size, tabla.previous)
                    generador.take_temporary()
                    ###
                elif valor.type == Tipos.STRUCT:
                    pass
                elif valor.type == Tipos.OBJECT:
                    pass
                else:
                    if valor.type == Tipos.FLOAT:
                        generador.to_string_float()
                    else:
                        generador.to_string_int()
                    ret_temp = generador.new_temporal()
                    generador.set_unused_temp(ret_temp)
                    generador.set_unused_temp(valor.value)
                    generador.temporary_storage()
                    if tabla.previous is not None and tabla.previous!=arbol.global_table or generador.in_function:
                        generador.place_operation(ret_temp, 'P',tabla.size-tabla.previous.size,'+')
                    else:
                        generador.place_operation(ret_temp, 'P',tabla.size,'+')
                    generador.place_operation(ret_temp, ret_temp, 1, '+')
                    generador.insert_stack(ret_temp, valor.value)
                    generador.new_env(tabla.size, tabla.previous)
                    if valor.type == Tipos.FLOAT:
                        generador.call_function("to_string")
                    else:
                        generador.call_function("to_string_int")
                    ret_temp = generador.new_temporal()
                    generador.get_stack(ret_temp, 'P')
                    generador.return_evn(tabla.size, tabla.previous)
                    generador.take_temporary()
            if self.Nativa == Tipos_Nativa.FLOAT:
                ret_temp = generador.new_temporal()
                generador.place_operation(ret_temp, valor.value, '1.0', '*')
            if self.Nativa == Tipos_Nativa.LOWERCASE:
                generador.lowercase()
                temp = generador.new_temporal()
                generador.set_unused_temp(valor.value)
                generador.set_unused_temp(temp)
                generador.temporary_storage()
                if tabla.previous is not None and tabla.previous!=arbol.global_table or generador.in_function:
                    generador.place_operation(temp, 'P',tabla.size-tabla.previous.size,'+')
                else:
                    generador.place_operation(temp, 'P',tabla.size,'+')
                generador.place_operation(temp, temp, 1, '+')
                generador.insert_stack(temp, valor.value)
                generador.new_env(tabla.size, tabla.previous)
                generador.call_function('lowercase')
                temp = generador.new_temporal()
                generador.get_stack(temp, 'P')
                generador.return_evn(tabla.size, tabla.previous)
                generador.take_temporary()
                ret_temp = temp
            if self.Nativa == Tipos_Nativa.UPPERCASE:
                generador.uppercase()
                temp = generador.new_temporal()
                generador.set_unused_temp(temp)
                generador.set_unused_temp(valor.value)
                generador.temporary_storage()
                if tabla.previous is not None and tabla.previous!=arbol.global_table or generador.in_function:
                    generador.place_operation(temp, 'P',tabla.size-tabla.previous.size,'+')
                else:
                    generador.place_operation(temp, 'P',tabla.size,'+')
                generador.place_operation(temp, temp, 1, '+')
                generador.insert_stack(temp, valor.value)
                generador.new_env(tabla.size, tabla.previous)
                generador.call_function('uppercase')
                temp = generador.new_temporal()
                generador.get_stack(temp, 'P')
                generador.return_evn(tabla.size, tabla.previous)
                generador.take_temporary()
                ret_temp = temp
            if self.Nativa == Tipos_Nativa.PARSE:
                if self.expresion == Tipos.FLOAT:
                    generador.parse_float()
                else:
                    generador.parse_int()
                ##
                temp = generador.new_temporal()
                generador.set_unused_temp(temp)
                generador.set_unused_temp(valor.value)
                generador.temporary_storage()
                if tabla.previous is not None and tabla.previous!=arbol.global_table or generador.in_function:
                    generador.place_operation(temp, 'P',tabla.size-tabla.previous.size,'+')
                else:
                    generador.place_operation(temp, 'P',tabla.size,'+')
                generador.place_operation(temp, temp, 1, '+')
                generador.insert_stack(temp, valor.value)
                ##    
                    
                generador.new_env(tabla.size, tabla.previous)
                if self.expresion == Tipos.FLOAT:
                    generador.call_function('parse_float')
                else:
                    generador.call_function('parse_int')
                temp = generador.new_temporal()
                generador.get_stack(temp, 'P')
                generador.return_evn(tabla.size, tabla.previous)
                generador.take_temporary()
                ret_temp = temp
            if self.Nativa == Tipos_Nativa.TRUNC:
                generador.trunc()
                temp = generador.new_temporal()
                generador.set_unused_temp(temp)
                generador.set_unused_temp(valor.value)
                generador.temporary_storage()
                
                if tabla.previous is not None and tabla.previous!=arbol.global_table or generador.in_function:
                    generador.place_operation(temp, 'P',tabla.size-tabla.previous.size,'+')
                else:
                    generador.place_operation(temp, 'P',tabla.size,'+')
                generador.place_operation(temp, temp, 1, '+')
                generador.insert_stack(temp, valor.value)
                
                generador.new_env(tabla.size, tabla.previous)
                generador.call_function('trunc')
                temp = generador.new_temporal()
                generador.get_stack(temp, 'P')
                generador.return_evn(tabla.size, tabla.previous)
                generador.take_temporary()
                ret_temp = temp
            if self.Nativa == Tipos_Nativa.LENGTH:
                generador.f_length()
                temp = generador.new_temporal()
                generador.set_unused_temp(temp)
                generador.set_unused_temp(valor.value)
                generador.temporary_storage()
                
                if tabla.previous is not None and tabla.previous!=arbol.global_table or generador.in_function:
                    generador.place_operation(temp, 'P',tabla.size-tabla.previous.size,'+')
                else:
                    generador.comment("hola")
                    generador.place_operation(temp, 'P',tabla.size,'+')
                generador.place_operation(temp, temp, 1, '+')
                generador.insert_stack(temp, valor.value)
                
                generador.new_env(tabla.size, tabla.previous)
                generador.call_function('f_length')
                temp = generador.new_temporal()
                generador.get_stack(temp, 'P')
                generador.return_evn(tabla.size, tabla.previous)
                generador.take_temporary()
                ret_temp = temp
            try: 
                self.type = inst[1]
                ret = Retorno(ret_temp, inst[1], True)
                if self.type != Tipos.ARRAY:
                    ret.valor = eval(inst[0])
                return ret
            except:
                return Error('Semantico', 'Error en la función '+self.Nativa.value.lower(), self.row, self.column)
    
    def print_array(self, types, retorno, variable, tabla):
        genAux = Generador()
        generador = genAux.get_instance()
        for x in types:
            if type(x) == type([]):
                stack = generador.new_temporal()
                generador.get_heap(stack, variable)
                heap = generador.new_temporal()
                size = generador.new_temporal()
                temp = generador.new_temporal()
                generador.get_heap(heap, stack)
                generador.place_operation(size, heap, stack, '+')
                generador.place_operation(temp, size, 1, '-')
                generador.set_unused_temp(heap)
                generador.set_unused_temp(size)
                #generamos [
                temp_arr = generador.new_temporal()
                generador.place_operation(temp_arr, 'H', '', '')
                generador.insert_heap('H', 91)
                generador.next_heap()
                generador.insert_heap('H',-1)
                generador.next_heap()
                #combinando lo self.anterior anexado si existe
                if self.anterior is not None:
                    ret_temp = generador.new_temporal()
                    generador.set_unused_temp(ret_temp)
                    generador.set_unused_temp(temp)
                    generador.set_unused_temp(temp_arr)
                    generador.set_unused_temp(self.anterior)
                    generador.temporary_storage()
                    if tabla.previous is not None and tabla.previous.previous is not None or generador.in_function:
                        generador.place_operation(ret_temp, 'P',tabla.size-tabla.previous.size,'+')
                    else:
                        generador.place_operation(ret_temp, 'P',tabla.size,'+')
                    generador.place_operation(ret_temp, ret_temp, 1, '+')
                    generador.insert_stack(ret_temp, self.anterior)
                    generador.place_operation(ret_temp, ret_temp, 1, '+')
                    generador.insert_stack(ret_temp, temp_arr)
                    
                    generador.new_env(tabla.size, tabla.previous)
                    generador.call_function("concat_string")
                    generador.use_temps[self.anterior] = self.anterior
                    generador.get_stack(self.anterior, 'P')
                    generador.return_evn(tabla.size, tabla.previous)
                    generador.take_temporary()
                else:
                    self.anterior = temp_arr
                ##
                w = generador.new_label()
                true_tag = generador.new_label()
                comp = generador.new_temporal()
                generador.place_operation(comp, stack, 1,'+')
                generador.set_unused_temp(stack)
                
                generador.place_label(w)
                generador.place_if(comp, temp, '>', true_tag)
                tipo = self.print_array(x, retorno, comp, tabla)
                generador.place_operation(comp, comp, 1, '+')
                generador.place_goto(w)
                generador.place_label(true_tag)
                ##aqui imprimir sin coma
                if type(x[0]) == type([]):
                    tipo = self.print_array(x, retorno, comp, tabla)
                else:
                    tipo = self.print_primitive(tipo, comp,  False, tabla)
                ##
                
                #generamos ]
                temp_arr = generador.new_temporal()
                generador.place_operation(temp_arr, 'H', '', '')
                generador.insert_heap('H', 93)
                generador.next_heap()
                generador.insert_heap('H',-1)
                generador.next_heap()
                #unimos esto con lo self.anterior
                generador.set_unused_temp(comp)
                
                ret_temp = generador.new_temporal()
                generador.set_unused_temp(ret_temp)
                generador.set_unused_temp(temp_arr)
                generador.set_unused_temp(self.anterior)
                generador.temporary_storage()
                if tabla.previous is not None and tabla.previous.previous is not None or generador.in_function:
                    generador.place_operation(ret_temp, 'P',tabla.size-tabla.previous.size,'+')
                else:
                    generador.place_operation(ret_temp, 'P',tabla.size,'+')
                generador.place_operation(ret_temp, ret_temp, 1, '+')
                generador.insert_stack(ret_temp, self.anterior)
                generador.place_operation(ret_temp, ret_temp, 1, '+')
                generador.insert_stack(ret_temp, temp_arr)
                
                generador.new_env(tabla.size, tabla.previous)        
                generador.call_function("concat_string")
                generador.use_temps[self.anterior] = self.anterior
                generador.get_stack(self.anterior, 'P')
                generador.return_evn(tabla.size, tabla.previous)
                generador.take_temporary()
                ##
                return tipo
            else:
                tipo = self.print_primitive(x, variable,  True, tabla)
                return x
    
    def print_primitive(self,x, variable,  condicion, tabla):
        genAux = Generador()
        generador = genAux.get_instance()
        if x == Tipos.ENTERO or x == Tipos.FLOAT:
            if x == Tipos.FLOAT:
                generador.to_string_float()
            else:
                generador.to_string_int()
            temp = generador.new_temporal()
            generador.get_heap(temp, variable)
            ### convertimos el valor en string
            ret_temp = generador.new_temporal()
            generador.set_unused_temp(variable)
            generador.set_unused_temp(temp)
            generador.set_unused_temp(ret_temp)
            generador.set_unused_temp(self.anterior)
            generador.temporary_storage()
            if tabla.previous is not None and tabla.previous.previous is not None or generador.in_function:
                generador.place_operation(ret_temp, 'P',tabla.size-tabla.previous.size,'+')
            else:
                generador.place_operation(ret_temp, 'P',tabla.size,'+')
            generador.place_operation(ret_temp, ret_temp, 1, '+')
            generador.insert_stack(ret_temp, temp)
            
            generador.new_env(tabla.size, tabla.previous)
            generador.call_function("to_string_int")
            temp = generador.new_temporal()
            generador.get_stack(temp, 'P')
            generador.return_evn(tabla.size, tabla.previous)
            generador.take_temporary()
            ### 
            ## Concatenamos el valor int con el self.anterior si existe
            if self.anterior is not None:
                generador.use_temps[self.anterior] = self.anterior
                ret_temp = generador.new_temporal()
                generador.set_unused_temp(self.anterior)
                generador.set_unused_temp(ret_temp)
                generador.set_unused_temp(temp)
                generador.temporary_storage()
                if tabla.previous is not None and tabla.previous.previous is not None or generador.in_function:
                    generador.place_operation(ret_temp, 'P',tabla.size-tabla.previous.size,'+')
                else:
                    generador.place_operation(ret_temp, 'P',tabla.size,'+')
                generador.place_operation(ret_temp, ret_temp, 1, '+')
                generador.insert_stack(ret_temp, self.anterior)
                generador.place_operation(ret_temp, ret_temp, 1, '+')
                generador.insert_stack(ret_temp, temp)
                
                generador.new_env(tabla.size, tabla.previous)
                generador.call_function("concat_string")
                generador.use_temps[self.anterior] = self.anterior
                generador.get_stack(self.anterior, 'P')
                generador.return_evn(tabla.size, tabla.previous)
                generador.take_temporary()
            else:
                self.anterior = temp
            ##
            if condicion:
                #generamos la ,
                temp_arr = generador.new_temporal()
                generador.place_operation(temp_arr, 'H', '', '')
                generador.insert_heap('H', 44)
                generador.next_heap()
                generador.insert_heap('H',-1)
                generador.next_heap()
                ret_temp = generador.new_temporal()
                generador.set_unused_temp(ret_temp)
                generador.set_unused_temp(temp_arr)
                generador.set_unused_temp(self.anterior)
                generador.temporary_storage()
                if tabla.previous is not None and tabla.previous.previous is not None or generador.in_function:
                    generador.place_operation(ret_temp, 'P',tabla.size-tabla.previous.size,'+')
                else:
                    generador.place_operation(ret_temp, 'P',tabla.size,'+')
                generador.place_operation(ret_temp, ret_temp, 1, '+')
                generador.insert_stack(ret_temp, self.anterior)
                generador.place_operation(ret_temp, ret_temp, 1, '+')
                generador.insert_stack(ret_temp, temp_arr)
                
                #combinamos con el self.anterior
                generador.new_env(tabla.size, tabla.previous)
                generador.call_function("concat_string")
                generador.use_temps[self.anterior] = self.anterior
                generador.get_stack(self.anterior, 'P')
                generador.return_evn(tabla.size, tabla.previous)
                generador.take_temporary()
        elif x == Tipos.STRING:
            temp_arr = generador.new_temporal()
            generador.place_operation(temp_arr, 'H', '', '')
            generador.insert_heap('H', 34)
            generador.next_heap()
            generador.insert_heap('H',-1)
            generador.next_heap()
            ## Concatenamos el valor char con el self.anterior si existe
            if self.anterior is not None:
                ret_temp = generador.new_temporal()
                generador.set_unused_temp(ret_temp)
                generador.set_unused_temp(temp_arr)
                generador.set_unused_temp(self.anterior)
                
                generador.temporary_storage()
                if tabla.previous is not None and tabla.previous.previous is not None or generador.in_function:
                    generador.place_operation(ret_temp, 'P',tabla.size-tabla.previous.size,'+')
                else:
                    generador.place_operation(ret_temp, 'P',tabla.size,'+')
                generador.place_operation(ret_temp, ret_temp, 1, '+')
                generador.insert_stack(ret_temp, self.anterior)
                generador.place_operation(ret_temp, ret_temp, 1, '+')
                generador.insert_stack(ret_temp, temp_arr)
                
                generador.new_env(tabla.size, tabla.previous)
                generador.call_function("concat_string")
                generador.use_temps[self.anterior] = self.anterior
                generador.get_stack(self.anterior, 'P')
                generador.return_evn(tabla.size, tabla.previous)
                generador.take_temporary()
            else:
                self.anterior = temp_arr
            ####
            temp_arr = generador.new_temporal()
            ret_temp = generador.new_temporal()
            
            generador.get_heap(temp_arr, variable)
            generador.set_unused_temp(ret_temp)
            generador.set_unused_temp(temp_arr)
            generador.set_unused_temp(variable)
            generador.set_unused_temp(self.anterior)
            generador.temporary_storage()
            if tabla.previous is not None and tabla.previous.previous is not None or generador.in_function:
                generador.place_operation(ret_temp, 'P',tabla.size-tabla.previous.size,'+')
            else:
                generador.place_operation(ret_temp, 'P',tabla.size,'+')
            generador.place_operation(ret_temp, ret_temp, 1, '+')
            generador.insert_stack(ret_temp, self.anterior)
            generador.place_operation(ret_temp, ret_temp, 1, '+')
            generador.insert_stack(ret_temp, temp_arr)
            
            #combinamos lo anterior
            generador.new_env(tabla.size, tabla.previous)
            generador.call_function("concat_string")
            generador.use_temps[self.anterior] = self.anterior
            generador.get_stack(self.anterior, 'P')
            generador.return_evn(tabla.size, tabla.previous)
            generador.take_temporary()
            #generamos "
            temp_arr = generador.new_temporal()
            generador.place_operation(temp_arr, 'H', '', '')
            generador.insert_heap('H', 34)
            generador.next_heap()
            generador.insert_heap('H',-1)
            generador.next_heap()
            ##
            ##combinamos lo anterior
            ret_temp = generador.new_temporal()
            
            generador.set_unused_temp(ret_temp)
            generador.set_unused_temp(temp_arr)
            generador.set_unused_temp(self.anterior)
            
            generador.temporary_storage()
            if tabla.previous is not None and tabla.previous.previous is not None or generador.in_function:
                generador.place_operation(ret_temp, 'P',tabla.size-tabla.previous.size,'+')
            else:
                generador.place_operation(ret_temp, 'P',tabla.size,'+')
            generador.place_operation(ret_temp, ret_temp, 1, '+')
            generador.insert_stack(ret_temp, self.anterior)
            generador.place_operation(ret_temp, ret_temp, 1, '+')
            generador.insert_stack(ret_temp, temp_arr)

            generador.new_env(tabla.size, tabla.previous)
            generador.call_function("concat_string")
            generador.use_temps[self.anterior] = self.anterior
            generador.get_stack(self.anterior, 'P')
            generador.return_evn(tabla.size, tabla.previous)
            generador.take_temporary()
            ##
            if condicion:
                #generamos la ,
                temp_arr = generador.new_temporal()
                generador.place_operation(temp_arr, 'H', '', '')
                generador.insert_heap('H', 44)
                generador.next_heap()
                generador.insert_heap('H',-1)
                generador.next_heap()
                ret_temp = generador.new_temporal()
                generador.set_unused_temp(ret_temp)
                generador.set_unused_temp(temp_arr)
                generador.set_unused_temp(self.anterior)
                generador.temporary_storage()
                if tabla.previous is not None and tabla.previous.previous is not None or generador.in_function:
                    generador.place_operation(ret_temp, 'P',tabla.size-tabla.previous.size,'+')
                else:
                    generador.place_operation(ret_temp, 'P',tabla.size,'+')
                generador.place_operation(ret_temp, ret_temp, 1, '+')
                generador.insert_stack(ret_temp, self.anterior)
                generador.place_operation(ret_temp, ret_temp, 1, '+')
                generador.insert_stack(ret_temp, temp_arr)
                
                #combinamos con el self.anterior
                generador.new_env(tabla.size, tabla.previous)
                generador.call_function("concat_string")
                generador.use_temps[self.anterior] = self.anterior
                generador.get_stack(self.anterior, 'P')
                generador.return_evn(tabla.size, tabla.previous)
                generador.take_temporary()
        elif x == Tipos.BOOL:
            temp = generador.new_temporal()
            generador.get_heap(temp, variable)
            aux = generador.new_label()
            true_flag = generador.new_label()
            false_flag = generador.new_label()
            generador.place_if(temp, 1, '==', true_flag)
            generador.place_goto(false_flag)
            generador.place_label(true_flag)
            generador.place_operation(temp, 'H', '', '')
            generador.insert_heap('H', ord('t'))
            generador.next_heap()
            generador.insert_heap('H', ord('r'))
            generador.next_heap()
            generador.insert_heap('H', ord('u'))
            generador.next_heap()
            generador.insert_heap('H', ord('e'))
            generador.next_heap()
            generador.insert_heap('H', -1)
            generador.next_heap()
            generador.place_goto(aux)
            generador.place_label(false_flag)
            generador.place_operation(temp, 'H', '', '')
            generador.insert_heap('H', ord('f'))
            generador.next_heap()
            generador.insert_heap('H', ord('a'))
            generador.next_heap()
            generador.insert_heap('H', ord('l'))
            generador.next_heap()
            generador.insert_heap('H', ord('s'))
            generador.next_heap()
            generador.insert_heap('H', ord('e'))
            generador.next_heap()
            generador.insert_heap('H', -1)
            generador.next_heap()
            generador.place_label(aux)
            #combinamos lo anterior con lo generado
            if self.anterior is not None:
                ret_temp = generador.new_temporal()
                generador.set_unused_temp(ret_temp)
                generador.set_unused_temp(temp)
                generador.set_unused_temp(variable)
                generador.set_unused_temp(self.anterior)
                generador.temporary_storage()
                if tabla.previous is not None and tabla.previous.previous is not None or generador.in_function:
                    generador.place_operation(ret_temp, 'P',tabla.size-tabla.previous.size,'+')
                else:
                    generador.place_operation(ret_temp, 'P',tabla.size,'+')
                generador.place_operation(ret_temp, ret_temp, 1, '+')
                generador.insert_stack(ret_temp, self.anterior)
                generador.place_operation(ret_temp, ret_temp, 1, '+')
                generador.insert_stack(ret_temp, temp)
                
                generador.new_env(tabla.size, tabla.previous)
                generador.call_function("concat_string")
                generador.use_temps[self.anterior] = self.anterior
                generador.get_stack(self.anterior, 'P')
                generador.return_evn(tabla.size, tabla.previous)
                generador.take_temporary()
            else:
                self.anterior = temp
            ###
            if condicion:
                #generamos la ,
                temp_arr = generador.new_temporal()
                generador.place_operation(temp_arr, 'H', '', '')
                generador.insert_heap('H', 44)
                generador.next_heap()
                generador.insert_heap('H',-1)
                generador.next_heap()
                ret_temp = generador.new_temporal()
                generador.set_unused_temp(ret_temp)
                generador.set_unused_temp(temp_arr)
                generador.set_unused_temp(self.anterior)
                generador.temporary_storage()
                if tabla.previous is not None and tabla.previous.previous is not None or generador.in_function:
                    generador.place_operation(ret_temp, 'P',tabla.size-tabla.previous.size,'+')
                else:
                    generador.place_operation(ret_temp, 'P',tabla.size,'+')
                generador.place_operation(ret_temp, ret_temp, 1, '+')
                generador.insert_stack(ret_temp, self.anterior)
                generador.place_operation(ret_temp, ret_temp, 1, '+')
                generador.insert_stack(ret_temp, temp_arr)
                
                #combinamos con el self.anterior
                generador.new_env(tabla.size, tabla.previous)
                generador.call_function("concat_string")
                generador.use_temps[self.anterior] = self.anterior
                generador.get_stack(self.anterior, 'P')
                generador.return_evn(tabla.size, tabla.previous)
                generador.take_temporary()
        elif x == Tipos.CHAR:
            #generamos '
            temp_arr = generador.new_temporal()
            generador.place_operation(temp_arr, 'H', '', '')
            generador.insert_heap('H', 39)
            generador.next_heap()
            generador.insert_heap('H',-1)
            generador.next_heap()
            ## Concatenamos el valor char con el self.anterior si existe
            if self.anterior is not None:
                ret_temp = generador.new_temporal()
                generador.set_unused_temp(ret_temp)
                generador.set_unused_temp(temp_arr)
                generador.set_unused_temp(self.anterior)
                generador.temporary_storage()       
                if tabla.previous is not None and tabla.previous.previous is not None or generador.in_function:
                    generador.place_operation(ret_temp, 'P',tabla.size-tabla.previous.size,'+')
                else:
                    generador.place_operation(ret_temp, 'P',tabla.size,'+')
                generador.place_operation(ret_temp, ret_temp, 1, '+')
                generador.insert_stack(ret_temp, self.anterior)
                generador.place_operation(ret_temp, ret_temp, 1, '+')
                generador.insert_stack(ret_temp, temp_arr)
                
                generador.new_env(tabla.size, tabla.previous)
                generador.call_function("concat_string")
                generador.use_temps[self.anterior] = self.anterior
                generador.get_stack(self.anterior, 'P')
                generador.return_evn(tabla.size, tabla.previous)
                generador.take_temporary()
            else:
                self.anterior = temp_arr
                
            temp = generador.new_temporal()
            generador.get_heap(temp, variable)
            #generamos el valor
            temp_arr = generador.new_temporal()
            generador.place_operation(temp_arr, 'H', '', '')
            generador.insert_heap('H', temp)
            generador.next_heap()
            generador.insert_heap('H',-1)
            generador.next_heap()
            
            ret_temp = generador.new_temporal()
            generador.set_unused_temp(ret_temp)
            generador.set_unused_temp(temp)
            generador.set_unused_temp(temp_arr)
            generador.set_unused_temp(self.anterior)
            generador.set_unused_temp(variable)
            
            generador.temporary_storage()
            if tabla.previous is not None and tabla.previous.previous is not None or generador.in_function:
                generador.place_operation(ret_temp, 'P',tabla.size-tabla.previous.size,'+')
            else:
                generador.place_operation(ret_temp, ret_temp,tabla.size,'+')
            generador.place_operation(ret_temp, 'P', 1, '+')
            generador.insert_stack(ret_temp, self.anterior)
            generador.place_operation(ret_temp, ret_temp, 1, '+')
            generador.insert_stack(ret_temp, temp_arr)
            
            
            #combinamos lo anterior
            generador.new_env(tabla.size, tabla.previous)
            generador.call_function("concat_string")
            generador.use_temps[self.anterior] = self.anterior
            generador.get_stack(self.anterior, 'P')
            generador.return_evn(tabla.size, tabla.previous)
            generador.take_temporary()
           
            #generamos '
            temp_arr = generador.new_temporal()
            generador.place_operation(temp_arr, 'H', '', '')
            generador.insert_heap('H', 39)
            generador.next_heap()
            generador.insert_heap('H',-1)
            generador.next_heap()
            
            
            ret_temp = generador.new_temporal()
            generador.set_unused_temp(ret_temp)
            generador.set_unused_temp(temp_arr)
            generador.set_unused_temp(self.anterior)
            
            generador.temporary_storage()
            if tabla.previous is not None and tabla.previous.previous is not None or generador.in_function:
                generador.place_operation(ret_temp, 'P',tabla.size-tabla.previous.size,'+')
            else:
                generador.place_operation(ret_temp, ret_temp,tabla.size,'+')
            generador.place_operation(ret_temp, 'P', 1, '+')
            generador.insert_stack(ret_temp, self.anterior)
            generador.place_operation(ret_temp, ret_temp, 1, '+')
            generador.insert_stack(ret_temp, temp_arr)
            
            generador.new_env(tabla.size, tabla.previous)
            generador.call_function("concat_string")
            generador.use_temps[self.anterior] = self.anterior
            generador.get_stack(self.anterior, 'P')
            generador.return_evn(tabla.size, tabla.previous)
            generador.take_temporary()
            ##
            if condicion:
                #generamos la ,
                temp_arr = generador.new_temporal()
                generador.place_operation(temp_arr, 'H', '', '')
                generador.insert_heap('H', 44)
                generador.next_heap()
                generador.insert_heap('H',-1)
                generador.next_heap()
                ret_temp = generador.new_temporal()
                generador.set_unused_temp(ret_temp)
                generador.set_unused_temp(temp_arr)
                generador.set_unused_temp(self.anterior)
                generador.temporary_storage()
                if tabla.previous is not None and tabla.previous.previous is not None or generador.in_function:
                    generador.place_operation(ret_temp, 'P',tabla.size-tabla.previous.size,'+')
                else:
                    generador.place_operation(ret_temp, 'P',tabla.size,'+')
                generador.place_operation(ret_temp, ret_temp, 1, '+')
                generador.insert_stack(ret_temp, self.anterior)
                generador.place_operation(ret_temp, ret_temp, 1, '+')
                generador.insert_stack(ret_temp, temp_arr)
                
                #combinamos con el self.anterior
                generador.new_env(tabla.size, tabla.previous)
                generador.call_function("concat_string")
                generador.use_temps[self.anterior] = self.anterior
                generador.get_stack(self.anterior, 'P')
                generador.return_evn(tabla.size, tabla.previous)
                generador.take_temporary()
        elif x == Tipos.NOTHING:
            temp = generador.new_temporal()
            generador.place_operation(temp, 'H', '', '')
            generador.insert_heap('H', ord('n'))
            generador.next_heap()
            generador.insert_heap('H', ord('o'))
            generador.next_heap()
            generador.insert_heap('H', ord('t'))
            generador.next_heap()
            generador.insert_heap('H', ord('h'))
            generador.next_heap()
            generador.insert_heap('H', ord('i'))
            generador.next_heap()
            generador.insert_heap('H', ord('g'))
            generador.next_heap()
            generador.insert_heap('H', -1)
            generador.next_heap()
            generador.set_unused_temp(variable)
            #combinamos lo anterior con lo generado
            if self.anterior is not None:
                
                ret_temp = generador.new_temporal()
                generador.set_unused_temp(ret_temp)
                generador.set_unused_temp(temp)
                generador.set_unused_temp(self.anterior)
                
                generador.temporary_storage()
                if tabla.previous is not None and tabla.previous.previous is not None or generador.in_function:
                    generador.place_operation(ret_temp, 'P',tabla.size-tabla.previous.size,'+')
                else:
                    generador.place_operation(ret_temp, 'P',tabla.size,'+')
                generador.place_operation(ret_temp, ret_temp, 1, '+')
                generador.insert_stack(ret_temp, self.anterior)
                generador.place_operation(ret_temp, ret_temp, 1, '+')
                generador.insert_stack(ret_temp, temp)
                
                
                generador.new_env(tabla.size, tabla.previous)
                generador.call_function("concat_string")
                generador.use_temps[self.anterior] = self.anterior
                generador.get_stack(self.anterior, 'P')
                generador.return_evn(tabla.size, tabla.previous)
                generador.take_temporary()
                
            else:
                self.anterior = temp
            ###
            if condicion:
                #generamos la ,
                temp_arr = generador.new_temporal()
                generador.place_operation(temp_arr, 'H', '', '')
                generador.insert_heap('H', 44)
                generador.next_heap()
                generador.insert_heap('H',-1)
                generador.next_heap()
                ret_temp = generador.new_temporal()
                generador.set_unused_temp(ret_temp)
                generador.set_unused_temp(temp_arr)
                generador.set_unused_temp(self.anterior)
                generador.temporary_storage()
                if tabla.previous is not None and tabla.previous.previous is not None or generador.in_function:
                    generador.place_operation(ret_temp, 'P',tabla.size-tabla.previous.size,'+')
                else:
                    generador.place_operation(ret_temp, 'P',tabla.size,'+')
                generador.place_operation(ret_temp, ret_temp, 1, '+')
                generador.insert_stack(ret_temp, self.anterior)
                generador.place_operation(ret_temp, ret_temp, 1, '+')
                generador.insert_stack(ret_temp, temp_arr)
                
                #combinamos con el self.anterior
                generador.new_env(tabla.size, tabla.previous)
                generador.call_function("concat_string")
                generador.use_temps[self.anterior] = self.anterior
                generador.get_stack(self.anterior, 'P')
                generador.return_evn(tabla.size, tabla.previous)
                generador.take_temporary()
        generador.set_unused_temp(self.anterior)
        return x
    
    def getNodo(self) -> NodoAST:
        nodo = NodoAST('NATIVA')
        if self.Nativa == Tipos_Nativa.LOG:
            nodo.agregarHijo(self.Nativa.value)
            nodo.agregarHijo('(')
            nodo.agregarHijoNodo(self.expresion.getNodo())
            nodo.agregarHijo(',')
            nodo.agregarHijoNodo(self.valor2.getNodo())
            nodo.agregarHijo(')')
        elif self.valor2 is not None:
            nodo.agregarHijo(self.Nativa.value)
            nodo.agregarHijo('(')
            nodo.agregarHijo(self.expresion.value)
            nodo.agregarHijo(',')
            nodo.agregarHijoNodo(self.valor2.getNodo())
            nodo.agregarHijo(')')
        else:
            nodo.agregarHijo(self.Nativa.value)
            nodo.agregarHijo('(')
            nodo.agregarHijoNodo(self.expresion.getNodo())
            nodo.agregarHijo(')')
        return nodo