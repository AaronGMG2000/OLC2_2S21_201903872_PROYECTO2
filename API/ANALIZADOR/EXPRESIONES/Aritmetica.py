from ..DICCIONARIO.Diccionario import D_Aritmetica
from ..ABSTRACT.Retorno import Retorno
from ..GENERAL.generator import Generador
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.table import Tabla
from ..GENERAL.Tipo import Tipos
from ..GENERAL.Tipo import Aritmeticos
from ..GENERAL.error import Error

class Aritmetica(Instruccion):

    def __init__(self, Operation:Aritmeticos, row, column, val1:Instruccion, val2:Instruccion=None):
        super().__init__(Tipos.ENTERO, row, column)
        self.val1:Instruccion = val1
        self.val2:Instruccion = val2
        self.Operation:Aritmeticos = Operation

    def getNodo(self) -> NodoAST:
        nodo = NodoAST('PRIMITIVO')
        nodo.agregarHijo(str(self.value))
        return nodo

    def Ejecutar(self, arbol: Arbol, tabla: Tabla):
        genAux = Generador()
        generador = genAux.get_instance()
        if isinstance(generador, Generador):
            if self.val2!=None:
                val1 = self.val1.Ejecutar(arbol, tabla)
                if isinstance(val1, Error):
                    return val1
                val2 = self.val2.Ejecutar(arbol, tabla)
                if isinstance(val2, Error):
                    return val2
                try:
                    dic = D_Aritmetica[f'{self.val1.type.value}{self.Operation.value}{self.val2.type.value}']
                    operation = dic[1]
                    self.type = dic[0]
                    if operation != Aritmeticos.POTENCIA:
                        if self.type != Tipos.STRING:
                            if operation == Aritmeticos.DIVISION or operation == Aritmeticos.MODULO:
                                true_flag = generador.new_label()
                                exit_flag = generador.new_label()
                                temp = generador.new_temporal()
                                generador.place_if(val2.value, 0, '!=', true_flag)
                                generador.print_mathError()
                                generador.call_function('math_error')
                                generador.place_operation(temp, 0,'','')
                                generador.place_goto(exit_flag)
                                generador.place_label(true_flag)
                                if operation == Aritmeticos.DIVISION:
                                    generador.place_operation(temp, val1.value,val2.value,'/')
                                else:
                                    t1 = val1.value
                                    t2 = val2.value
                                    if val1.is_temporal:
                                        t1 = f'int({val1.value})'
                                    if val2.is_temporal:
                                        t2 = f'int({val2.value})'
                                    if val1.is_temporal or val2.is_temporal:
                                        generador.inser_code(f'{temp} = float64({t1} % {t2});\n')
                                    else:
                                        generador.inser_code(f'{temp} = {t1} % {t2};\n')
                                generador.place_label(exit_flag)
                                return Retorno(temp, self.type, True)
                            else:
                                temp = generador.new_temporal()
                                generador.place_operation(temp, val1.value, val2.value, operation.value)
                                return Retorno(temp, self.type, True)
                except:
                    pass
            else:
                val1 = self.val1.Ejecutar(arbol, tabla)
                if isinstance(val1, Error):
                    return val1
                try:
                    dic = D_Aritmetica[f'{self.Operation.value}{self.val1.type.value}']
                    operation = dic[1]
                    self.type = dic[0]
                    temp = generador.new_temporal()
                    generador.place_operation(temp, 0, val1.value, operation.value)
                    return Retorno(temp, self.type, True)
                except:
                    pass
