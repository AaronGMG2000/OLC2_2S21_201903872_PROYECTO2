from ..GENERAL.Simbolo import Simbolo
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.Tipo import CICLICO, Tipos
from ..GENERAL.error import Error
from ..GENERAL.generator import Generador
from ..GENERAL.table import Tabla
from ..ABSTRACT.Retorno import Retorno

class LLAMADA_EXP(Instruccion):

    def __init__(self, id, parametros,row, column):
        super().__init__(Tipos.STRUCT, row, column)
        self.id = id
        self.parametros = parametros
        
    def Ejecutar(self, arbol: Arbol, tabla: Tabla):
        genAux = Generador()
        generador = genAux.get_instance()
        variable = tabla.get_variable(self.id)
        if variable is None:
            return Error("Sintactico","La función o struct indicado no existe", self.row, self.column)
        else:
            if variable.getTipo() == Tipos.STRUCT:
                generador.comment("Iniciando Struct")
                a = 0
                dic = dict(variable.getValor())
                diccionario = variable.getValor()
                t_p = len(self.parametros)
                t_v =len(list(dic.keys()))-2
                if  t_v != t_p:
                    return Error("Sintactico","Class Struct necesita "+str(t_v)+" parametros y esta recibiendo "+str(t_p)+" parametros", self.row, self.column)
                temp = generador.new_temporal()
                temp2 = generador.new_temporal()
                generador.place_operation(temp, 'H', '', '')
                generador.place_operation(temp2, 'H', '', '')
                generador.place_operation('H', 'H', t_v, '+')
                for key in list(dic.keys()):
                    if key == 1 or key == 2:
                        continue
                    valor = self.parametros[a].Ejecutar(arbol, tabla)
                    if isinstance(valor, Error): return valor
                    if self.parametros[a].type == Tipos.NOTHING and dic[key][2] == Tipos.OBJECT:
                        pass
                    elif dic[key][2] == Tipos.OBJECT and self.parametros[a].type == Tipos.OBJECT:
                        if dic[key][1] != self.parametros[a].struct_type:
                            return Error("Sintactico", "El tipo indicado de la variable no coincide", self.row, self.column)
                    elif type(dic[key][2]) == type([]):
                        if dic[key][2] != self.parametros[a].types:
                            return Error("Sintactico", "Error en los tipos de array", self.row, self.column)
                    elif dic[key][2] is not None and dic[key][2]!= self.parametros[a].type:
                        return Error("Sintactico","El parametro '"+key+"' del struct es type "+dic[key][2].value+" y se recibio un type "+self.parametros[a].type.value, self.row, self.column)
                    
                    dic[key] = diccionario[key][:]
                    dic[key][0] = self.parametros[a].type
                    generador.insert_heap(temp2, valor.value)
                    if dic[key][2] == Tipos.OBJECT and self.parametros[a].type == Tipos.OBJECT:
                        if dic[key][1] == self.parametros[a].struct_type:
                            dic[key][4] = valor.valor
                    generador.place_operation(temp2, temp2, '1', '+')
                    a = a+1
                generador.set_unused_temp(temp2)
                self.type = Tipos.OBJECT
                self.struct_type = self.id
                ret = Retorno(temp, Tipos.OBJECT, True)
                ret.auxiliar_type = self.id
                ret.valor = dic
                generador.comment("terminando Struct")
                return ret
            elif variable.getTipo() == Tipos.FUNCTION:
                contenido = variable.getValor()
                x = 0
                if len(self.parametros)!=len(contenido[0]):
                    return Error("Sintactico","La función requiere "+str(len(contenido[0]))+"Parametros y esta recibiendo "+str(len(self.parametros), self.row, self.column) )
                nuevoEntorno = Tabla(tabla, self.id)
                nuevoEntorno.funcion = True
                for par in contenido[0]:
                    
                    variable2 = self.parametros[x].Ejecutar(arbol, tabla)
                    if par[1] != Tipos.NOTHING:
                        if self.parametros[x].type!= par[1]:
                            return Error("Semantico", "Tipo de variable de función invalido", self.row, self.column)
                    newData = Simbolo(variable2, self.parametros[x].type, par[0], self.row, self.column)
                    nuevoEntorno.tabla[par[0]] = newData
                    x+=1
                    
                arbol.PilaFunc.append(self.id)
                for inst in contenido[1]:
                    res = inst.Ejecutar(arbol, nuevoEntorno)
                    if isinstance(res, Error):
                        arbol.errores.append(res)
                        
                arbol.PilaFunc.pop()
                self.type = Tipos.NOTHING
                return "nothing"
            else:
                return Error("Sintactico","la variable indicada no corresponde a un struct o una función", self.row, self.column)

        
    def getNodo(self) -> NodoAST:
        nodo = NodoAST("LLAMADA")
        nodo.agregarHijo(self.id)
        nodo.agregarHijo("(")
        para = None
        anterior = None
        if len(self.parametros):
            for par in self.parametros:
                para = NodoAST("PARAMETROS")
                if anterior is not None:
                    para.agregarHijoNodo(anterior)
                para.agregarHijoNodo(par.getNodo())
                anterior = para
            nodo.agregarHijoNodo(para)
        nodo.agregarHijo(")")
        nodo.agregarHijo(";")
        return nodo
    
    