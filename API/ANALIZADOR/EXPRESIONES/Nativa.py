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
                ret.valor = eval(inst[0])
                return ret
            except:
                return Error('Semantico', 'Error en la función '+self.Nativa.value.lower(), self.row, self.column)
                
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