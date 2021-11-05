class Retorno(object):
    def __init__(self, value, type, is_temporal, auxiliar_type = None, true_tag = '', false_tag = '') -> None:
        self.value = value
        self.type = type
        self.auxiliar_type = auxiliar_type
        self.is_temporal = is_temporal
        self.true_tag = true_tag
        self.false_tag = false_tag
        self.valor = ""
        self.types = []
        self.valores = []