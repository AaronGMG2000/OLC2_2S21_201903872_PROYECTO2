from typing import Dict, List

from ..GENERAL.generator import Generador

from ..ABSTRACT.Retorno import Retorno
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.table import Tabla
from ..GENERAL.Tipo import Tipos
from ..GENERAL.error import Error
from ..GENERAL.Simbolo import Simbolo

class Imprimir(Instruccion):

    def __init__(self, expresion: List, println, fila, columna):
        super().__init__(Tipos.STRING, fila, columna)
        self.expresion = expresion
        self.println = println
        
    def Ejecutar(self, arbol: Arbol, tabla: Tabla):
        for exp in self.expresion:
            genAux = Generador()
            generador = genAux.get_instance()
            if isinstance(generador, Generador):
                if isinstance(exp, Instruccion):
                    retorno = exp.Ejecutar(arbol, tabla)
                    if isinstance (retorno, Error):
                        generador.error_code()
                        return retorno
                    if retorno.type == Tipos.ENTERO:
                        generador.place_print('d', retorno.value)
                    
                    elif retorno.type == Tipos.FLOAT:
                        generador.place_print('f', retorno.value)
                        
                    elif retorno.type == Tipos.CHAR:
                        generador.place_print('c', retorno.value)
                        
                    elif retorno.type == Tipos.NOTHING:
                        generador.nothing()
                          
                    elif retorno.type == Tipos.BOOL:
                        if retorno.is_temporal:
                            true_tag = generador.new_label()
                            false_tag = generador.new_label()
                            exit = generador.new_label()
                            generador.place_if(retorno.value, 1, '==', true_tag)
                            generador.place_goto(false_tag)
                            generador.place_label(true_tag)
                            generador.print_true()
                            generador.place_goto(exit)
                            generador.place_label(false_tag)
                            generador.print_false()
                            generador.place_label(exit)
                        else:
                            etiqueta_temporal = generador.new_label()
                            generador.place_label(retorno.true_tag)
                            generador.print_true()
                            generador.place_goto(etiqueta_temporal)
                            generador.place_label(retorno.false_tag)
                            generador.print_false()
                            generador.place_label(etiqueta_temporal)
                        
                    elif retorno.type == Tipos.STRING:
                        generador.F_print()
                        temp = generador.new_temporal()
                        generador.place_operation(temp, "P",tabla.size,"+")
                        generador.place_operation(temp, temp,"1","+")
                        generador.insert_stack(temp, retorno.value)
                        generador.set_unused_temp(retorno.value)
                        generador.new_env(tabla.size)
                        generador.call_function("F_print")
                        temp3 = generador.new_temporal()
                        generador.get_stack(temp3, 'P')
                        generador.return_evn(tabla.size)
                        generador.set_unused_temp(temp)
                        generador.set_unused_temp(temp3)
                        continue
                    elif retorno.type == Tipos.RANGE:
                        aux = retorno.auxiliar_type
                        t1 = generador.new_temporal()
                        generador.get_heap(t1, retorno.value)
                        if aux == Tipos.ENTERO:
                            generador.place_print('d', t1)
                        else:
                            generador.place_print('f', t1)
                        generador.place_print('c', ord(':'))
                        generador.place_operation(retorno.value, retorno.value, 1, '+')
                        generador.get_heap(t1, retorno.value)
                        if aux == Tipos.ENTERO:
                            generador.place_print('d', t1)
                        else:
                            generador.place_print('f', t1)
                        generador.set_unused_temp(retorno.value)
                        generador.set_unused_temp(t1)
                        continue
                    elif retorno.type == Tipos.ARRAY:
                        self.array(retorno, tabla)
                    elif retorno.type == Tipos.STRUCT:
                        generador.F_print()
                        temp = generador.new_temporal()
                        generador.place_operation(temp, 'H', '', '')
                        for x in retorno.valor[1]:
                            generador.insert_heap('H', ord(x))
                            generador.next_heap()
                        generador.insert_heap('H',-1)
                        generador.next_heap()
                        temp2 = generador.new_temporal()
                        generador.place_operation(temp2, 'P', tabla.size, '+')
                        generador.place_operation(temp2, temp2, 1, '+')
                        generador.insert_stack(temp2, temp)
                        generador.new_env(tabla.size)
                        generador.call_function("F_print")
                        generador.return_evn(tabla.size)
                        generador.set_unused_temp(temp)
                        generador.set_unused_temp(temp2)
                    elif type(retorno.type) == type(""):
                        self.print_object(retorno.valor, retorno.value, tabla)
                    elif retorno.type == Tipos.OBJECT:
                        self.print_object(retorno.valor, retorno.value, tabla)
                    if retorno.is_temporal:
                        generador.set_unused_temp(retorno.value)
        genAux = Generador()
        generador = genAux.get_instance()             
        if self.println:
            if isinstance(generador, Generador):
                generador.place_print('c',ord('\n'))
        generador.set_anterior()              
    
    def array(self, retorno, tabla):
        genAux = Generador()
        generador = genAux.get_instance()
        generador.comment("inicio de impresión array")
        heap = generador.new_temporal()
        temp = generador.new_temporal()
        size = generador.new_temporal()
        generador.get_heap(heap, retorno.value)
        generador.place_operation(size, heap, retorno.value, '+')
        generador.place_operation(temp, size, '1', '-')
        generador.place_print('c', 91)
        w = generador.new_label()
        true_tag = generador.new_label()
        comp = generador.new_temporal()
        generador.place_operation(comp, retorno.value, '1','+')
        generador.set_unused_temp(retorno.value)
        generador.set_unused_temp(heap)
        generador.set_unused_temp(size)
        generador.place_label(w)
        generador.place_if(comp, temp, '>', true_tag)
        tipo = self.print_array(retorno.types, retorno, comp, tabla)
        generador.place_operation(comp, comp, 1, '+')
        if type(retorno.types[0]) == type([]):
            generador.place_print('c', 44)
        generador.place_goto(w)
        generador.place_label(true_tag)
        if type(retorno.types[0]) == type([]):
            tipo = self.print_array(retorno.types, retorno, comp, tabla)
        else:
            if tipo == Tipos.OBJECT or type(tipo) == type(""):
                struct = tabla.get_variable(tipo)
                if isinstance(struct, Simbolo):
                    temp2 = generador.new_temporal()
                    generador.get_heap(temp2, comp)
                    self.print_object(struct.value, temp2, tabla, True)
                    generador.set_unused_temp(temp2)
            else:
                tipo = self.print_primitive(tipo, comp,  False, tabla)
        generador.place_print('c', 93)
        generador.set_unused_temp(temp)
        generador.set_unused_temp(comp)
        generador.comment("final de impresión array")
    
    def print_array(self, types, retorno, variable, tabla, valor = None):
        genAux = Generador()
        generador = genAux.get_instance()
        for x in types:
            if type(x) == type([]):
                generador.comment("inicio de impresión array interno")
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
                generador.place_print('c', 91)
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
                    if tipo == Tipos.OBJECT or type(tipo) == type(""):
                        struct = tabla.get_variable(tipo)
                        if isinstance(struct, Simbolo):
                            temp2 = generador.new_temporal()
                            generador.get_heap(temp2, comp)
                            self.print_object(struct.value, temp2, tabla, True)
                            generador.set_unused_temp(temp2)
                    else:
                        self.print_primitive(tipo, comp,  False, tabla)
                ##
                generador.set_unused_temp(temp)
                generador.set_unused_temp(comp)
                generador.place_print('c', 93)
                generador.comment("fin de impresión array interno")
            else:
                if type(x)== type("") or x == Tipos.OBJECT:
                    struct = tabla.get_variable(x)
                    if isinstance(struct, Simbolo):
                        temp = generador.new_temporal()
                        generador.get_heap(temp, variable)
                        self.print_object(struct.value, temp, tabla, True)
                        generador.place_print('c', 44)
                        generador.set_unused_temp(temp)
                else:
                    self.print_primitive(x, variable,  True, tabla)
                return x
    
    def print_primitive(self,x, variable,  condicion, tabla):
        genAux = Generador()
        generador = genAux.get_instance()
        if x == Tipos.ENTERO:
            temp = generador.new_temporal()
            generador.get_heap(temp, variable)
            generador.place_print('d', temp)
            if condicion:
                generador.place_print('c', 44)
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
            generador.place_print('f', temp)
            if condicion:
                generador.place_print('c', 44)
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
            generador.place_print('c', 39)
            temp = generador.new_temporal()
            generador.get_heap(temp, variable)
            generador.place_print('c', temp)
            generador.place_print('c', 39)
            if condicion:
                generador.place_print('c', 44)
            generador.set_unused_temp(temp)
        elif x == Tipos.NOTHING:
            generador.nothing()
    
    def print_object(self, struct, retorno, tabla, array = False):
        genAux = Generador()
        generador = genAux.get_instance()
        dic:Dict = struct
        a = 1
        temp = generador.new_temporal()
        nombre = dic[1]
        for n in nombre:
            generador.place_print('c', ord(n))
        generador.place_print('c', ord('('))
        for key in  list(dic.keys()):
            if key == 1 or key == 2:
                continue
            lista = dic[key]
            if lista[2] == Tipos.OBJECT:
                if not lista[4] and not array:
                    if a < len(dic.keys())-2:
                        generador.place_operation(temp, retorno, lista[3], '+')
                        self.print_primitive(Tipos.NOTHING, temp,  True, tabla)
                    else:
                        generador.place_operation(temp, retorno, lista[3], '+')
                        self.print_primitive(Tipos.NOTHING, temp,  False, tabla)
                else:
                    generador.place_operation(temp, retorno, lista[3], '+')
                    generador.get_heap(temp, temp)
                    true_tag = None
                    exit = None
                    if array:
                        exit = generador.new_label()
                        true_tag = generador.new_label()
                        generador.place_if(temp, -1, '==', true_tag)
                        self.print_object(struct, temp, tabla)
                        generador.place_goto(exit)
                        generador.place_label(true_tag)
                        generador.nothing()
                        generador.place_label(exit)
                    else:
                        self.print_object(lista[4], temp, tabla)
                        
            else:
                if a < len(dic.keys())-2:
                    generador.place_operation(temp, retorno, lista[3], '+')
                    if type(lista[2]) == type([]):
                        generador.get_heap(temp, temp)
                        ret = Retorno(temp, Tipos.ARRAY, False)
                        ret.types = lista[2]
                        self.array(ret, tabla)
                    else:
                        self.print_primitive(lista[0], temp,  True, tabla)
                else:
                    generador.place_operation(temp, retorno, lista[3], '+')
                    if type(lista[2]) == type([]):
                        generador.get_heap(temp, temp)
                        ret = Retorno(temp, Tipos.ARRAY, False)
                        ret.types = lista[2]
                        self.array(ret, tabla)
                    else:
                        self.print_primitive(lista[0], temp,  False, tabla)
            a = a + 1
        generador.place_print('c', ord(')'))
        generador.set_unused_temp(temp)
    def getNodo(self) -> NodoAST:
        nodo = NodoAST('PRINT')
        nodo.agregarHijo('PRINT')
        nodo.agregarHijo('(')
        anterior = None
        nodoParametro = None
        for ex in self.expresion:
            nodoParametro = NodoAST("PARAMETROS")
            if anterior is not None:
                nodoParametro.agregarHijoNodo(anterior)
                nodoParametro.agregarHijo(',')
            nodoParametro.agregarHijoNodo(ex.getNodo())
            anterior = nodoParametro
        if nodoParametro is not None:
            nodo.agregarHijoNodo(nodoParametro)
        nodo.agregarHijo(')')
        return nodo