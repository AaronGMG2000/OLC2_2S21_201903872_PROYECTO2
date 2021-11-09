from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.table import Tabla
from ..GENERAL.Tipo import Tipos
from ..GENERAL.error import Error
from ..ABSTRACT.Retorno import Retorno
from ..GENERAL.generator import Generador

class Rango(Instruccion):

    def __init__(self, valor1, valor2, fila, columna):
        super().__init__(Tipos.RANGE, fila, columna)
        self.valor1 = valor1
        self.valor2 = valor2
        self.types = []
        
    def getNodo(self) -> NodoAST:
        nodo = NodoAST('RANGE')
        nodo.agregarHijoNodo(self.valor1.getNodo())
        nodo.agregarHijo(":")
        nodo.agregarHijoNodo(self.valor2.getNodo())
        return nodo

    def Ejecutar(self, arbol: Arbol, tabla: Tabla):
        genAux = Generador()
        generador = genAux.get_instance()
        if self.valor1 == None and self.valor2 == None:
            ret = generador.new_temporal()
            generador.place_operation(ret,'H', '','')
            generador.insert_heap('H',-1)
            generador.next_heap()
            generador.insert_heap('H',-1)
            return Retorno(ret, self.type, True)
        v1 = self.valor1.Ejecutar(arbol, tabla)
        if isinstance(v1, Error): return v1
        v2 = self.valor2.Ejecutar(arbol, tabla)
        if isinstance(v2, Error): return v2
        if self.valor1.type!=Tipos.FLOAT and self.valor1.type!=Tipos.ENTERO:
            return Error("Sintactico","El rango unicamente puede tener valores numericos",self.fila, self.columna)
        if self.valor2.type!=Tipos.FLOAT and self.valor2.type!=Tipos.ENTERO:
            return Error("Sintactico","El rango unicamente puede tener valores numericos",self.fila, self.columna)
        ret = generador.new_temporal()
        generador.place_operation(ret,'H', '','')
        generador.insert_heap('H',v1.value)
        generador.next_heap()
        generador.insert_heap('H',v2.value)
        generador.next_heap()
        if v1.type == Tipos.FLOAT or v2.type == Tipos.FLOAT:
            aux_type = Tipos.FLOAT
        else:
            aux_type = Tipos.ENTERO
        generador.set_unused_temp(v1.value)
        generador.set_unused_temp(v2.value)
        return Retorno(ret, self.type, True, aux_type)