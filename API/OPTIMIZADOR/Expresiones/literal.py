from ..Abstract.instruccion import Instruccion


class Literal(Instruccion):


    def __init__(self, value, row, column, const = False) -> None:
        super().__init__(row, column)
        self.value = value
        self.const = const


    def get_code(self):
        return str(self.value)