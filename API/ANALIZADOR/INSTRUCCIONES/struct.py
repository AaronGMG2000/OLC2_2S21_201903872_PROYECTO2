from ..GENERAL.Simbolo import Simbolo
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.table import Tabla
from ..GENERAL.Tipo import Tipos
from ..GENERAL.error import Error
from ..GENERAL.generator import Generador
from ..ABSTRACT.Retorno import Retorno

class STRUCT(Instruccion):

    def __init__(self, id, parametros,row, column, mutable=False):
        super().__init__(Tipos.STRUCT, row, column)
        self.id = id
        self.parametros = parametros
        self.mutable = mutable
        
    def Ejecutar(self, arbol: Arbol, tabla: Tabla):
        genAux = Generador()
        generador = genAux.get_instance()
        variable = tabla.get_variable(self.id)
        content = {1:self.id, 2: self.mutable}
        a = 0
        if variable is None:
            for par in self.parametros:#tipo, nombre_struct, tipo_obligatorio, posicion
                if type(par[1]) == type(""):
                    objeto = tabla.get_variable(par[1])
                    if objeto == None and par[1]!=self.id:
                        generador.error_code()
                        return Error("Sintactico", "El tipo Struct indicado no existe", self.row, self.column)
                    content[par[0]] = [Tipos.OBJECT, par[1], Tipos.OBJECT, a, False]
                else:
                    content[par[0]] = [par[1], None, par[1], a, False]
                a = a + 1
            tabla.set_variable(self.id, self.type, False)
            self.struct_type = self.id
            var = tabla.get_variable(self.id)
            tabla.size -=1
            if isinstance(var, Simbolo):
                var.value = content
                var.struct_type = self.id
            generador.set_anterior()
            return content
        else:
            generador.error_code()
            return Error("Sintactico","No se puede crear un Struct con ese nombre debido que ya hay una variable asignada", self.row, self.column)
        
    def getNodo(self) -> NodoAST:
        nodo = NodoAST("STRUCT")
        if self.mutable:
            nodo.agregarHijo("MUTABLE")
        nodo.agregarHijo("STRUCT")
        nodo.agregarHijo(self.id)
        para = None
        anterior = None
        for par in self.parametros:
            para = NodoAST("PARAMETROS")
            tipo = NodoAST("TIPO")
            nid = NodoAST("ID")
            if anterior!=None:
                para.agregarHijoNodo(anterior)
            nid.agregarHijo(par[0])
            para.agregarHijoNodo(nid)
            if par[1] !=None:
                para.agregarHijo(":")
                para.agregarHijo(":")
                tipo.agregarHijo(par[1].value)
                para.agregarHijoNodo(tipo)
            para.agregarHijo(";")
            anterior = para
        nodo.agregarHijoNodo(para)
        nodo.agregarHijo("end")
        nodo.agregarHijo(";")    
        return nodo
    
    