import re

from ..ABSTRACT.Retorno import Retorno
from ..GENERAL.Simbolo import Simbolo
from ..EXPRESIONES.variable import Variable
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.table import Tabla
from ..GENERAL.Tipo import CICLICO, Tipos
from ..GENERAL.error import Error
from ..GENERAL.generator import Generador
class FUNCION(Instruccion):

    def __init__(self, id, instruciones,fila, columna, parametros=[], aux_type=Tipos.NOTHING):
        super().__init__(Tipos.FUNCTION, fila, columna)
        self.id = id
        self.parametros = parametros
        self.instruciones = instruciones
        self.auxiliar_type = aux_type

    def Ejecutar(self, arbol: Arbol, tabla: Tabla):
        variable = tabla.get_variable(self.id)
        genAux = Generador()
        generador = genAux.get_instance()
        generador.in_function = True
        ret_flag = False
        if variable == None:
            exit = generador.new_label()
            # nombre = self.id+"("
            # para = False
            # for par in self.parametros:
            #     if type(par[1]) == type(""):
            #         nombre+=par[1]+","
            #     else:
            #         nombre+=par[1].value+","
            #     para = True
            # if para:
            #     nombre = nombre[0:len(nombre)-1]
            # nombre+=")"
            tabla.set_variable(arbol, self.row, self.column, self.id, Tipos.FUNCTION, False)
            vari = tabla.get_variable(self.id)
            vari.value = self.parametros
            vari.auxiliar_type = self.auxiliar_type
            generador.new_function(self.id)
            generador.set_anterior()
            tabla.size-=1
            newTable = Tabla(tabla, self.id)
            newTable.size=1
            arbol.PilaFunc.append([False, -1, exit])
            for par in self.parametros:
                if type(par[1]) != type("") and type(par[1])!=type([]):
                    newTable.set_variable(arbol, self.row, self.column, par[0], par[1], False)
                elif type(par[1])==type([]):
                    newTable.set_variable(arbol, self.row, self.column, par[0], Tipos.ARRAY, False)
                    var = newTable.get_variable(par[0])
                    var.types = par[1]
                else:
                    newTable.set_variable(arbol, self.row, self.column, par[0], Tipos.OBJECT, False)
                    var = newTable.get_variable(par[0])
                    var.struct_type = par[1]
            
            for ins in self.instruciones:
                res = ins.Ejecutar(arbol, newTable)
                if isinstance(res, Error):
                    arbol.errors.append(res)
                if isinstance(res, Retorno):
                    generador.set_unused_temp(res.value)
                    
            if arbol.PilaFunc[-1][0] is True:
                vari.ret_flag = True
                generador.place_label(exit)
            generador.end_function()
            generador.set_anterior()
            generador.in_function = False
            arbol.PilaFunc.pop()
        else:
            generador.error_code()
            return Error("Sintactico","La función indicada ya existe", self.fila, self.columna)
        
    def getNodo(self) -> NodoAST:
        nodo = NodoAST('FUNCTION')
        nodo.agregarHijo(self.id)
        nodo.agregarHijo("(")
        if len(self.parametros):
            para = None
            anterio = None
            for par in self.parametros:
                para = NodoAST("PARAMETROS")
                if anterio is not None:
                    para.agregarHijoNodo(anterio)
                    para.agregarHijo(",")
                    
                para.agregarHijo(par[0])
                if par[1] != Tipos.NOTHING:
                    para.agregarHijo("::")
                    para.agregarHijo(par[1].value)
                anterio = para
            nodo.agregarHijoNodo(para)
        nodo.agregarHijo(")")
        inst = NodoAST("INSTRUCCIONES")
        for ins in self.instruciones:
            insts = NodoAST("INSTRUCCION")
            insts.agregarHijoNodo(ins.getNodo())
            inst.agregarHijoNodo(insts)
        nodo.agregarHijoNodo(inst)
        nodo.agregarHijo("end")
        nodo.agregarHijo(";")
        return nodo