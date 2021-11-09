import re
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

class Variable(Instruccion):

    def __init__(self, id, fila, columna):
        super().__init__(Tipos.STRING, fila, columna)
        self.id = id
        self.types = None
        
    def Ejecutar(self, arbol: Arbol, tabla: Tabla):
        genAux = Generador()
        generador = genAux.get_instance()
        if isinstance(generador, Generador):
            valor = tabla.get_variable(self.id)
            if  isinstance(valor, Simbolo):
                temp_stack = generador.new_temporal()
                self.type = valor.type
                if tabla.previous == None or valor.is_global:
                    generador.get_stack(temp_stack, valor.position)
                else:
                    temp = generador.new_temporal()
                    if generador.in_function:
                        anterio = tabla
                        if tabla.name == "WHILE" or tabla.name == "FOR":
                            while (anterio.name == "WHILE" or anterio.name == "FOR"):
                                anterio = anterio.previous
                        resta = anterio.previous.size + generador.count_save
                        resta = valor.position- resta
                        if resta < 0 and generador.count_save == 0:
                            resta = 0
                        if resta < 0:
                            generador.place_operation(temp, 'P', resta, '')
                        else:
                            generador.place_operation(temp, 'P', resta, '+')
                    else:
                        if tabla.previous == arbol.global_table:
                            generador.place_operation(temp, 'P', valor.position,'+')
                        else:
                            resta = valor.position - generador.count_save
                            if resta < 0:
                                generador.place_operation(temp, 'P', resta,'')
                            else:
                                generador.place_operation(temp, 'P', resta,'+')
                    generador.get_stack(temp_stack, temp)
                    generador.set_unused_temp(temp)
                ret = Retorno(temp_stack, self.type, True)
                ret.valor = valor.getValor()
                ret.types = valor.types
                self.types = valor.types
                ret.auxiliar_type = valor.auxiliar_type
                self.struct_type = valor.struct_type
                return ret
            else:
                return Error("Sintactico","La variable indicada no existe", self.row, self.column)
                                          
    
    
        
    def getNodo(self) -> NodoAST:
        nodo = NodoAST('PRINT')
        
        return nodo