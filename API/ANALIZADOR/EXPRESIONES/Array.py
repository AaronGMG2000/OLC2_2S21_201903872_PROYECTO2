import types
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.table import Tabla
from ..GENERAL.Simbolo import Simbolo
from ..GENERAL.Tipo import Tipos
from ..GENERAL.error import Error
from ..GENERAL.generator import Generador
from ..ABSTRACT.Retorno import Retorno

class ARRAY(Instruccion):

    def __init__(self, expresion, fila, columna):
        super().__init__(Tipos.ARRAY, fila, columna)
        self.expresion = expresion
        self.types = []

    def Ejecutar(self, arbol: Arbol, tabla: Tabla):
        genAux = Generador()
        generador = genAux.get_instance()
        valor = []
        temp = generador.new_temporal()
        generador.place_operation(temp, 'H','','')
        temp2 = generador.new_temporal()
        generador.place_operation(temp2, temp, 1, '+')
        generador.insert_heap('H', len(self.expresion))
        generador.place_operation('H','H',len(self.expresion)+1,'+')
        generador.inser_code('\n')
        t_type = None
        aux_type = None
        valores = []
        for exp in self.expresion:
            res = exp.Ejecutar(arbol, tabla)
            if isinstance(res, Error): 
                return res
            if t_type == None:
                t_type = exp.type
                if t_type == Tipos.OBJECT:
                    t_type = exp.struct_type
                aux_type = res.auxiliar_type
                if aux_type is not None:
                    if t_type == Tipos.RANGE:
                        self.types.append(aux_type)
                    else:
                        self.types.append(exp.types)
                else:
                    self.types.append(t_type)
            valores.append(res.valor)
            if exp.type == Tipos.OBJECT and exp.struct_type == t_type:
                pass
            elif exp.type != t_type or aux_type != res.auxiliar_type:
                return Error("Sintactico","Los arrays solo pueden contener un tipo", self.row, self.column)
            if exp.type != Tipos.BOOL:
                generador.insert_heap(temp2, res.value)
            else:
                aux = generador.new_label()
                generador.place_label(res.true_tag)
                generador.insert_heap(temp2, 1)
                generador.place_goto(aux)
                generador.place_label(res.false_tag)
                generador.insert_heap(temp2, 0)
                generador.place_label(aux)
            generador.place_operation(temp2, temp2, 1, '+')
            generador.set_unused_temp(res.value)
        generador.set_unused_temp(temp2)
        self.type = Tipos.ARRAY
        ret = Retorno(temp, Tipos.ARRAY, True, t_type)
        ret.types = self.types
        ret.valor = valores
        ret.valores = valores
        return ret
    
    
    def getNodo(self) -> NodoAST:
        nodo = NodoAST('ARRAY')
        lista = None
        anterior = None
        nodo.agregarHijo("[")
        for exp in self.expresion:
            lista = NodoAST('LISTA_ARRAY')
            if anterior is not None:
                lista.agregarHijoNodo(anterior)
                lista.agregarHijo(",")
            lista.agregarHijoNodo(exp.getNodo())
            anterior = lista
        nodo.agregarHijoNodo(lista)
        nodo.agregarHijo("]")
        return nodo