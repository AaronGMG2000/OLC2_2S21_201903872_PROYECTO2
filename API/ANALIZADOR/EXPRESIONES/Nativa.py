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
                    if valor.type == Tipos.ARRAY:
                        generador.concat_string()
                        generador.comment("inicio de to_string(array)")
                        heap = generador.new_temporal()
                        temp = generador.new_temporal()
                        size = generador.new_temporal()
                        generador.get_heap(heap, valor.value)
                        generador.place_operation(size, heap, valor.value, '+')
                        generador.place_operation(temp, size, '1', '-')
                        #generamos [
                        ret_temp = generador.new_temporal()
                        generador.place_operation(ret_temp, 'H', '', '')
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
                        tipo = self.print_array(valor.types, valor, comp, tabla, ret_temp)
                        anterior = tipo[1]
                        tipo = tipo[0]
                        generador.place_operation(comp, comp, 1, '+')
                        if type(valor.types[0]) == type([]):
                            #generamos la , 
                            temp_num = generador.new_temporal()
                            generador.place_operation(temp_num, 'H', '', '')
                            generador.insert_heap('H', 44)
                            generador.next_heap()
                            generador.insert_heap('H',-1)
                            generador.next_heap()
                            #combinamos con el anterior
                            ret_temp = generador.new_temporal()
                            generador.place_operation(ret_temp, 'P', tabla.size, '+')
                            generador.place_operation(ret_temp, ret_temp, 1, '+')
                            generador.insert_stack(ret_temp, anterior)
                            generador.place_operation(ret_temp, ret_temp, 1, '+')
                            generador.insert_stack(ret_temp, temp_num)
                            generador.set_unused_temp(temp_num)
                            generador.new_env(tabla.size)
                            generador.call_function("concat_string")
                            generador.get_stack(ret_temp, 'P')
                            generador.return_evn(tabla.size)
                            ####
                        generador.place_goto(w)
                        generador.place_label(true_tag)
                        if type(valor.types[0]) == type([]):
                            tipo = self.print_array(valor.types, valor, comp, tabla, ret_temp)
                            anterior = tipo[1]
                            tipo = tipo[0]
                        else:
                            tipo = self.print_primitive(tipo, comp,  False, tabla, ret_temp)
                            anterior = tipo[1]
                            tipo = tipo[0]
                        #generamos ]
                        temp_arr = generador.new_temporal()
                        generador.place_operation(temp_arr, 'H', '', '')
                        generador.insert_heap('H', 93)
                        generador.next_heap()
                        generador.insert_heap('H',-1)
                        generador.next_heap()
                        #unimos esto con lo anterior
                        ret_temp = generador.new_temporal()
                        generador.place_operation(ret_temp, 'P', tabla.size, '+')
                        generador.place_operation(ret_temp, ret_temp, 1, '+')
                        generador.insert_stack(ret_temp, anterior)
                        generador.place_operation(ret_temp, ret_temp, 1, '+')
                        generador.insert_stack(ret_temp, temp_arr)
                        generador.set_unused_temp(temp_arr)
                        generador.new_env(tabla.size)
                        generador.call_function("concat_string")
                        generador.get_stack(ret_temp, 'P')
                        generador.return_evn(tabla.size)
                        ##
                        generador.set_unused_temp(temp)
                        generador.set_unused_temp(comp)
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
                        t1 = generador.new_temporal()
                        t2 = generador.new_temporal()
                        if valor.auxiliar_type == Tipos.FLOAT:
                            generador.to_string_float()
                        else:
                            generador.to_string_int()
                        generador.concat_string()
                        generador.get_heap(t1, valor.value)
                        generador.place_operation(valor.value, valor.value, 1, '+')
                        generador.get_heap(t2, valor.value)
                        ret_temp = generador.new_temporal()
                        #volviendo t1 a string
                        
                        generador.place_operation(ret_temp, 'P', tabla.size, '+')
                        generador.place_operation(ret_temp, ret_temp, 1, '+')
                        generador.insert_stack(ret_temp, t1)
                        generador.new_env(tabla.size)
                        if valor.auxiliar_type == Tipos.FLOAT:
                            generador.call_function("to_string")
                        else:
                            generador.call_function("to_string_int")
                        generador.get_stack(t1, 'P')
                        generador.return_evn(tabla.size)
                        
                        ####
                        #generando el :
                        
                        dp = generador.new_temporal()
                        generador.place_operation(dp, 'H', '', '')
                        generador.insert_heap('H', ord(':'))
                        generador.next_heap()
                        generador.insert_heap('H', -1)
                        generador.next_heap()
                        ##
                        ##concatenando t1 y :
                        
                        generador.place_operation(ret_temp, 'P', tabla.size, '+')
                        generador.place_operation(ret_temp, ret_temp, 1, '+')
                        generador.insert_stack(ret_temp, t1)
                        generador.place_operation(ret_temp, ret_temp, 1, '+')
                        generador.insert_stack(ret_temp, dp)
                        generador.set_unused_temp(dp)
                        generador.new_env(tabla.size)
                        generador.call_function("concat_string")
                        generador.get_stack(t1, 'P')
                        generador.return_evn(tabla.size)
                        
                        ###
                        ###enviando t2 a convertir a string
                        
                        generador.place_operation(ret_temp, 'P', tabla.size, '+')
                        generador.place_operation(ret_temp, ret_temp, 1, '+')
                        generador.insert_stack(ret_temp, t2)
                        generador.new_env(tabla.size)
                        if valor.auxiliar_type == Tipos.FLOAT:
                            generador.call_function("to_string")
                        else:
                            generador.call_function("to_string_int")
                        generador.get_stack(t2, 'P')
                        generador.return_evn(tabla.size)
                        
                        ###
                        ###concatenando t2
                        
                        generador.place_operation(ret_temp, 'P', tabla.size, '+')
                        generador.place_operation(ret_temp, ret_temp, 1, '+')
                        generador.insert_stack(ret_temp, t1)
                        generador.place_operation(ret_temp, ret_temp, 1, '+')
                        generador.insert_stack(ret_temp, t2)
                        generador.set_unused_temp(dp)
                        generador.new_env(tabla.size)
                        generador.call_function("concat_string")
                        generador.get_stack(ret_temp, 'P')
                        generador.return_evn(tabla.size)
                        
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
                        generador.place_operation(ret_temp, 'P', tabla.size, '+')
                        generador.place_operation(ret_temp, ret_temp, 1, '+')
                        generador.insert_stack(ret_temp, valor.value)
                        generador.new_env(tabla.size)
                        if valor.type == Tipos.FLOAT:
                            generador.call_function("to_string")
                        else:
                            generador.call_function("to_string_int")
                        generador.get_stack(ret_temp, 'P')
                        generador.return_evn(tabla.size)
                if self.Nativa == Tipos_Nativa.FLOAT:
                    pass
                if self.Nativa == Tipos_Nativa.LOWERCASE:
                    pass
                if self.Nativa == Tipos_Nativa.UPPERCASE:
                    pass
                if self.Nativa == Tipos_Nativa.PARSE:
                    pass
                if self.Nativa == Tipos_Nativa.TRUNC:
                    pass
            try: 
                self.type = inst[1]
                ret = Retorno(ret_temp, inst[1], True)
                if self.type != Tipos.ARRAY:
                    ret.valor = eval(inst[0])
                return ret
            except:
                return Error('Semantico', 'Error en la función '+self.Nativa.value.lower(), self.row, self.column)
    
    def print_array(self, types, retorno, variable, tabla, anterior = None):
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
                #combinando lo anterior anexado si existe
                if anterior is not None:
                    ret_temp = generador.new_temporal()
                    generador.place_operation(ret_temp, 'P', tabla.size, '+')
                    generador.place_operation(ret_temp, ret_temp, 1, '+')
                    generador.insert_stack(ret_temp, anterior)
                    generador.place_operation(ret_temp, ret_temp, 1, '+')
                    generador.insert_stack(ret_temp, temp_arr)
                    generador.set_unused_temp(temp_arr)
                    generador.new_env(tabla.size)
                    generador.call_function("concat_string")
                    generador.get_stack(ret_temp, 'P')
                    generador.return_evn(tabla.size)
                else:
                    ret_temp = temp_arr
                ##
                w = generador.new_label()
                true_tag = generador.new_label()
                comp = generador.new_temporal()
                generador.place_operation(comp, stack, 1,'+')
                generador.set_unused_temp(stack)
                
                generador.place_label(w)
                generador.place_if(comp, temp, '>', true_tag)
                tipo = self.print_array(x, retorno, comp, tabla, ret_temp)
                ret_temp = tipo[1]
                tipo = tipo[0]
                generador.place_operation(comp, comp, 1, '+')
                generador.place_goto(w)
                generador.place_label(true_tag)
                ##aqui imprimir sin coma
                if type(x[0]) == type([]):
                    tipo = self.print_array(x, retorno, comp, tabla, ret_temp)
                    anterior = tipo[1]
                    tipo = tipo[0]
                else:
                    tipo = self.print_primitive(tipo, comp,  False, tabla, ret_temp)
                    anterior = tipo[1]
                    tipo = tipo[0]
                ##
                generador.set_unused_temp(ret_temp)
                generador.set_unused_temp(temp)
                generador.set_unused_temp(comp)
                #generamos ]
                temp_arr = generador.new_temporal()
                generador.place_operation(temp_arr, 'H', '', '')
                generador.insert_heap('H', 93)
                generador.next_heap()
                generador.insert_heap('H',-1)
                generador.next_heap()
                #unimos esto con lo anterior
                ret_temp = generador.new_temporal()
                generador.place_operation(ret_temp, 'P', tabla.size, '+')
                generador.place_operation(ret_temp, ret_temp, 1, '+')
                generador.insert_stack(ret_temp, anterior)
                generador.place_operation(ret_temp, ret_temp, 1, '+')
                generador.insert_stack(ret_temp, temp_arr)
                generador.set_unused_temp(temp_arr)
                generador.new_env(tabla.size)
                generador.call_function("concat_string")
                generador.get_stack(ret_temp, 'P')
                generador.return_evn(tabla.size)
                generador.set_unused_temp(anterior)
                ##
                return [tipo, ret_temp]
            else:
                tipo = self.print_primitive(x, variable,  True, tabla, anterior)
                ret_temp = tipo[1]
                return [x, ret_temp]
    
        
    def print_primitive(self,x, variable,  condicion, tabla, anterior=None):
        genAux = Generador()
        generador = genAux.get_instance()
        if x == Tipos.ENTERO:
            temp = generador.new_temporal()
            generador.get_heap(temp, variable)
            ### convertimos el valor en string
            generador.to_string_int()
            ret_temp = generador.new_temporal()
            generador.place_operation(ret_temp, 'P', tabla.size, '+')
            generador.place_operation(ret_temp, ret_temp, 1, '+')
            generador.insert_stack(ret_temp, temp)
            generador.new_env(tabla.size)
            generador.call_function("to_string_int")
            generador.get_stack(temp, 'P')
            generador.return_evn(tabla.size)
            ### 
            ## Concatenamos el valor int con el anterior si existe
            if anterior is not None:
                ret_temp = generador.new_temporal()
                generador.place_operation(ret_temp, 'P', tabla.size, '+')
                generador.place_operation(ret_temp, ret_temp, 1, '+')
                generador.insert_stack(ret_temp, anterior)
                generador.place_operation(ret_temp, ret_temp, 1, '+')
                generador.insert_stack(ret_temp, temp)
                generador.set_unused_temp(temp)
                generador.new_env(tabla.size)
                generador.call_function("concat_string")
                generador.get_stack(ret_temp, 'P')
                generador.return_evn(tabla.size)
                generador.set_unused_temp(anterior)
            else:
                ret_temp = temp
            ##
            if condicion:
                anterior = ret_temp
                #generamos la ,
                temp_arr = generador.new_temporal()
                generador.place_operation(temp_arr, 'H', '', '')
                generador.insert_heap('H', 44)
                generador.next_heap()
                generador.insert_heap('H',-1)
                generador.next_heap()
                #combinamos con el anterior
                ret_temp = generador.new_temporal()
                generador.place_operation(ret_temp, 'P', tabla.size, '+')
                generador.place_operation(ret_temp, ret_temp, 1, '+')
                generador.insert_stack(ret_temp, anterior)
                generador.place_operation(ret_temp, ret_temp, 1, '+')
                generador.insert_stack(ret_temp, temp_arr)
                generador.set_unused_temp(anterior)
                generador.set_unused_temp(temp_arr)
                generador.new_env(tabla.size)
                generador.call_function("concat_string")
                generador.get_stack(ret_temp, 'P')
                generador.return_evn(tabla.size)
            generador.set_unused_temp(temp)
        elif x == Tipos.STRING:
            generador.place_print('c', 34)
            heap = generador.new_temporal()
            generador.get_heap(heap, variable)
            generador.F_print()
            temp = generador.new_temporal()
            generador.place_operation(temp, "P",tabla.size,"+")
            generador.place_operation(temp, temp,"1","+")
            generador.insert_stack(temp, heap)
            generador.set_unused_temp(heap)
            generador.new_env(tabla.size)
            generador.call_function("F_print")
            temp3 = generador.new_temporal()
            generador.get_stack(temp3, 'P')
            generador.return_evn(tabla.size)
            generador.set_unused_temp(temp)
            generador.set_unused_temp(temp3)
            generador.place_print('c', 34)
            if condicion:
                generador.place_print('c', 44)
        elif x == Tipos.FLOAT:
            temp = generador.new_temporal()
            generador.get_heap(temp, variable)
            ### convertimos el valor en string
            generador.to_string_float()
            ret_temp = generador.new_temporal()
            generador.place_operation(ret_temp, 'P', tabla.size, '+')
            generador.place_operation(ret_temp, ret_temp, 1, '+')
            generador.insert_stack(ret_temp, temp)
            generador.new_env(tabla.size)
            generador.call_function("to_string")
            generador.get_stack(temp, 'P')
            generador.return_evn(tabla.size)
            ### 
            ## Concatenamos el valor int con el anterior si existe
            if anterior is not None:
                ret_temp = generador.new_temporal()
                generador.place_operation(ret_temp, 'P', tabla.size, '+')
                generador.place_operation(ret_temp, ret_temp, 1, '+')
                generador.insert_stack(ret_temp, anterior)
                generador.place_operation(ret_temp, ret_temp, 1, '+')
                generador.insert_stack(ret_temp, temp)
                generador.set_unused_temp(temp)
                generador.new_env(tabla.size)
                generador.call_function("concat_string")
                generador.get_stack(ret_temp, 'P')
                generador.return_evn(tabla.size)
                generador.set_unused_temp(anterior)
            else:
                ret_temp = temp
            ##
            if condicion:
                anterior = ret_temp
                #generamos la ,
                temp_arr = generador.new_temporal()
                generador.place_operation(temp_arr, 'H', '', '')
                generador.insert_heap('H', 44)
                generador.next_heap()
                generador.insert_heap('H',-1)
                generador.next_heap()
                #combinamos con el anterior
                ret_temp = generador.new_temporal()
                generador.place_operation(ret_temp, 'P', tabla.size, '+')
                generador.place_operation(ret_temp, ret_temp, 1, '+')
                generador.insert_stack(ret_temp, anterior)
                generador.place_operation(ret_temp, ret_temp, 1, '+')
                generador.insert_stack(ret_temp, temp_arr)
                generador.set_unused_temp(anterior)
                generador.set_unused_temp(temp_arr)
                generador.new_env(tabla.size)
                generador.call_function("concat_string")
                generador.get_stack(ret_temp, 'P')
                generador.return_evn(tabla.size)
            generador.set_unused_temp(temp)
            
        elif x == Tipos.BOOL:
            temp = generador.new_temporal()
            generador.get_heap(temp, variable)
            aux = generador.new_label()
            true_flag = generador.new_label()
            false_flag = generador.new_label()
            generador.place_if(temp, 1, '==', true_flag)
            generador.place_goto(false_flag)
            generador.place_label(true_flag)
            generador.print_true()
            generador.place_goto(aux)
            generador.place_label(false_flag)
            generador.print_false()
            generador.place_label(aux)
            if condicion:
                generador.place_print('c', 44)
            generador.set_unused_temp(temp)
        elif x == Tipos.CHAR:
            #generamos '
            temp_arr = generador.new_temporal()
            generador.place_operation(temp_arr, 'H', '', '')
            generador.insert_heap('H', 39)
            generador.next_heap()
            generador.insert_heap('H',-1)
            generador.next_heap()
            ## Concatenamos el valor char con el anterior si existe
            if anterior is not None:
                ret_temp = generador.new_temporal()
                generador.place_operation(ret_temp, 'P', tabla.size, '+')
                generador.place_operation(ret_temp, ret_temp, 1, '+')
                generador.insert_stack(ret_temp, anterior)
                generador.place_operation(ret_temp, ret_temp, 1, '+')
                generador.insert_stack(ret_temp, temp_arr)
                generador.set_unused_temp(temp_arr)
                generador.new_env(tabla.size)
                generador.call_function("concat_string")
                generador.get_stack(ret_temp, 'P')
                generador.return_evn(tabla.size)
            else:
                ret_temp = temp_arr
                
            anterior = ret_temp
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
            generador.place_operation(ret_temp, 'P', tabla.size, '+')
            generador.place_operation(ret_temp, ret_temp, 1, '+')
            generador.insert_stack(ret_temp, anterior)
            generador.place_operation(ret_temp, ret_temp, 1, '+')
            generador.insert_stack(ret_temp, temp_arr)
            generador.set_unused_temp(temp_arr)
            generador.new_env(tabla.size)
            generador.call_function("concat_string")
            generador.get_stack(ret_temp, 'P')
            generador.return_evn(tabla.size)
            generador.set_unused_temp(anterior)
            #generamos '
            anterior = ret_temp
            temp_arr = generador.new_temporal()
            generador.place_operation(temp_arr, 'H', '', '')
            generador.insert_heap('H', 39)
            generador.next_heap()
            generador.insert_heap('H',-1)
            generador.next_heap()
            ret_temp = generador.new_temporal()
            generador.place_operation(ret_temp, 'P', tabla.size, '+')
            generador.place_operation(ret_temp, ret_temp, 1, '+')
            generador.insert_stack(ret_temp, anterior)
            generador.place_operation(ret_temp, ret_temp, 1, '+')
            generador.insert_stack(ret_temp, temp_arr)
            generador.set_unused_temp(temp_arr)
            generador.new_env(tabla.size)
            generador.call_function("concat_string")
            generador.get_stack(ret_temp, 'P')
            generador.return_evn(tabla.size)
            generador.set_unused_temp(anterior)
            ##
            if condicion:
                anterior = ret_temp
                #generamos la ,
                temp_arr = generador.new_temporal()
                generador.place_operation(temp_arr, 'H', '', '')
                generador.insert_heap('H', 44)
                generador.next_heap()
                generador.insert_heap('H',-1)
                generador.next_heap()
                #combinamos con el anterior
                ret_temp = generador.new_temporal()
                generador.place_operation(ret_temp, 'P', tabla.size, '+')
                generador.place_operation(ret_temp, ret_temp, 1, '+')
                generador.insert_stack(ret_temp, anterior)
                generador.place_operation(ret_temp, ret_temp, 1, '+')
                generador.insert_stack(ret_temp, temp_arr)
                generador.set_unused_temp(temp_arr)
                generador.new_env(tabla.size)
                generador.call_function("concat_string")
                generador.get_stack(ret_temp, 'P')
                generador.return_evn(tabla.size)
                generador.set_unused_temp(anterior)
            generador.set_unused_temp(temp)
        elif x == Tipos.NOTHING:
            generador.nothing()
        return [x, ret_temp]
    
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