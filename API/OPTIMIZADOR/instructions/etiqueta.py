from ..Abstract.instruccion import Instruccion


class Etiqueta(Instruccion):

    def __init__(self, id, row, column) -> None:
        super().__init__(row, column)
        self.id = id

    
    def get_code(self):
        if self.deleted:
            return ''
        return f'{self.id}:'