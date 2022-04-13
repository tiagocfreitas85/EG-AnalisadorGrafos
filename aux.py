class Registers():
    def __init__(self):
        self.int = {}
        self.boolean = {}
        self.string = {}
        self.list = {}
        self.tuple = {}
        self.set = {}
        self.dict = {}

    def to_string(self):
        res = {}
        res['int'] = self.int
        res['boolean'] = self.boolean
        res['string'] = self.string
        res['list'] = self.list
        res['tuple'] = self.tuple
        res['set'] = self.set
        res['dict'] = self.dict
        return res

# 1 -> variável declarada mas nao inicializada
# 2 -> variavel declarada e inicializada
# 3 -> variável inexistente
def var_verifier(var,regs):
    for i in regs.int:
        if var == i:
            if regs.int[i] == None:
                return 1
            else : return 2
    for i in regs.boolean:
        if var == i:
            if regs.boolean[i] == None:
                return 1
            else : return 2
    for i in regs.string:
        if var == i:
            if regs.string[i] == None:
                return 1
            else : return 2
    for i in regs.list:
        if var == i:
            if regs.list[i] == None:
                return 1
            else : return 2
    for i in regs.tuple:
        if var == i:
            if regs.tuple[i] == None:
                return 1
            else : return 2
    for i in regs.set:
        if var == i:
            if regs.set[i] == None:
                return 1
            else : return 2
    for i in regs.dict:
        if var == i:
            if regs.dict[i] == None:
                return 1
            else : return 2
    return 3