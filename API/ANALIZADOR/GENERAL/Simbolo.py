from .Tipo import Tipos

class Simbolo(object):
    def __init__(self, id , type: Tipos, position, is_global, in_Heap):
        self.type = type
        self.id = id
        self.value = None
        self.is_global = is_global
        self.position = position
        self.in_Heap = in_Heap
        self.types = []
        self.auxiliar_type = None
        
    def getID(self):
        return self.id

    def getTipo(self):
        return self.type

    def setTipo(self, type: Tipos):
        self.type = type

    def getValor(self):
        return self.value

    def setValor(self, value):
        self.value = value