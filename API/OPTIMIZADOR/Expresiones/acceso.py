from ..Abstract.instruccion import Instruccion


class Acceso(Instruccion):

    def __init__(self, StackHeap, position:Instruccion, row, column) -> None:
        super().__init__(row, column)
        self.StackHeap = StackHeap
        self.position = position


    def get_code(self):
        return f'{self.StackHeap}[int({self.position.get_code()})]'
