from ..GENERAL.reglas import Rule as Rules
from ..instructions.asignacion import Asignacion
from ..instructions.etiqueta import Etiqueta
from ..instructions.goto import Goto
from ..instructions.I_IF import If
from ..Expresiones.acceso import Acceso
from ..Expresiones.literal import Literal
# from .blocks import Blocks


class Optimizador:

    def __init__(self, package, temps, code) -> None:
        self.package = package
        self.temps = temps
        self.code = code 
        self.rules = []
        self.del_labels = []
        self.use_labels = []
    
    def get_code(self):
        if len(self.package)==1:
            retorno = f'package main;\n\nimport (\n\t"{self.package[0]}"\n);\n'
        else:
            retorno = f'package main;\n\nimport (\n\t"{self.package[0]}";\n\t"{self.package[1]}";\n);\n'
        for temp in self.temps:
            retorno = retorno + f'var {temp}\n'
        retorno = retorno + '\n'
        
        for func in self.code:
            retorno = retorno + func.get_code() + '\n\n'
        return retorno

    def Mirilla(self):
        for func in self.code:
            size = 20
            if len(func.instrunctions) < 20:
                size = len(func.instrunctions)
            for i in range(10):
                opt = False
                n = 0
                while (size +  n) <= len(func.instrunctions):
                    opt = opt or self.Rule1(func.instrunctions[0 + n: size + n])
                    opt = opt or self.Rule2(func.instrunctions[0 + n: size + n])
                    opt = opt or self.Rule3(func.instrunctions[0 + n: size + n])
                    opt = opt or self.Rule4(func.instrunctions[0 + n: size + n])
                    opt = opt or self.Rule5(func.instrunctions[0 + n: size + n])
                    opt = opt or self.Rule6(func.instrunctions[0 + n: size + n])
                    opt = opt or self.Rule7(func.instrunctions[0 + n: size + n])
                    opt = opt or self.Rule8(func.instrunctions[0 + n: size + n])
                    n = n + 1
                if not opt:
                    size = size + 20
                
    # def Mirilla(self):
    #     for func in self.code:
    #         size = 20
    #         if len(func.instrunctions) < 20:
    #             size = len(func.instrunctions)
    #         while size <= len(func.instrunctions):
    #             opt = False
    #             for i in range(10):
    #                 n = 0
    #                 while (size +  n) <= len(func.instrunctions):
    #                     opt = opt or self.Rule1(func.instrunctions[0 + n: size + n])
    #                     opt = opt or self.Rule2(func.instrunctions[0 + n: size + n])
    #                     opt = opt or self.Rule3(func.instrunctions[0 + n: size + n])
    #                     opt = opt or self.Rule4(func.instrunctions[0 + n: size + n])
    #                     opt = opt or self.Rule5(func.instrunctions[0 + n: size + n])
    #                     opt = opt or self.Rule6(func.instrunctions[0 + n: size + n])
    #                     opt = opt or self.Rule7(func.instrunctions[0 + n: size + n])
    #                     opt = opt or self.Rule8(func.instrunctions[0 + n: size + n])
    #                     n = n + 1
    #             if not opt:
    #                 size = size + 20

    ########################
    ##########RuleS########
    ########################
    
    def Rule1(self, instrunctions):
        retorno = False
        receive = value = None
        for i in range(len(instrunctions)):
            current = instrunctions[i]
            if isinstance(current, Asignacion) and not current.deleted:
                if isinstance(current.pos, Literal) and isinstance(current.expression, Literal):
                    if receive is None:
                        receive = current.pos.get_code()
                        value = current.expression.get_code()
                        Rule = Rules(len(self.rules)+1, 'Mirilla', 'Regla 1', f'{current.get_code()}', current.row, current.column)
                        Rule.opt =  f'{current.get_code()}'
                    else: # Si no es none significa que se verifica si se puede optimizar
                        if (current.expression.get_code() == receive) and (current.pos.get_code() == value):
                            Rule.opt += f'\n {current.get_code()}'
                            current.deleted = retorno = True
                            self.rules.append(Rule)
                        elif (current.expression.get_code() == receive) and (current.pos.get_code() != value):
                            receive = value = None
                elif (current.pos.get_code() == receive) and (current.expression.get_code() != value):
                    receive = value = None
                elif isinstance(current.pos, Literal) and isinstance(current.expression, Acceso) and receive == " -":
                    if receive is None:
                        receive = current.pos.get_code()
                        value = current.expression.get_code()
                        Rule = Rules(len(self.rules)+1, 'Mirilla', 'Regla 1', f'{current.get_code()}', current.row, current.column)
                        Rule.opt =  f'{current.get_code()}'
                    else: # Si no es none significa que se verifica si se puede optimizar
                        if (current.expression.get_code() == receive) and (current.pos.get_code() == value):
                            Rule.opt += f'\n {current.get_code()}'
                            current.deleted = retorno = True
                            self.rules.append(Rule)
                        elif (current.expression.get_code() == receive) and (current.pos.get_code() != value):
                            receive = value = None
                elif isinstance(current.pos, Acceso) and isinstance(current.expression, Literal) and receive == " -":
                    if receive is None:
                        receive = current.pos.get_code()
                        value = current.expression.get_code()
                        Rule = Rules(len(self.rules)+1, 'Mirilla', 'Regla 1', f'{current.get_code()}', current.row, current.column)
                        Rule.opt =  f'{current.get_code()}'
                    else: # Si no es none significa que se verifica si se puede optimizar
                        if (current.expression.get_code() == receive) and (current.pos.get_code() == value):
                            Rule.opt += f'\n {current.get_code()}'
                            current.deleted = retorno = True
                            self.rules.append(Rule)
                        elif (current.expression.get_code() == receive) and (current.pos.get_code() != value):
                            receive = value = None
                
            elif isinstance(current, Etiqueta) and not current.deleted:
                receive = value = None
        return retorno


    def Rule2(self, instrunctions):
        retorno = delete = False
        optimized = 0
        for i in range(len(instrunctions)):
            try:
                current = instrunctions[i]
            except:
                continue
            if isinstance(current, Etiqueta) and (not current.deleted) and (len(self.del_labels)>0):
                if current.id in self.del_labels:
                    current.deleted = True
                    self.del_labels.remove(current.id)
            if delete:
                if isinstance(current, Etiqueta) and (not current.deleted):
                    delete = False
                    if optimized > 0:
                        self.rules.append(Rule)
                        optimized = 0
                elif isinstance(current, Goto) and (not current.deleted):
                    Rule.original += f'\n {current.get_code()}'
                    current.deleted = retorno = True
                    if not current.etiqueta in self.use_labels:
                        self.del_labels.append(current.etiqueta)
                    optimized += 1
                elif not current.deleted: 
                    Rule.original += f'\n {current.get_code()}'
                    current.deleted = retorno = True
                    optimized += 1
            if isinstance(current, Goto) and (not current.deleted) and (not delete):
                delete = True
                self.use_labels.append(current.etiqueta)
                Rule = Rules(len(self.rules)+1, 'Mirilla', 'Regla 2', f'{current.get_code()}', current.row, current.column)
                Rule.opt =  f'{current.get_code()}'
        return retorno


    def Rule3(self, instrunctions):
        retorno = False
        del_labels = []
        for i in range(len(instrunctions)):
            try:
                current = instrunctions[i]
            except:
                continue
            if isinstance(current, Etiqueta) and (not current.deleted) and (len(del_labels)>0):
                if current.id in del_labels:
                    current.deleted = True
                    del_labels.remove(current.id)
            if isinstance(current, If) and not current.deleted:
                try:
                    next_instruction = instrunctions[i+1]
                except:
                    continue
                if isinstance(next_instruction, Goto) and not next_instruction.deleted:
                    try:
                        Rule = Rules(len(self.rules)+1, 'Mirilla', 'Regla 3', f'{current.get_code()} \n {next_instruction.get_code()} \n {instrunctions[i+2].get_code()}',
                                     current.row, current.column)
                    except:
                        continue
                    current.condition.contrario()
                    del_labels.append(current.etiqueta)
                    current.etiqueta = next_instruction.etiqueta
                    next_instruction.deleted = retorno = True
                    Rule.opt = current.get_code()
                    self.rules.append(Rule)
        return retorno


    def Rule4(self, instrunctions):
        retorno = False
        tag_optimize = None
        opt_ins = None
        for i in range(len(instrunctions)):
            current = instrunctions[i]
            if isinstance(current, Goto) and (not current.deleted) and (tag_optimize is None):
                tag_optimize = current.etiqueta
                opt_ins = current
            elif isinstance(current, Etiqueta) and (not tag_optimize is None) and (not current.deleted):
                if current.id == tag_optimize:
                    try:
                        if isinstance(instrunctions[i+1], Goto) and (not instrunctions[i+1].deleted):
                            Rule = Rules(len(self.rules)+1, 'Mirilla', 'Regla 4', f'{opt_ins.get_code()} \n <instrunctions> \n {current.get_code()} \n {instrunctions[i+1].get_code()}',
                                         current.row, current.column)
                            Rule.opt = f'{opt_ins.get_code()} \n <instrunctions>'
                            opt_ins.etiqueta = instrunctions[i+1].etiqueta
                            current.deleted = instrunctions[i+1].deleted = retorno  = True
                            self.rules.append(Rule)
                    finally:
                        tag_optimize = opt_ins = None
                        continue
        return retorno


    def Rule5(self, instrunctions):
        retorno = False
        tag_optimize = None
        opt_ins = None
        for i in range(len(instrunctions)):
            current = instrunctions[i]
            if isinstance(current, If) and (not current.deleted) and (tag_optimize is None):
                tag_optimize = current.etiqueta
                opt_ins = current
            elif isinstance(current, Etiqueta) and (not tag_optimize is None) and (not current.deleted):
                if current.id == tag_optimize:
                    try:
                        if isinstance(instrunctions[i+1], Goto) and (not instrunctions[i+1].deleted):
                            Rule = Rules(len(self.rules)+1, 'Mirilla', 'Regla 5', f'{opt_ins.get_code()} \n <instrunctions> \n {current.get_code()} \n {instrunctions[i+1].get_code()}',
                                         current.row, current.column)
                            Rule.opt = f'{opt_ins.get_code()} \n <instrunctions>'
                            opt_ins.etiqueta = instrunctions[i+1].etiqueta
                            current.deleted = instrunctions[i+1].deleted = retorno = True
                            self.rules.append(Rule)
                    finally:
                        tag_optimize = opt_ins = None
                        continue
        return retorno


    def Rule6(self, instrunctions):
        retorno = False
        for i in range(len(instrunctions)):
            try:
                current = instrunctions[i]
            except:
                continue
            if isinstance(current, Asignacion) and not current.deleted:
                if current.own_allocation():
                    bandera = current.expression.other_operations()
                    if bandera:
                        # Se optimizara
                        Rule = Rules(len(self.rules)+1, 'Mirilla', 'Regla 6', f'{current.get_code()}',
                                         current.row, current.column)
                        current.deleted = retorno = True
                        self.rules.append(Rule)
        return retorno

    
    def Rule7(self, instrunctions):
        retorno = False
        for i in range(len(instrunctions)):
            current = instrunctions[i]
            if isinstance(current, Asignacion) and not current.deleted:
                if (not current.own_allocation()) and (not isinstance(current.expression, Acceso)) and (not isinstance(current.expression, Literal)):
                    if current.expression.delete_neutral:
                        continue
                    bandera = current.expression.other_operations()
                    if bandera:
                        Rule = Rules(len(self.rules)+1, 'Mirilla', 'Regla 7', f'{current.get_code()}',
                                         current.row, current.column)
                        Rule.opt = current.get_code()
                        current.expression.delete_neutral = retorno = True
                        self.rules.append(Rule)
        return retorno


    def Rule8(self, instrunctions):
        retorno = False
        for i in range(len(instrunctions)):
            current = instrunctions[i]
            if isinstance(current, Asignacion) and not current.deleted:
                if (not current.own_allocation()) and (not isinstance(current.expression, Acceso)) and (not isinstance(current.expression, Literal)):
                    if current.expression.force_reduction:
                        continue
                    bandera = current.expression.reduction_force()
                    if bandera:
                        Rule = Rules(len(self.rules)+1, 'Mirilla', 'Regla 8', f'{current.get_code()}',
                                         current.row, current.column)
                        Rule.opt = current.get_code()
                        current.expression.force_reduction = retorno = True
                        self.rules.append(Rule)
        return retorno
                
    ########################
    #########BLOQUES########
    ########################
    # def Bloques(self):
    #     self.blocks = []
    #     self.GenerarBloques()

    # def GenerarBloques(self):
    #     self.GenerarLideres()
    #     self.CrearBloques()
    #     self.ConnectBloques()
    #     print('Prueba')

    # def GenerarLideres(self):
    #     for func in self.code:
    #         func.instr[0].isLeader = True
    #         flag = False
    #         for instr in func.instr:
    #             if flag:
    #                 instr.isLeader = True
    #                 flag = False
    #             if type(instr) is Goto or type(instr) is If:
    #                 flag = True

    # def CrearBloques(self):
    #     for func in self.code:
    #         blocks = []
    #         block = None
    #         for instr in func.instr:
    #             if instr.isLeader:
    #                 if block != None:
    #                     blocks.append(block)
    #                 block = Blocks(instr)
    #             block.code.append(instr)
    #         blocks.append(block)
    #         self.blocks.append(blocks)

    # def ConnectBloques(self):
        for func in self.blocks:
            prevBlock = None
            for block in func:
                if prevBlock == None:
                    prevBlock = block
                    continue
                prevBlock.nexts.append(block)
                prevBlock = block
            
            for block in func:
                lastIns = block.code[len(block.code) - 1]
                if type(lastIns) is Goto or type(lastIns) is If:
                    label = lastIns.label
                    for check in func:
                        if type(check.first) is Etiqueta and check.first.id == label:
                            block.nexts.append(check)
                            break