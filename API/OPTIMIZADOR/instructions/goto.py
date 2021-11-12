from ..Abstract.instruccion import Instruccion


class Goto(Instruccion):

    def __init__(self, etiqueta, row, column) -> None:
        super().__init__(row, column)
        self.etiqueta = etiqueta

    
    def get_code(self):
        if self.deleted:
            return ''
        return f'goto {self.etiqueta};'