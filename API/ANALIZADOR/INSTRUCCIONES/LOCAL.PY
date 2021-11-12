from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.table import Tabla
from ..GENERAL.Tipo import CICLICO, Tipos
from ..GENERAL.error import Error
from ..GENERAL.generator import Generador

class LOCAL(Instruccion):

    def __init__(self, id, fila, columna, expresion = None, tipo = None):
        super().__init__(CICLICO.BREAK, fila, columna)
        self.id = id
        self.expresion = expresion
        self.tipoA = tipo

    def Ejecutar(self, arbol: Arbol, tabla: Tabla):
        genAux = Generador()
        generador = genAux.get_instance()
        if isinstance(generador, Generador):
            try:
                variable = tabla.variables[self.id]
                generador.error_code()
                return Error("Sintactico", "La variable ya existe en el entorno", self.row, self.column)
            except:
                if self.expresion is not None:
                    exp = self.expresion.Ejecutar(arbol, tabla)
                    if isinstance(exp, Error):
                        generador.error_code()
                        return exp
                    if self.tipoA is not None:
                        if (self.expresion.type != self.tipoA and self.expresion.types != self.tipoA 
                            and self.expresion.struct_type != self.tipoA and exp.type != self.tipoA
                            and exp.types != self.tipoA and exp.auxiliar_type!= self.tipoA):
                            generador.error_code()
                            return Error("Sintactico", "El tipo ingresado no coincide con el solicitado", self.row, self.column)
                    generador.insert_stack(tabla.size, exp.value)
                    self.type = exp.type
                    tabla.set_variable(arbol, self.row, self.column, self.id, self.type, False)
                    variable = tabla.get_variable(self.id)
                    variable.types = exp.types
                    if type(exp.auxiliar_type) == type(""):
                        variable.struct_type = exp.auxiliar_type
                        variable.type = Tipos.OBJECT
                    elif type(exp.auxiliar_type) == type([]):
                        variable.types = exp.auxiliar_type
                        variable.type = Tipos.STRUCT
                    else:
                        variable.auxiliar_type = exp.auxiliar_type
                    generador.set_unused_temp(exp.value)
                else:
                    tabla.set_variable(arbol, self.row, self.column, self.id, Tipos.NOTHING, False)
                generador.set_anterior()
                
    def getNodo(self) -> NodoAST:
        nodo = NodoAST('GLOBAL')
        nodo.agregarHijo("global")
        nodo.agregarHijo(self.id)
        if self.expresion is not None:
            nodo.agregarHijo("=")
            nodo.agregarHijoNodo(self.expresion.getNodo())
            if self.tipo is not None:
                nodo.agregarHijo("::")
                if self.tipo.value == Tipos.OBJECT:
                    nodo.agregarHijo(Tipos.STRUCT.value)
                else:
                    nodo.agregarHijo(self.tipo.value)
        nodo.agregarHijo(";")
        return nodo