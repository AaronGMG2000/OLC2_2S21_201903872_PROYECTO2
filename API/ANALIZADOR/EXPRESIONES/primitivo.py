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
                ret = Retorno(self.value, self.type, False)
                ret.valor = self.value
                return ret
            if self.type == Tipos.BOOL:
                if self.true_tag == '':
                    self.true_tag = generador.new_label()
                if self.false_tag == '':
                    self.false_tag = generador.new_label()
                
                if self.value:
                    generador.place_goto(self.true_tag)
                    generador.place_goto(self.false_tag)
                else:
                    generador.place_goto(self.false_tag)
                    generador.place_goto(self.true_tag)
                ret = Retorno(None, self.type, False, None, self.true_tag, self.false_tag)
                ret.valor = self.value
                return ret
                
            if self.type == Tipos.STRING:
                temp_string = generador.new_temporal()
                generador.place_operation(temp_string, 'H', '', '') 
                for c in str(self.value):
                    generador.insert_heap('H', ord(c)) 
                    generador.next_heap()
                generador.insert_heap('H', -1)
                generador.next_heap()
                ret = Retorno(temp_string, self.type, True) 
                ret.valor = self.value
                return ret
            
            if self.type == Tipos.CHAR:
                ret = Retorno(ord(self.value), self.type, False)
                ret.valor = self.value
                return ret
            if self.type == Tipos.NOTHING:
                ret = Retorno("nothing", self.type, False)
                ret.valor = "nothing"
                return ret
