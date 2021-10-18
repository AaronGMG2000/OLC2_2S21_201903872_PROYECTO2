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
                        print(retorno.descripcion)
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
                    elif retorno.type == Tipos.ARRAY:
                        generador.comment("inicio de impresión array")
                        self.print_multi_array(retorno.types, retorno.value, tabla)
                        generador.comment("final de impresión array")
                    
                    if retorno.is_temporal:
                        generador.set_unused_temp(retorno.value)
        genAux = Generador()
        generador = genAux.get_instance()             
        if self.println:
            if isinstance(generador, Generador):
                generador.place_print('c',ord('\n'))
        generador.set_anterior()              
    
    def print_multi_array(self, types, variable, tabla):
        genAux = Generador()
        generador = genAux.get_instance()
        if type(types) == type([]):
            temp = generador.new_temporal()
            generador.place_operation(temp, variable, 1, '+')
            a = 1
            generador.place_print('c', 91)
            generador.comment("inicio de impresión array interno")
            for x in types:
                vari = generador.new_temporal()
                generador.get_heap(vari,temp)
                if a != len(types):
                    if type(x) == type([]):
                        self.print_multi_array(x, vari, tabla)
                        generador.place_print("c","44")
                    else:
                        self.print_primitive(x, vari, True, tabla)
                else:
                    if type(x) == type([]):
                        self.print_multi_array(x, vari, tabla)
                    else:
                        self.print_primitive(x, vari, False, tabla)
                a = a + 1
                generador.set_unused_temp(vari)
                generador.place_operation(temp, temp, 1, '+')
            generador.place_print('c', 93)
            generador.comment("Fin de impresión array interno")

    def print_primitive(self,x, variable,  condicion, tabla):
        genAux = Generador()
        generador = genAux.get_instance()
        if x == Tipos.ENTERO:
            generador.place_print('d', variable)
            if condicion:
                generador.place_print('c', 44)
        elif x == Tipos.STRING:
            generador.place_print('c', 34)
            generador.F_print()
            temp = generador.new_temporal()
            generador.place_operation(temp, "P",tabla.size,"+")
            generador.place_operation(temp, temp,"1","+")
            generador.insert_stack(temp, variable)
            generador.set_unused_temp(variable)
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
            generador.place_print('f', variable)
            if condicion:
                generador.place_print('c', 44)
            
        elif x == Tipos.BOOL:
            aux = generador.new_label()
            true_flag = generador.new_label()
            false_flag = generador.new_label()
            generador.place_if(variable, 1, '==', true_flag)
            generador.place_goto(false_flag)
            generador.place_label(true_flag)
            generador.print_true()
            generador.place_goto(aux)
            generador.place_label(false_flag)
            generador.print_false()
            generador.place_label(aux)
            if condicion:
                generador.place_print('c', 44)
        elif x == Tipos.CHAR:
            generador.place_print('c', 39)
            generador.place_print('c', variable)
            generador.place_print('c', 39)
            if condicion:
                generador.place_print('c', 44)
        elif x == Tipos.NOTHING:
            generador.nothing()
    

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