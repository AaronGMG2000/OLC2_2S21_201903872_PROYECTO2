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
            # nombre = self.id+"("
            # para = False
            # generador.set_anterior()
            # for par in self.parametros:
            #     res = par.Ejecutar(arbol, tabla)
            #     if isinstance(res, Error):
            #         return res
            #     if type(res.type) == type(""):
            #         nombre+=res.type+","
            #     else:
            #         if res.type == Tipos.OBJECT:
            #             nombre+=res.auxiliar_type+","
            #         else:
            #             nombre+=res.type.value+","
            #     para = True
            #     generador.set_unused_temp(res.value)
            #     generador.error_code()
            # if para:
            #     nombre = nombre[0:len(nombre)-1]
            # nombre+=")"
            # variable = tabla.get_variable(nombre)
            # if variable is None:
            generador.error_code()
            return Error("Sintactico","La función o struct indicado no existe", self.row, self.column)
        if variable.getTipo() == Tipos.STRUCT:
            generador.comment("Iniciando Struct")
            a = 0
            dic = dict(variable.getValor())
            diccionario = variable.getValor()
            t_p = len(self.parametros)
            t_v =len(list(dic.keys()))-2
            if  t_v != t_p:
                generador.error_code()
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
                generador.set_unused_temp(valor.value)
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
            self.type = variable.auxiliar_type
            if len(self.parametros)!=len(contenido):
                generador.error_code()
                return Error("Sintactico","La función requiere "+str(len(contenido))+"Parametros y esta recibiendo "+str(len(self.parametros), self.row, self.column) )
            generador.temporary_storage(tabla.size)
            temp = generador.new_temporal()
            generador.place_operation(temp, 'P', tabla.size, '+')
            n = 1
            for par in contenido:
                generador.place_operation(temp, temp, 1, '+')
                if isinstance(self.parametros[x], LLAMADA_EXP):
                    tabla.size+=n
                variable2 = self.parametros[x].Ejecutar(arbol, tabla)
                if isinstance(self.parametros[x], LLAMADA_EXP):
                    tabla.size-=n
                if isinstance(variable2, Error):
                    generador.error_code()
                    return variable2
                if type(contenido[x][1]) != type("") and type(contenido[x][1]) != type([]):
                    if variable2.type != contenido[x][1]:
                        generador.error_code()
                        return Error("Sintactico", "Se esperaba un tipo "+contenido[x][1].value, self.row, self.column)
                else:
                    if variable2.type != contenido[x][1] and variable2.auxiliar_type != contenido[x][1] and self.parametros[x].struct_type != contenido[x][1] and self.parametros[x].types != contenido[x][1]:
                        generador.error_code()
                        print(contenido[x][1])
                        return Error("Sintactico", "Se esperaba un tipo "+str(contenido[x][1]), self.row, self.column)
                x+=1
                n+=1
                generador.insert_stack(temp, variable2.value)
                generador.set_unused_temp(variable2.value)
            generador.set_unused_temp(temp)
            
            generador.new_env(tabla.size, tabla.previous)
            generador.call_function(variable.id.split("(")[0])
            if variable.ret_flag:
                retorno = generador.new_temporal()
                generador.get_stack(retorno, 'P')
                ret:Retorno = Retorno(retorno, variable.auxiliar_type, True)
                ret.valor = 0
            else:
                ret:Retorno = Retorno(-1, Tipos.NOTHING, False)
                ret.valor = -1
            generador.return_evn(tabla.size, tabla.previous)
            generador.take_temporary(tabla.size)
            generador.set_anterior()
            return ret
        else:
            generador.error_code()
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
    
    