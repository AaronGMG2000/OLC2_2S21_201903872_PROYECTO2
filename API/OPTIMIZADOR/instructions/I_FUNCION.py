from ..Abstract.instruccion import Instruccion


class LlamadaFuncion(Instruccion):

    def __init__(self, id, row, column) -> None:
        super().__init__(row, column)
        self.id = id


    def get_code(self):
        return f'{self.id}();'