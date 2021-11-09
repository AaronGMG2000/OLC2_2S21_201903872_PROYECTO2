from ..DICCIONARIO.Diccionario import D_LOGICA
from ..ABSTRACT.Retorno import Retorno
from ..GENERAL.generator import Generador
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.table import Tabla
from ..GENERAL.Tipo import Logicas, Tipos
from ..GENERAL.Tipo import Aritmeticos
from ..GENERAL.error import Error

class Logico(Instruccion):

    def __init__(self, Operation:Logicas, row, column, val1:Instruccion, val2:Instruccion=None):
        super().__init__(Tipos.ENTERO, row, column)
        self.val1:Instruccion = val1
        self.val2:Instruccion = val2
        self.Operation:Logicas = Operation

    def getNodo(self) -> NodoAST:
        nodo = NodoAST('PRIMITIVO')
        nodo.agregarHijo(str(self.value))
        return nodo

    def Ejecutar(self, arbol: Arbol, tabla: Tabla):
        genAux = Generador()
        generador = genAux.get_instance()
        if isinstance(generador, Generador):
            resutl = False
            if self.true_tag == '':
                self.true_tag = generador.new_label()
            if self.false_tag == '':
                self.false_tag = generador.new_label()
                
            if self.Operation == Logicas.OR:
                self.val1.true_tag = self.val2.true_tag = self.true_tag
                aux = self.val1.false_tag = generador.new_label()
                self.val2.false_tag=self.false_tag
                op = "or"
                
            elif self.Operation == Logicas.NOT:
                self.val1.false_tag = self.true_tag
                self.val1.true_tag = self.false_tag
                val1 = self.val1.Ejecutar(arbol, tabla)
                if self.val1.type != Tipos.BOOL:
                    return Error("Sintactico", "negación unicamente valida con valores booleanos",self.row, self.column)
                self.type = Tipos.BOOL
                op = "not"
                try:
                    resutl = eval(f'{op} val1.valor')
                except:
                    resutl = True
                val1.valor = resutl
                return val1
            elif self.Operation == Logicas.AND:
                aux = self.val1.true_tag = generador.new_label()
                self.val2.true_tag = self.true_tag
                self.val1.false_tag = self.val2.false_tag = self.false_tag
                op = "and"
                
            val1 = self.val1.Ejecutar(arbol, tabla)
            if self.val1.type != Tipos.BOOL:
                return Error("Sintactico", "negación unicamente valida con valores booleanos",self.row, self.column)
            generador.place_label(aux)
            val2 = self.val2.Ejecutar(arbol, tabla)
            if self.val2.type != Tipos.BOOL:
                return Error("Sintactico", "negación unicamente valida con valores booleanos",self.row, self.column)
            self.type = Tipos.BOOL
            ret = Retorno(None, Tipos.BOOL,False, None, self.true_tag, self.false_tag)
            try:
                ret.valor = eval(f'val1.valor {op} val2.valor')
            except:
                ret.valor = True
            if val1.is_temporal:
                generador.set_unused_temp(val1.value)
            if val2.is_temporal:
                generador.set_unused_temp(val2.value)
            return ret
            
