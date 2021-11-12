from .literal import Literal
from ..Abstract.instruccion import Instruccion


class Expresion(Instruccion):

    def __init__(self, izq:Literal, der:Literal, op, row, column) -> None:
        super().__init__(row, column)
        self.izq = izq
        self.der = der
        self.op = op
        self.const = izq.const or der.const
        self.delete_neutral = False
        self.force_reduction = False
        self.reduction = ''

    
    def other_operations(self):
        if self.op == '+':
            self.deleted = self.der.get_code() == '0' or self.izq.get_code() == '0'
        elif self.op == '-':
            self.deleted = self.der.get_code() == '0'
        elif self.op == '*':
            self.deleted = self.der.get_code() == '1' or self.izq.get_code() == '1'
        elif self.op == '/':
            self.deleted = self.der.get_code() == '1'
        return self.deleted


    def reduction_force(self):
        fuerza = False
        if self.op == '*':
            if (self.der.get_code() == '0') or (self.izq.get_code() == '0'):
                fuerza = True
                self.reduction = '0'
            elif (self.der.get_code() == '2'):
                fuerza = True
                self.reduction = f'{self.izq.get_code()}+{self.izq.get_code()}'
            elif (self.izq.get_code() == '2'):
                fuerza = True
                self.reduction = f'{self.der.get_code()}+{self.der.get_code()}'
        elif self.op == '/':
            if (self.izq.get_code() == '0') or (self.izq.get_code() == '0.0'):
                fuerza = True
                self.reduction = '0'
        return fuerza


    def contrario(self):
        if self.op == '>':
            self.op = '<='
        elif self.op == '<':
            self.op = '>='
        elif self.op == '>=':
            self.op = '<'
        elif self.op == '<=':
            self.op = '>'
        elif self.op == '==':
            self.op = '!='
        elif self.op == '!=':
            self.op = '=='

    
    def get_code(self):
        if self.delete_neutral:
            if (self.op == '+') or (self.op == '-'):
                if self.der.get_code() == '0':
                    return f'{self.izq.get_code()}'
                return f'{self.der.get_code()}'
            elif (self.op == '*') or (self.op == '/'):
                if self.der.get_code() == '1':
                    return f'{self.izq.get_code()}'
                return f'{self.der.get_code()}'
        if self.force_reduction:
            return self.reduction
        if self.op == '%':
            return f'math.Mod({self.izq.get_code()}, {self.der.get_code()})'
        return f'{self.izq.get_code()}{self.op}{self.der.get_code()}'