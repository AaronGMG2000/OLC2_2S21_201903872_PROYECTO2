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

class Asignar_Variable(Instruccion):

    def __init__(self, id,expresion, fila, columna, required_type=None):
        super().__init__(Tipos.STRING, fila, columna)
        self.id = id
        self.expresion = expresion
        self.required_type = required_type
        
    def Ejecutar(self, arbol: Arbol, tabla: Tabla):
        genAux = Generador()
        generador = genAux.get_instance()
        if isinstance(generador, Generador):
            generador.comment("Asignación de variable "+self.id)
            if isinstance(self.expresion, Instruccion):
                valor = self.expresion.Ejecutar(arbol, tabla)
                if isinstance(valor, Error):
                    return valor
                if self.expresion.type != self.required_type and self.required_type != None:
                    return Error("Sintactico", "Se esperaba un valor tipo "+self.required_type.value+" y se obtuvo un valor tipo "+self.expresion.type.value, self.row, self.column)
                self.type = self.expresion.type
                if tabla.get_variable(self.id) == None:
                    if tabla.previous == None:
                        generador.insert_stack(tabla.size, valor.value)
                    else:
                        temp = generador.new_temporal()
                        generador.place_operation(temp, "P", tabla.size, '+')
                        generador.insert_stack(temp, valor.value)
                        generador.set_unused_temp(temp)
                    tabla.set_variable(self.id, self.expresion.type, False)
                    variable = tabla.get_variable(self.id)
                    variable.setValor(valor.valor)
                    if self.type == Tipos.ARRAY:
                        variable.types = self.expresion.types
                    variable.aux_type = valor.auxiliar_type
                    if valor.is_temporal:
                        generador.set_unused_temp(valor.value)
                else:
                    variable = tabla.get_variable(self.id)
                    if isinstance(variable, Simbolo):
                        if tabla.previous == None:
                            generador.insert_stack(variable.position, valor.value)
                        else:
                            temp = generador.new_temporal()
                            generador.place_operation(temp, "P", variable.position, '+')
                            generador.insert_stack(temp, valor.value)
                            generador.set_unused_temp(temp)
                        variable.type = self.expresion.type
                        if self.expresion.type == Tipos.STRING:
                            variable.in_Heap = True
                        else:
                            variable.in_Heap = False
                        if valor.is_temporal:
                            generador.set_unused_temp(valor.value)
                        variable.setValor(valor.valor)
                        if self.type == Tipos.ARRAY:
                            variable.types = self.expresion.types
                        variable.aux_type = valor.auxiliar_type
                generador.set_anterior()
                generador.comment("Terminando asignación de variable "+self.id)
                
                
                                          
    
    
        
    def getNodo(self) -> NodoAST:
        nodo = NodoAST('PRINT')
        
        return nodo