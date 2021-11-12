from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.table import Tabla
from ..GENERAL.Tipo import CICLICO, Tipos
from ..GENERAL.error import Error
from ..GENERAL.generator import Generador

class TGLOBAL(Instruccion):

    def __init__(self, id, fila, columna, expresion = None, tipo = None):
        super().__init__(CICLICO.BREAK, fila, columna)
        self.id = id
        self.expresion = expresion
        self.tipoA = tipo

    def Ejecutar(self, arbol: Arbol, tabla: Tabla):
        genAux = Generador()
        generador = genAux.get_instance()
        if isinstance(generador, Generador):
            variable = arbol.global_table.get_variable(self.id)
            if variable is None:
                generador.error_code()
                return Error("Sintactico", "La variable no existe en el entorno global", self.row, self.column)
            if tabla.previous is None:
                generador.error_code()
                return Error("Sintactico", "Global no puede ser utilizado en el entorno global", self.row, self.column)
            try:
                var = tabla.variables[self.id]
                generador.error_code()
                return Error("La variable ya existe en el entorno actual")
            except:
                tabla.variables[self.id] = variable
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
                    variable.types = exp.types
                    if type(exp.auxiliar_type) == type(""):
                        variable.struct_type = exp.auxiliar_type
                        variable.type = Tipos.OBJECT
                    elif type(exp.auxiliar_type) == type([]):
                        variable.types = exp.auxiliar_type
                        variable.type = Tipos.STRUCT
                    else:
                        variable.auxiliar_type = exp.auxiliar_type
                    generador.insert_stack(variable.position, exp.value)
                    generador.set_unused_temp(exp.value)
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