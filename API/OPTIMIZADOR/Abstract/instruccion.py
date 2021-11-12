from abc import ABC, abstractmethod

class Instruccion(ABC):

    def __init__(self, row, column) -> None:
        self.row = row
        self.column = column
        self.deleted = False
        self.pos = False


    @abstractmethod
    def get_code(self):
        pass