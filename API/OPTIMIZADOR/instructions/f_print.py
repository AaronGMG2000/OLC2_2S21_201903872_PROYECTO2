from ..Abstract.instruccion import Instruccion


class Imprimir(Instruccion):

    def __init__(self, t, expression:Instruccion, row, column) -> None:
        super().__init__(row, column)
        self.t = t
        self.expression = expression


    def get_code(self):
        if self.t == "%f":
            return f'fmt.Printf("{self.t}", {self.expression.get_code()});'
        else:
            return f'fmt.Printf("{self.t}", int({self.expression.get_code()}));'