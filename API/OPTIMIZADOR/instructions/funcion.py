from ..Abstract.instruccion import Instruccion


class Funcion(Instruccion):

    def __init__(self, instrunctions, id, row, column) -> None:
        super().__init__(row, column)
        self.instrunctions = instrunctions
        self.id = id


    def get_code(self):
        temp = f'func {self.id}(){{\n'
        for ins in self.instrunctions:
            aux_temp = ins.get_code()
            if aux_temp == '': continue
            temp = temp + f'\t{aux_temp}\n'
        temp = temp + '}'
        return temp