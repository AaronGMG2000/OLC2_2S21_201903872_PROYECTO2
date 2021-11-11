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
import math
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
                    if self.type != Tipos.STRING:
                        if operation != Aritmeticos.POTENCIA:
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
                                    if not val1.is_temporal:
                                        val1.value = val1.value*1.0
                                    if not val2.is_temporal:
                                        val2.value = val2.value*1.0
                                    generador.place_operation(temp, val1.value,val2.value,'/')
                                else:
                                    if "math" not in generador.imports:
                                        generador.imports.append('math')
                                    generador.inser_code(f'{temp} = math.Mod({val1.value},{val2.value});\n')
                                generador.place_label(exit_flag)
                                if val1.is_temporal:
                                    generador.set_unused_temp(val1.value)
                                if val2.is_temporal:
                                    generador.set_unused_temp(val2.value)
                                ret = Retorno(temp, self.type, True)
                                ret.valor = 0
                                try:
                                    if val2.valor >0:
                                        ret.valor = eval(f'val1.valor {operation.value} val2.valor')
                                except:
                                    ret.valor = 0
                                return ret
                            else:
                                temp = generador.new_temporal()
                                generador.place_operation(temp, val1.value, val2.value, operation.value)
                                if val1.is_temporal:
                                    generador.set_unused_temp(val1.value)
                                if val2.is_temporal:
                                    generador.set_unused_temp(val2.value)
                                ret = Retorno(temp, self.type, True)
                                try:
                                    ret.valor = eval(f'val1.valor {operation.value} val2.valor')
                                except:
                                    ret.valor = 0
                                return ret
                        else:
                            generador.potencia()
                            temp = generador.new_temporal()
                            generador.set_unused_temp(val1.value)
                            generador.set_unused_temp(val2.value)
                            generador.set_unused_temp(temp)
                            generador.temporary_storage(tabla.size)
                            generador.place_operation(temp, 'P',tabla.size,'+')
                            generador.place_operation(temp, temp,1,'+')
                            generador.insert_stack(temp, val1.value)
                            generador.place_operation(temp, temp,1,'+')
                            generador.insert_stack(temp, val2.value)
                            generador.new_env(tabla.size, tabla.previous)
                            generador.call_function("potencia")
                            
                            temp3 = generador.new_temporal()
                            generador.get_stack(temp3, 'P')
                            normal = generador.new_label()
                            generador.place_if(val2.value, 0, '>=',normal)
                            generador.place_operation(temp3, 1, temp3, '/')
                            generador.place_label(normal)
                            generador.return_evn(tabla.size, tabla.previous)
                            generador.take_temporary(tabla.size)
                            ret = Retorno(temp3, self.type, True)
                            try:
                                ret.valor = math.pow(val1.valor, val2.valor)
                            except:
                                ret.valor = 0
                            return ret
                            
                    else:
                        if operation == Aritmeticos.SUMA:
                            generador.concat_string()
                            temp = generador.new_temporal()
                            #liberamos los temporales
                            if val1.is_temporal:
                                generador.set_unused_temp(val1.value)
                            if val2.is_temporal:
                                generador.set_unused_temp(val2.value)
                            generador.set_unused_temp(temp)
                            #teminamos de liberar temporales
                            generador.temporary_storage(tabla.size)
                            generador.place_operation(temp, 'P',tabla.size,'+')
                            generador.place_operation(temp, temp,1,'+')
                            generador.insert_stack(temp, val1.value)
                            generador.place_operation(temp, temp,1,'+')
                            generador.insert_stack(temp, val2.value)
                            generador.new_env(tabla.size, tabla.previous)
                            generador.call_function("concat_string")
                            temp2 = generador.new_temporal()
                            generador.get_stack(temp2, 'P')
                            generador.return_evn(tabla.size, tabla.previous)
                            generador.take_temporary(tabla.size)
                            ret = Retorno(temp2, self.type, True)
                            try:
                                ret.valor = eval(f'val1.valor {operation.value} val2.valor')
                            except:
                                ret.valor = ""
                            return ret
                        
                        
                        if self.Operation == Aritmeticos.POTENCIA:
                            generador.mult_string()
                            temp = generador.new_temporal()
                            #liberamos temporales
                            if val1.is_temporal:
                                generador.set_unused_temp(val1.value)
                            if val2.is_temporal:
                                generador.set_unused_temp(val2.value)
                            generador.set_unused_temp(temp)
                            #terminamos de liberar temporales
                            generador.temporary_storage(tabla.size)
                            generador.place_operation(temp, 'P',tabla.size,'+')
                            generador.place_operation(temp, temp,1,'+')
                            generador.insert_stack(temp, val1.value)
                            generador.place_operation(temp, temp,1,'+')
                            generador.insert_stack(temp, val2.value)
                            generador.new_env(tabla.size, tabla.previous)
                            generador.call_function("mult_string")
                            temp3 = generador.new_temporal()
                            generador.get_stack(temp3, 'P')
                            generador.return_evn(tabla.size, tabla.previous)
                            generador.take_temporary(tabla.size)
                            ret = Retorno(temp3, self.type, True)
                            try:
                                ret.valor = eval(f'val1.valor {operation.value} val2.valor')
                            except:
                                ret.valor = 0
                            return ret
                except:
                    return Error("Sintactico", f'No se pueden operar los tipos {self.val1.type.value} y el tipo {self.val2.type.value} con el operador {self.Operation.value}', self.row, self.column)
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
                    if val1.is_temporal:
                        generador.set_unused_temp(val1.value)
                    ret = Retorno(temp, self.type, True)
                    try:
                        ret.valor = eval(f'{operation.value} val1.valor')
                    except:
                        ret.valor = 0
                    return ret
                except:
                    return Error("Sintactico","No se puede operar el negativo con el tipo "+self.val1.type.value, self.row, self.column)
