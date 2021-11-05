
from ..GENERAL.error import Error
from ..GENERAL.table import Tabla
from ..ABSTRACT.NodoAST import NodoAST
import re
import os
class Arbol(object):

    def __init__(self, instructions):
        self.instructions = instructions
        self.global_table = Tabla(None,"GLOBAL")
        self.errors = []
        self.root = NodoAST("INIT")
        self.graph = ""
        self.function = []
        self.c = 0
        
    def ejecutar(self):
        instructions = NodoAST("INSTRUCCIONES")
        for inst in self.getInstrucciones():
            res = inst.Ejecutar(self, self.global_table)
            if isinstance(res, Error):
                self.errors.append(res)
        #     try:
        #         nodoInstruction = NodoAST("INSTRUCCION")
        #         nodoInstruction.agregarHijoNodo(inst.getNodo())
        #         instructions.agregarHijoNodo(nodoInstruction)
        #     except Exception as e:
        #         print(e)
        # self.root.agregarHijoNodo(instructions)
        x = 1
        for er in self.errors:
            er.numero = x
            x+=1
    def getInstrucciones(self):
        return self.instructions

    def getconsole(self):
        return self.console

    def updateconsole(self, update):
        self.console = f"{self.console}{update}"

    
    def graphAST(self):
        return self.getDot(self.root)
        
    def getDot(self, root):
    
        self.graph = ""
        self.graph += "digraph {\n"
        res = r'\"';
        self.graph += "n0[label=\"" +  re.sub(res, '\\\"', root.getValor()) + "\"];\n";
        self.c = 1;
        self.recorrerAST("n0",root);
        self.graph += "}";
        return self.graph;
    
    
    def recorrerAST(self,padre , nPadre):
        for hijo in nPadre.getHijos():
            nombreHijo = "n" + str(self.c);
            res = r'\"'; 
            self.graph += nombreHijo + "[label=\"" + re.sub(res, '\\\"', hijo.getValor())+ "\"];\n";
            self.graph += padre + "->" + nombreHijo + ";\n";
            self.c+=1
            self.recorrerAST(nombreHijo,hijo);
        
    