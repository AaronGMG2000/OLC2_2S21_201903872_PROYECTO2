from ..Abstract.instruccion import Instruccion


class If(Instruccion):

    def __init__(self, condition: Instruccion, etiqueta, row, column) -> None:
        super().__init__(row, column)
        self.etiqueta = etiqueta
        self.condition = condition

    
    def get_code(self):
        return f'if ({self.condition.get_code()}) {{ goto {self.etiqueta}; }}'