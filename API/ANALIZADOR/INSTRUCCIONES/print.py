from typing import List

from ..GENERAL.generator import Generador

from ..ABSTRACT.Retorno import Retorno
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.table import Tabla
from ..GENERAL.Tipo import Tipos
from ..GENERAL.error import Error
from ..GENERAL.Simbolo import Simbolo

class Imprimir(Instruccion):

    def __init__(self, expresion: List, println, fila, columna):
        super().__init__(Tipos.STRING, fila, columna)
        self.expresion = expresion
        self.println = println
        
    def Ejecutar(self, arbol: Arbol, tabla: Tabla):
        for exp in self.expresion:
            genAux = Generador()
            generador = genAux.get_instance()
            if isinstance(generador, Generador):
                if isinstance(exp, Instruccion):
                    retorno = exp.Ejecutar(arbol, tabla)
                    if isinstance (retorno, Error):
                        return retorno
                    if retorno.type == Tipos.ENTERO:
                        generador.place_print('d', retorno.value)
                        continue
                    if retorno.type == Tipos.FLOAT:
                        generador.place_print('f', retorno.value)
                        continue
                    if retorno.type == Tipos.CHAR:
                        generador.place_print('c', retorno.value)
                        continue
                    if retorno.type == Tipos.NOTHING:
                        generador.nothing()
                        continue  
                    if retorno.type == Tipos.BOOL:
                        etiqueta_temporal = generador.new_label()
                        if retorno.value:
                            generador.place_goto(retorno.true_tag)
                            generador.place_goto(retorno.false_tag)
                        else:
                            generador.place_goto(retorno.false_tag)
                            generador.place_goto(retorno.true_tag)
                        generador.place_label(retorno.true_tag)
                        generador.print_true()
                        generador.place_goto(etiqueta_temporal)

                        generador.place_label(retorno.false_tag)
                        generador.print_false()

                        generador.place_label(etiqueta_temporal)
                        continue
                    if retorno.type == Tipos.STRING:
                        generador.F_print()
                        temp = generador.new_temporal()
                        temp2 = generador.new_temporal()
                        generador.place_operation(temp, "P","0","+")
                        generador.place_operation(temp2, temp,"1","+")
                        generador.insert_stack(temp2, retorno.value)
                        generador.new_env(0)
                        generador.call_function("F_print")
                        temp3 = generador.new_temporal()
                        generador.get_stack(temp3, temp)
                        generador.return_evn(0)
                        continue
        if self.println:
            genAux = Generador()
            generador = genAux.get_instance()
            if isinstance(generador, Generador):
                generador.place_print('c',ord('\n'))            
    def getStruct(self, val, struct):
        val += struct[1] + "("
        lista = list(struct.keys())
        for key in lista:
            if key == 1 or key == 2:
                continue
            if key != lista[2]:
                val +=","
            valor = struct[key]
            if valor[1] == Tipos.OBJECT:
                val = self.getStruct(val, valor[0])
            elif valor[1] == Tipos.ARRAY:
                val = str(self.getArrayValue(valor[0], val))
            elif valor[1] == Tipos.STRING:
                val +='"'+valor[0]+'"'
            elif valor[1] == Tipos.CHAR:
                val +='"'+valor[0]+'"'
            elif valor[1] == Tipos.BOOL:
                val += str(valor[0]).lower()
            elif valor[1].tipo == Tipos.FUNCTION:
                val = valor[2]
            else:
                val += str(valor[0])
        val += ")"
        return val
    
    def getArrayValue(self, simb, val):
        val += '['
        for sim in simb:
            if sim != simb[0]:
                val+=","
            if not isinstance(sim, Simbolo):
                val = self.getArrayValue(sim, val)
            else:
                valor = sim.getValor()
                if sim.getTipo() == Tipos.OBJECT:
                    val = self.getStruct(val, valor)
                else:
                    if sim.getTipo() == Tipos.STRING:
                        val +='"'+valor+'"'
                    elif sim.getTipo() == Tipos.CHAR:
                        val +="'"+valor+"'"
                    elif sim.getTipo() == Tipos.FUNCTION:
                        val = valor[2]
                    elif sim.getTipo() == Tipos.BOOL:
                        val = str(valor).lower()
                    else:
                        val+=str(valor)
        val += ']'
        return val
        
    def getNodo(self) -> NodoAST:
        nodo = NodoAST('PRINT')
        nodo.agregarHijo('PRINT')
        nodo.agregarHijo('(')
        anterior = None
        nodoParametro = None
        for ex in self.expresion:
            nodoParametro = NodoAST("PARAMETROS")
            if anterior is not None:
                nodoParametro.agregarHijoNodo(anterior)
                nodoParametro.agregarHijo(',')
            nodoParametro.agregarHijoNodo(ex.getNodo())
            anterior = nodoParametro
        if nodoParametro is not None:
            nodo.agregarHijoNodo(nodoParametro)
        nodo.agregarHijo(')')
        return nodo