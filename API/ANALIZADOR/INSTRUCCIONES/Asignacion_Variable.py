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
                    generador.error_code()
                    return valor
                if type(self.required_type) == type([]):
                    if self.expresion.types != self.required_type:
                        generador.error_code()
                        return Error("Sintactico", "tipo de Arreglo Invalido", self.row, self.column)
                elif type(self.required_type) == type(""):
                    if self.expresion.struct_type != self.required_type and self.expresion.type != self.required_type:
                        generador.error_code()
                        return Error("Sintactico", "Se esperaba un valor tipo "+self.required_type+" y se obtuvo un valor tipo "+self.expresion.type.value, self.row, self.column)
                elif self.expresion.type != self.required_type and self.required_type != None:
                    generador.error_code()
                    return Error("Sintactico", "Se esperaba un valor tipo "+self.required_type.value+" y se obtuvo un valor tipo "+self.expresion.type.value, self.row, self.column)
                self.type = self.expresion.type
                if tabla.get_variable(self.id) == None:
                    if tabla.previous == None:
                        if valor.type == Tipos.BOOL and not valor.is_temporal:
                            exit = generador.new_label()
                            generador.place_label(valor.true_tag)
                            generador.insert_stack(tabla.size, 1)
                            generador.place_goto(exit)
                            generador.place_label(valor.false_tag)
                            generador.insert_stack(tabla.size, 0)
                            generador.place_label(exit)
                        else:
                            generador.insert_stack(tabla.size, valor.value)
                    else:
                        temp = generador.new_temporal()
                        resta = tabla.size - generador.count_save
                        if resta<0:
                            generador.place_operation(temp, "P", resta, '')
                        else:
                            generador.place_operation(temp, "P", resta, '+')
                        generador.insert_stack(temp, valor.value)
                        generador.set_unused_temp(temp)
                    tabla.set_variable(self.id, self.expresion.type, False)
                    variable = tabla.get_variable(self.id)
                    variable.setValor(valor.valor)
                    if self.type == Tipos.ARRAY:
                        variable.types = self.expresion.types
                    variable.auxiliar_type = valor.auxiliar_type
                    if valor.is_temporal:
                        generador.set_unused_temp(valor.value)
                    if self.type == Tipos.OBJECT:
                        variable.struct_type = self.expresion.struct_type
                else:
                    variable = tabla.get_variable(self.id)
                    if isinstance(variable, Simbolo):
                        if tabla.previous == None  or variable.is_global:
                            if valor.type == Tipos.BOOL and not valor.is_temporal:
                                exit = generador.new_label()
                                generador.place_label(valor.true_tag)
                                generador.insert_stack(variable.position, 1)
                                generador.place_goto(exit)
                                generador.place_label(valor.false_tag)
                                generador.insert_stack(variable.position, 0)
                                generador.place_label(exit)
                            else:
                                generador.insert_stack(variable.position, valor.value)
                        else:
                            temp = generador.new_temporal()
                            resta = variable.position - generador.count_save
                            if resta < 0:
                                generador.place_operation(temp, 'P', resta,'')
                            else:
                                generador.place_operation(temp, 'P', resta,'+')
                            generador.insert_stack(temp, valor.value)
                            generador.set_unused_temp(temp)
                        variable.type = self.expresion.type
                        variable.auxiliar_type = valor.auxiliar_type
                        if valor.is_temporal:
                            generador.set_unused_temp(valor.value)
                        variable.setValor(valor.valor)
                        if self.type == Tipos.ARRAY:
                            variable.types = self.expresion.types
                        if self.type == Tipos.OBJECT:
                            variable.struct_type = self.expresion.struct_type
                generador.set_unused_temp(valor.value)
                generador.comment("Terminando asignación de variable "+self.id)
                generador.set_anterior()
                
                                          
    
    
        
    def getNodo(self) -> NodoAST:
        nodo = NodoAST('PRINT')
        
        return nodo