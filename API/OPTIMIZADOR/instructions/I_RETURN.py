from ..Abstract.instruccion import Instruccion


class Return(Instruccion):

    def __init__(self, row, column) -> None:
        super().__init__(row, column)


    def get_code(self):
        return 'return;'