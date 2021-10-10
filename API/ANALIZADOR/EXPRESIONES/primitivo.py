from ..ABSTRACT.Retorno import Retorno
from ..GENERAL.generator import Generador
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.table import Tabla
from ..GENERAL.Tipo import Tipos


class Primitivo(Instruccion):

    def __init__(self, type:Tipos, value, row, column):
        super().__init__(type, row, column)
        self.value = value

    def getNodo(self) -> NodoAST:
        nodo = NodoAST('PRIMITIVO')
        nodo.agregarHijo(str(self.value))
        return nodo

    def Ejecutar(self, arbol: Arbol, tabla: Tabla):
        genAux = Generador()
        generador = genAux.get_instance()
        if isinstance(generador, Generador):
            if self.type == Tipos.ENTERO or self.type == Tipos.FLOAT:
                return Retorno(self.value, self.type, False)
            if self.type == Tipos.BOOL:
                if self.true_tag == '':
                    self.true_tag = generador.new_label()
                if self.false_tag == '':
                    self.false_tag = generador.new_label()

                return Retorno(self.value, self.type, False, None, self.true_tag, self.false_tag)
                
            if self.type == Tipos.STRING:
                temp_string = generador.new_temporal()
                generador.place_operation(temp_string, 'H', '', '') 
                for c in str(self.value):
                    generador.insert_heap('H', ord(c)) 
                    generador.next_heap()
                generador.insert_heap('H', -1)
                generador.next_heap()
                return Retorno(temp_string, self.type, True) 
            
            if self.type == Tipos.CHAR:
                return Retorno(ord(self.value), self.type, False)
            if self.type == Tipos.NOTHING:
                return Retorno("nothing", self.type, False)
