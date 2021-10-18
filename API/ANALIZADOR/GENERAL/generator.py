from .table import Tabla

class Generador(object):
    generador = None
    def __init__(self) -> None:
        self.temp_counter = 0
        self.label_counter = 0
        self.code = ''
        self.functions = ''
        self.natives = ''
        self.previous_code = ''
        self.previous_functions = ''
        self.previous_natives = ''
        self.in_function = False
        self.in_native = False
        self.temps = []
        self.native_true = []
        self.imports = []
        self.use_temps = {}
        self.unused_temps = {}

    def limpiar(self):
        self.temp_counter = 0
        self.label_counter = 0
        self.code = ''
        self.functions = ''
        self.natives = ''
        self.in_function = False
        self.in_native = False
        self.temps = []
        self.native_true = []
        self.imports = []
        Generador.generador = Generador()

    
    '''
    CODIGO
    '''
    def generate_header(self) -> str:
        if len(self.imports) == 0:
            c = 'package main;\n\nimport (\n\t"fmt"\n)\n\n'
        else:
            c = 'package main;\n\nimport (\n\t"fmt"\n'
            for im in self.imports:
                c+=f'\t"{im}"\n'
            c += ')\n\n'
        if len(self.temps) > 0:
            c += 'var '
            for temp in range(len(self.temps)):
                c += self.temps[temp]
                if temp != (len(self.temps) - 1):
                    c += ", "
            c += " float64;\n"
        c += "var P, H float64;\nvar stack [30101999]float64;\nvar heap [30101999]float64;\n\n"
        return c

    def error_code(self):
        self.code = self.previous_code
        self.functions = self.previous_functions
        self.natives = self.previous_natives
    
    def set_anterior(self):
        self.previous_code = self.code
        self.previous_functions = self.functions
        self.previous_natives = self.natives
    
    def get_code(self):
        return f'{self.generate_header()}{self.natives}\n{self.functions}\nfunc main(){{\n\tP = 0;\n\tH = 0;\n{self.code}\n}}'


    def inser_code(self, codigo, tab='\t'):
        if self.in_native:
            if self.natives == '':
                self.natives += '/*----native functions----*/\n'
            self.natives = self.natives + tab + codigo
        elif self.functions:
            if self.functions == '':
                self.functions += '/*----functions----*/\n'
            self.functions += tab + codigo 
        else:
            self.code += '\t' + codigo


    def comment(self, comment):
        self.inser_code(f'/* {comment} */\n')


    def get_instance(self):
        if Generador.generador == None:
            Generador.generador = Generador()
        return Generador.generador


    def jump(self):
        self.inser_code('\n')


    '''
    TEMPORALES
    '''
    def new_temporal(self) -> str:
        if len(self.unused_temps.keys()) >0:
            temp = self.unused_temps.pop(list(self.unused_temps.keys())[0], None)
            self.use_temps[temp] = temp
            return temp
        else:
            temporal = f't{self.temp_counter}'
            self.use_temps[temporal] = temporal
            self.temp_counter += 1
            self.temps.append(temporal)
            return temporal

    def set_unused_temp(self, T):
        if len(self.use_temps.keys())>0:
            temp = self.use_temps.get(T)
            if temp is not None:
                unused = self.use_temps.pop(temp, None)
                self.unused_temps[unused] = unused
    '''
    ETIQUETAS
    '''
    def new_label(self) -> str:
        etiqueta = f'L{self.label_counter}'
        self.label_counter += 1
        return etiqueta


    def place_label(self, etiqueta):
        self.inser_code(f'{etiqueta}:\n')



    def place_goto(self, etiqueta):
        self.inser_code(f'goto {etiqueta};\n')



    def place_if(self, izq, der, operador, etiqueta):
        self.inser_code(f'if {izq}{operador}{der} {{goto {etiqueta};}}\n')


    '''
    OPERACION BINARIA
    '''
    def place_operation(self, resultado, izq, der, operador):
        self.inser_code(f'{resultado}={izq}{operador}{der}; \n')


    '''
    functions
    '''
    def new_function(self, id):
        if not self.in_native:
            self.in_function = True
        self.inser_code(f'func {id}(){{\n', '')


    def end_function(self):
        self.inser_code('return;\n}\n\n')
        if not self.in_native:
            self.in_function = False


    '''
    STACK
    '''
    def insert_stack(self, posicion, valor):
        self.inser_code(f'stack[int({posicion})]={valor};\n')


    def get_stack(self, variable, posicion):
        self.inser_code(f'{variable}=stack[int({posicion})];\n')


    '''
    HEAP
    '''
    def insert_heap(self, posicion, valor):
        self.inser_code(f'heap[int({posicion})]={valor};\n')


    def get_heap(self, variable, posicion):
        self.inser_code(f'{variable}=heap[int({posicion})];\n')


    def next_heap(self):
        self.inser_code('H = H + 1;\n')

    
    '''
    ENTORNO
    '''
    def new_env(self, tamano):
        self.inser_code(f'P=P+{tamano};\n')

    
    def call_function(self, id):
        self.inser_code(f'{id}();\n')


    def return_evn(self, tamano):
        self.inser_code(f'P=P-{tamano};\n')

    # Añadir print de go 
    def place_print(self, tipo, valor):
        if tipo != 'f':
            self.inser_code(f'fmt.Printf("%{tipo}", int({valor}));\n')
        else:
            self.inser_code(f'fmt.Printf("%{tipo}", {valor});\n')

    '''
        prints
    '''
    def print_true(self):
        self.place_print('c', 116)#t
        self.place_print('c', 114)#r
        self.place_print('c', 117)#u
        self.place_print('c', 101)#e

    def print_false(self):
        self.place_print('c', 102)#f
        self.place_print('c', 97) #a
        self.place_print('c', 108)#l
        self.place_print('c', 115)#s
        self.place_print('c', 101)#e

    def nothing(self):
        self.place_print('c', 110) #n
        self.place_print('c', 111) #o
        self.place_print('c', 116) #t
        self.place_print('c', 104) #h
        self.place_print('c', 105) #i
        self.place_print('c', 110) #n
        self.place_print('c', 103) #g


    '''
    natives
    '''

    def print_mathError(self):
        if "math_error" in self.native_true:
            return
        self.native_true.append("math_error")
        self.in_native = True

        self.new_function('math_error')
        self.place_print('c', 77)   #M
        self.place_print('c', 97)   #a
        self.place_print('c', 116)  #t
        self.place_print('c', 104)  #h
        self.place_print('c', 69)   #E
        self.place_print('c', 114)  #r
        self.place_print('c', 114)  #r
        self.place_print('c', 111)  #o
        self.place_print('c', 114)  #r
        self.place_print('c', 10)   #Salto de linea
        self.end_function()
        self.in_native = False

    def print_BoundsError(self):
        if "BoundsError" in self.native_true:
            return
        self.native_true.append("BoundsError")
        self.in_native = True

        self.new_function('BoundsError')
        self.place_print('c', 66)   #B
        self.place_print('c', 111)  #O
        self.place_print('c', 117)  #U
        self.place_print('c', 110)  #N
        self.place_print('c', 100)  #D 
        self.place_print('c', 115)  #S
        self.place_print('c', 69)   #E
        self.place_print('c', 114)  #R
        self.place_print('c', 114)  #R
        self.place_print('c', 111)  #O
        self.place_print('c', 114)  #R
        self.place_print('c', 10)   #Salto de linea
        self.end_function()
        self.in_native = False

    
    def F_print(self):
        if "F_print" in self.native_true:
            return
        self.native_true.append("F_print")
        self.in_native = True
        self.new_function('F_print')
        salir = self.new_label()
        loop = self.new_label()
        stack = self.new_temporal()
        heap = self.new_temporal()
        self.place_operation(stack,'P','1','+')
        self.get_stack(heap, stack)
        self.set_unused_temp(stack)
        comparar = self.new_temporal()
        self.place_label(loop)
        self.get_heap(comparar, heap)
        self.place_if(comparar, -1, '==', salir)
        self.place_print('c', comparar)
        self.place_operation(heap, heap, "1", "+")
        self.place_goto(loop)
        self.place_label(salir)
        self.end_function()
        self.set_unused_temp(heap)
        self.set_unused_temp(comparar)
        
        self.in_native = False
        
    def potencia(self):
        if "potencia" in self.native_true:
            return
        self.native_true.append("potencia")
        self.in_native = True
        self.new_function('potencia')
        pos_value = self.new_temporal()
        pos_pot = self.new_temporal()
        self.place_operation(pos_value, 'P', 1, '+')
        self.place_operation(pos_pot, 'P', 2, '+')
        exit = self.new_label()
        w1 = self.new_label()
        value = self.new_temporal()
        self.get_stack(value, pos_value)
        pot = self.new_temporal()
        self.get_stack(pot, pos_pot)
        normal = self.new_label()
        self.place_if(pot, 0, '>=', normal)
        self.place_operation(pot, pot, -1, '*')
        self.place_label(normal)
        comp = self.new_temporal()
        self.place_operation(comp, 1, '','')
        self.place_label(w1)
        mult = self.new_temporal()
        self.place_operation(mult, 1, '','')
        self.place_if(comp, pot, '>=', exit)
        self.get_stack(mult, pos_value)
        self.place_operation(value, mult, value, '*')
        self.place_operation(comp, comp, 1, '+')
        self.place_goto(w1)
        self.place_label(exit)
        self.insert_stack('P', value)
        self.end_function()
        self.set_unused_temp(pos_value)
        self.set_unused_temp(pos_pot)
        self.set_unused_temp(value)
        self.set_unused_temp(pot)
        self.set_unused_temp(comp)
        self.set_unused_temp(mult)
        
        self.in_native = False    

    def mult_string(self):
        if "mult_string" in self.native_true:
            return
        self.native_true.append("mult_string")
        self.in_native = True
        self.new_function('mult_string')
        ret = self.new_temporal()
        self.place_operation(ret, 'H','','')
        pos_str = self.new_temporal()
        pos_value = self.new_temporal()
        self.place_operation(pos_str, 'P', 1, '+')
        self.place_operation(pos_value, 'P', 2, '+')
        exit = self.new_label()
        w1 = self.new_label()
        w2 = self.new_label()
        resta = self.new_label()
        #obtenemos el valor
        value = self.new_temporal()
        self.get_stack(value, pos_value)
        #primer while
        self.place_label(w1)
        str = self.new_temporal()
        self.get_stack(str, pos_str)
        self.place_if(value, 0, '==', exit)
        self.place_label(w2)
        #vamos colocando el nuevo string
        comp = self.new_temporal()
        self.get_heap(comp, str)
        self.place_if(comp, -1, '==', resta)
        self.insert_heap('H', comp)
        self.next_heap()
        self.place_operation(str, str, 1, '+')
        self.place_goto(w2)
        self.place_label(resta)
        self.place_operation(value, value, 1, '-')
        self.place_goto(w1)
        self.place_label(exit)
        self.insert_heap('H',-1)
        self.next_heap()
        self.insert_stack('P', ret)
        self.end_function()
        self.set_unused_temp(ret)
        self.set_unused_temp(pos_str)
        self.set_unused_temp(pos_value)
        self.set_unused_temp(value)
        self.set_unused_temp(str)
        self.set_unused_temp(comp)
        self.in_native = False

    def concat_string(self):
        if "concat_string" in self.native_true:
            return
        self.native_true.append("concat_string")
        self.in_native = True
        self.new_function('concat_string')
        temp = self.new_temporal()
        self.place_operation(temp, 'H','','')
        temp2 = self.new_temporal()
        temp4 = self.new_temporal()
        self.place_operation(temp2, 'P', 1, '+')
        self.place_operation(temp4, 'P', 2, '+')
        temp3 = self.new_temporal()
        self.get_stack(temp3, temp2)
        self.set_unused_temp(temp2)
        exit = self.new_label()
        label = self.new_label()
        self.place_label(label)
        temp5 = self.new_temporal()
        self.get_heap(temp5, temp3)
        label2 = self.new_label()
        self.place_if(temp5, -1, '==', label2)
        self.insert_heap('H', temp5)
        self.next_heap()
        self.place_operation(temp3, temp3, 1, '+')
        self.place_goto(label)
        self.place_label(label2)
        temp6 = self.new_temporal()
        self.get_stack(temp6, temp4)
        self.set_unused_temp(temp4)
        label3 = self.new_label()
        self.place_label(label3)
        #-------#
        comp = self.new_temporal()
        self.get_heap(comp, temp6)
        self.place_if(comp, -1, '==', exit)
        self.insert_heap('H', comp)
        self.next_heap()
        self.place_operation(temp6, temp6, 1, '+')
        self.place_goto(label3)
        self.place_label(exit)
        self.insert_heap('H',-1)
        self.next_heap()
        self.insert_stack('P', temp)
        self.end_function()
        self.set_unused_temp(temp)
        self.set_unused_temp(temp3)
        self.set_unused_temp(temp5)
        self.set_unused_temp(temp6)
        self.set_unused_temp(comp)
        self.in_native = False

    def compare_string(self):
        if "compare_string" in self.native_true:
            return
        self.native_true.append("compare_string")
        self.in_native = True
        self.new_function('compare_string')
        temp = self.new_temporal()
        temp2 = self.new_temporal()
        self.place_operation(temp, 'P', 1, '+')
        self.get_stack(temp2, temp)
        self.place_operation(temp, temp, 1, '+')
        temp3 = self.new_temporal()
        self.get_stack(temp3, temp)
        self.set_unused_temp(temp)
        exit = self.new_label()
        w = self.new_label()
        self.place_label(w)
        temp4 = self.new_temporal()
        temp5 = self.new_temporal()
        self.get_heap(temp4, temp2)
        self.get_heap(temp5, temp3)
        l_true = self.new_label()
        l_false = self.new_label()
        self.place_if(temp4, temp5, '!=', l_false)
        self.place_if(temp4, -1, '==', l_true)
        self.place_operation(temp2, temp2, 1, '+')
        self.place_operation(temp3, temp3, 1, '+')
        self.place_goto(w)
        self.place_label(l_true)
        self.insert_stack('P', 1)
        self.place_goto(exit)
        self.place_label(l_false)
        self.insert_stack('P', 0)
        self.place_label(exit)        
        self.end_function()
        self.set_unused_temp(temp2)
        self.set_unused_temp(temp3)
        self.set_unused_temp(temp4)
        self.set_unused_temp(temp5)
        self.in_native = False
