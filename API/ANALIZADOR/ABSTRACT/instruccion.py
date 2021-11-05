from ..GENERAL.Tipo import Tipos
from ..GENERAL.table import Tabla
from ..GENERAL.Arbol import Arbol
from .NodoAST import NodoAST
from abc import ABC, abstractmethod


class Instruccion(ABC):

    def __init__(self, type, row, column):
        self.type = type
        self.row = row
        self.column = column
        self.false_tag = ""
        self.true_tag = ""
        self.types = []
        self.struct_type = ""
        super().__init__()

    @abstractmethod
    def Ejecutar(self, arbol: Arbol, tabla: Tabla):
        pass

    @abstractmethod
    def getNodo(self) -> NodoAST:
        pass
