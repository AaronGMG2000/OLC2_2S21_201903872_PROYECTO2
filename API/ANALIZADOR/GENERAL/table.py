from .Simbolo import Simbolo

class Tabla(object):

    def __init__(self, previous=None, name = "") -> None:
        self.previous = previous
        self.size = 0
        self.name = name
        if (previous != None):
            self.size = self.previous.size

        self.variables = {}
        self.functions = {}
        self.structs = {}


    def set_variable(self, id, type, in_heap) -> bool:
        if id in self.variables.keys():
            return False
        else:
            new_symbol = Simbolo(id, type, self.size, self.previous == None, in_heap)
            self.size += 1
            self.variables[id] = new_symbol
            return True


    def set_function(self, id, func) -> bool:
        if id in self.functions.keys():
            return False
        else:
            self.functions[id] = func
            return True


    def set_struct(self, id, struct) -> bool:
        if id in self.structs.keys():
            return False
        else:
            self.structs[id] = struct
            return True


    def get_variable(self, id):
        tabla = self
        while tabla != None:
            if id in tabla.variables.keys():
                return tabla.variables[id]
            tabla = tabla.previous
        return None


    def get_funcion(self, id):
        tabla = self
        while tabla != None:
            if id in tabla.functions.keys():
                return tabla.functions[id]
            tabla = tabla.previous
        return None


    def get_struct(self, id):
        tabla = self
        while tabla != None:
            if id in tabla.structs.keys():
                return tabla.structs[id]
            tabla = tabla.previous
        return None


    def get_global(self):
        tabla = self
        while tabla.previous != None:
            tabla = tabla.previous
        return tabla


