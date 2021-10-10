class NodoAST(object):

    def __init__(self, valor):
        self.valor = valor
        self.hijos = []

    def setHijos(self, hijos):
        self.hijos = hijos

    def agregarHijo(self, cadena):
        self.hijos.append(NodoAST(cadena))

    def agregarHijos(self, hijos):
        for m in hijos:
            self.hijos.append(m)

    def agregarHijoNodo(self, hijo):
        self.hijos.append(hijo)

    def getValor(self):
        return self.valor

    def setValor(self, cadena):
        self.valor = cadena

    def getHijos(self):
        return self.hijos
