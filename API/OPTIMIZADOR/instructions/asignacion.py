from ..Expresiones.acceso import Acceso
from ..Abstract.instruccion import Instruccion
from ..Expresiones.literal import Literal
from ..Expresiones.expresion import Expresion

class Asignacion(Instruccion):

    def __init__(self, pos:Instruccion, expression:Expresion, row, column) -> None:
        super().__init__(row, column)
        self.pos = pos
        self.expression = expression


    def own_allocation(self):
        if isinstance(self.expression, Literal):
            temp = self.pos.get_code() == self.expression.get_code()
        elif isinstance(self.expression, Acceso):
            return False
        else:
            temp = self.pos.get_code() == self.expression.izq.get_code() or self.pos.get_code() == self.expression.der.get_code()
        return temp

    
    def get_code(self):
        if self.deleted:
            return ''
        return f'{self.pos.get_code()} = {self.expression.get_code()};'