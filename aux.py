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
# 4 -> tuplos são imutáveis
# 5 -> estrutura não possui esse índice
# 6 -> entrada inexistente

def var_verifier(var,regs):
    flag = 0
    
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
    
    if '[' in var:
        v = var.split('[')[0]
        index = var.split('[')[1].split(']')[0]
        flag = 1
    
    for i in regs.list:
        if not(flag):
            if var == i:
                if regs.list[i] == None or regs.list[i] == []:
                    return 1
                else : return 2
        else:
            if v == i:
                if len(regs.list[i]) > int(index): return 2
                else: return 5
               
    for i in regs.tuple:
        if not(flag):
            if var == i:
                if regs.tuple[i] == None or regs.tuple == ():
                    return 1
                else : return 2
        else: 
            if v == i: return 4

    for i in regs.set:
        if not(flag):
            if var == i:
                if regs.set[i] == None or regs.set[i] == set():
                    return 1
                else : return 2
        else:
            if v == i:
                if len(regs.set[i]) > int(index): return 2
                else: return 5

    for i in regs.dict:
        if not(flag):
            if var == i:
                if regs.dict[i] == None or regs.dict[i] == {}:
                    return 1
                else : return 2
        else:
            if v == i: return 2
    return 3

# A -> variável declarada mas nao inicializada
# B -> variável inexistente
# C -> estrutura não possui esse índice
# D -> entrada inexistente
def value_verifier(value,regs):
    flag = 0
    
    for i in regs.int:
        if value == i:
            if regs.int[i] == None:
                return "A"
            else:
                value = regs.int[i] 
                return value
    
    for i in regs.boolean:
        if value == i:
            if regs.boolean[i] == None:
                return "A"
            else:
                value = regs.boolean[i] 
                return value
    
    for i in regs.string:
        if value == i:
            if regs.string[i] == None:
                return "A"
            else:
                value = regs.string[i] 
                return value
    
    if not(value.isdigit()) and '[' in value:
        v = value.split('[')[0]
        index = value.split('[')[1].split(']')[0]
        flag = 1
    
    for i in regs.list:
        if not(flag):
            if value == i:
                if regs.list[i] == None or regs.list[i] == []:
                    return "A"
                else:
                    value = regs.list[i]
                    return value
        else:
            if v == i:
                if len(regs.list[i]) > int(index): 
                    value = regs.list[i][int(index)]
                    return value
                else: return "C"
               
    for i in regs.tuple:
        if not(flag):
            if value == i:
                if regs.tuple[i] == None or regs.tuple == ():
                    return "A"
                else:
                    value = regs.tuple[i] 
                    return value
        else: 
            if v == i:
                if len(regs.list[i]) > int(index):
                    value = regs.tuple[i][int(index)] 
                    return value
                else: return "C"

    for i in regs.set:
        if not(flag):
            if value == i:
                if regs.set[i] == None or regs.set[i] == set():
                    return "A"
                else : 
                    value = regs.set[i]
                    return value
        else:
            if v == i:
                if len(regs.set[i]) > int(index): 
                    value = regs.set[i][int(index)]
                    return value
                else: return "C"

    for i in regs.dict:
        if not(flag):
            if value == i:
                if regs.dict[i] == None or regs.dict[i] == {}:
                    return "A"
                else: 
                    value = regs.dict[i]
                    return value
        else:
            if v == i:
                if index in regs.dict[i]: 
                    value = regs.dict[i][index]
                    return value
                else: return "D"
    return "B"

           
# 0 -> valor com diferente tipo da variável
def type_verifier(var,value,regs):
    for i in regs.int:
        if var == i:
            if value.isdigit(): return 1
            else: return 0
    for i in regs.boolean:
        if var == i:
            if value == 'true' or value == 'false': return 1
            else: return 0
    for i in regs.string:
        if var == i:
            if ('"' in value): return 1
            else: return 0

def error_html(error,value):
    return '<div class="error">' + value + '<span class="errortext">' + error + '</span></div>'