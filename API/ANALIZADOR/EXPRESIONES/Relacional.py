from ..DICCIONARIO.Diccionario import D_Aritmetica, D_Relacional
from ..ABSTRACT.Retorno import Retorno
from ..GENERAL.generator import Generador
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.table import Tabla
from ..GENERAL.Tipo import Relacionales, Tipos
from ..GENERAL.Tipo import Aritmeticos
from ..GENERAL.error import Error

class Relacional(Instruccion):

    def __init__(self, Operation:Relacionales, row, column, val1:Instruccion, val2:Instruccion):
        super().__init__(Tipos.BOOL, row, column)
        self.val1:Instruccion = val1
        self.val2:Instruccion = val2
        self.Operation:Relacional = Operation

    def getNodo(self) -> NodoAST:
        nodo = NodoAST('PRIMITIVO')
        nodo.agregarHijo(str(self.value))
        return nodo

    def Ejecutar(self, arbol: Arbol, tabla: Tabla):
        genAux = Generador()
        generador = genAux.get_instance()
        if isinstance(generador, Generador):
            val1 = self.val1.Ejecutar(arbol, tabla)
            if isinstance(val1, Error):
                return val1
            try:
                if val1.type!=Tipos.STRING:
                    if self.val1.type==Tipos.BOOL:
                        temporal = generador.new_label()
                        generador.place_label(val1.true_tag)
                        t1 = generador.new_temporal()
                        t2 = generador.new_temporal()
                        generador.place_operation(t1, 1, '','')
                        generador.place_goto(temporal)
                        generador.place_label(val1.false_tag)
                        generador.place_operation(t1, 0, '','')
                        generador.place_label(temporal)
                        val2 = self.val2.Ejecutar(arbol, tabla)
                        if isinstance(val2, Error):
                            return val2
                        operation = D_Relacional[f'{self.val1.type.value}{self.Operation.value}{self.val2.type.value}']
                        temporal2 = generador.new_label()
                        self.true_tag = generador.new_label()
                        self.false_tag = generador.new_label()
                        generador.place_label(val2.true_tag)
                        generador.place_operation(t2, 1, '','')
                        generador.place_goto(temporal2)
                        generador.place_label(val2.false_tag)
                        generador.place_operation(t2, 0, '','')
                        generador.place_label(temporal2)
                        generador.place_if(t1, t2, self.Operation.value, self.true_tag)
                        generador.place_goto(self.false_tag)
                        ret = Retorno(None, Tipos.BOOL, False, None, self.true_tag, self.false_tag)
                        ret.valor = eval(f'val1.valor {self.Operation.value} val2.valor')
                        return 
                    else:
                        val2 = self.val2.Ejecutar(arbol, tabla)
                        if isinstance(val2, Error):
                            return val2
                        operation = D_Relacional[f'{self.val1.type.value}{self.Operation.value}{self.val2.type.value}']
                        self.true_tag = generador.new_label()
                        self.false_tag = generador.new_label()
                        generador.place_if(val1.value, val2.value, self.Operation.value, self.true_tag)
                        generador.place_goto(self.false_tag)
                        ret = Retorno(None, Tipos.BOOL, False, None, self.true_tag, self.false_tag)
                        ret.valor = eval(f'val1.valor {self.Operation.value} val2.valor')
                        return ret
                else:
                    val2 = self.val2.Ejecutar(arbol, tabla)
                    if isinstance(val2, Error):
                        return val2
                    operation = D_Relacional[f'{self.val1.type.value}{self.Operation.value}{self.val2.type.value}']
                    generador.compare_string()
                    temp1 = generador.new_temporal()
                    generador.place_operation(temp1, 'P', tabla.size, '+')
                    generador.place_operation(temp1, temp1, 1, '+')
                    generador.insert_stack(temp1, val1.value)
                    generador.place_operation(temp1, temp1, 1, '+')
                    generador.insert_stack(temp1, val2.value)
                    generador.set_unused_temp(temp1)
                    generador.new_env(tabla.size)
                    generador.call_function("compare_string")
                    ret = generador.new_temporal()
                    generador.get_stack(ret, 'P')
                    self.true_tag = generador.new_label()
                    self.false_tag = generador.new_label()
                    generador.return_evn(tabla.size)
                    generador.place_if(ret, 1, '==', self.true_tag)
                    generador.place_goto(self.false_tag)
                    ret = Retorno(None, Tipos.BOOL, False, None, self.true_tag, self.false_tag)
                    ret.valor = eval(f'val1.valor {self.Operation.value} val2.valor')
                    return ret
            except:
                pass