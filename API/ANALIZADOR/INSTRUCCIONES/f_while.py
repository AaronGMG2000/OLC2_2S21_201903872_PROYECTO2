# from ..INSTRUCCIONES.BREAK import BREAK
# from ..INSTRUCCIONES.CONTINUE import CONTINUE
# from ..INSTRUCCIONES.RETURN import RETURN
from ..GENERAL.Simbolo import Simbolo
from ..ABSTRACT.instruccion import Instruccion
from ..ABSTRACT.NodoAST import NodoAST
from ..GENERAL.Arbol import Arbol
from ..GENERAL.table import Tabla
from ..GENERAL.Tipo import CICLICO, Tipos
from ..GENERAL.error import Error
from ..GENERAL.generator import Generador
from ..ABSTRACT.Retorno import Retorno

class WHILE(Instruccion):

    def __init__(self, expresion, instruciones,fila, columna):
        super().__init__(Tipos.NOTHING, fila, columna)
        self.expresion = expresion
        self.instruciones = instruciones

    def Ejecutar(self, arbol: Arbol, tabla: Tabla):
        genAux = Generador()
        generador = genAux.get_instance()
        w = generador.new_label()
        
        generador.place_label(w)
        condicion = self.expresion.Ejecutar(arbol, tabla)
        
        if isinstance(condicion, Error):
            generador.error_code() 
            return condicion
        if condicion.type == Tipos.BOOL:
            true_tag = condicion.true_tag
            false_tag = condicion.false_tag
        else:
            generador.error_code()
            return Error("Sintactico", "Se esperaba un valor booleano en la expresion del while", self.fila, self.columna)
        if self.expresion.type == Tipos.BOOL:
            generador.place_label(true_tag)
            evaluado = True
            nuevo_entorno = Tabla(tabla, "WHILE")
            for inst in self.instruciones:
                res = inst.Ejecutar(arbol, nuevo_entorno)
                if isinstance(res, Error) and evaluado:
                    arbol.errors.append(res)
            evaluado = False
            generador.place_goto(w)
            generador.place_label(false_tag)
            generador.set_anterior()
        else:
            return Error("Sintactico", "Se esperaba un valor booleano en la expresion del while", self.fila, self.columna)
                    
        
    def getNodo(self) -> NodoAST:
        nodo = NodoAST('WHILE')
        nodo.agregarHijoNodo(self.expresion.getNodo())
        inst = NodoAST('INSTRUCCIONES')
        for ins in self.instruciones:
            instr = NodoAST("INSTRUCCION")
            instr.agregarHijoNodo(ins.getNodo())
            inst.agregarHijoNodo(instr)
        nodo.agregarHijoNodo(inst)
        return nodo