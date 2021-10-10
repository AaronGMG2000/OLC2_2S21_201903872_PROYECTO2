from datetime import datetime
class Error(object):

    def __init__(self,tipo, descripcion, fila, columna):
        self.tipo = tipo
        self.descripcion = descripcion
        self.fila = fila
        self.columna = columna
        now = datetime.now()
        format = now.strftime('%d/%m/%Y %H:%M:%S')
        self.fecha = format
        self.numero = 0
        
    def toString(self):
        return self.tipo + " - " + self.descripcion + " [" + self.fila + ", " + self.columna + "]\n"
