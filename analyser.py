from lark import Lark
from lark.visitors import Interpreter
from aux import *

class LPIS2_Interpreter(Interpreter):
    def __init__(self):
        self.regs = Registers()
        self.instrs = {'atrib': 0, 'read': 0, 'write': 0, 'if': 0, 'if_else': 0, 'for': 0, 'while': 0, 'repeat': 0}
        self.ifs = {}
        self.level = 0
        self.output = {}

    def start(self,tree):
        self.visit(tree.children[0])
        self.visit_children(tree.children[2])
        self.output['regs'] = self.regs.to_string()
        self.output['instrs'] = self.instrs
        self.output['ifs'] = self.ifs
        return(self.output)

    def decls(self,tree):
        self.visit_children(tree)

    def decl(self,tree):
        self.visit_children(tree)

    def decl_int(self,tree):
        var = tree.children[1].value
        if len(tree.children) == 3:
            value = self.visit(tree.children[2])
            if not(isinstance(value,int)):
                if '"' in value or value == 'true' or value == 'false':
                    print("Erro: '" + value + "' não é do tipo 'int'")
                else:
                    vrf = value_verifier(value,self.regs)
                    if vrf == "A":
                        print("Erro: Variável '" + value + "' vazia")
                    elif vrf == "B":
                        print("Erro: Variável '" + value + "' inexsitente")
                    elif vrf == "C":
                        vl = value.split('[')[0]
                        print("Erro: '" + vl + "' não possui esse índice")
                    elif vrf == "D":
                        vl = value.split('[')[0]
                        print("Erro: '" + vl + "' não possui essa entrada")
                    elif type_verifier(var,vrf,self.regs) == 0:
                        print("Erro: '" + value + "' não é do tipo 'int'")
                    else:
                        self.regs.int[var] = value
            else:
                self.regs.int[var] = value
        else: 
            value = None
            self.regs.int[var] = value

    def decl_boolean(self,tree):
        var = tree.children[1].value
        if len(tree.children) == 3:
            value = self.visit(tree.children[2])
            if not(value == 'true' or value == 'false'):
                if isinstance(value,int) or '"' in value:
                    print("Erro: '" + str(value) + "' não é do tipo 'boolean'")
                else:
                    vrf = value_verifier(value,self.regs)
                    if vrf == "A":
                        print("Erro: Variável '" + value + "' vazia")
                    elif vrf == "B":
                        print("Erro: Variável '" + value + "' inexsitente")
                    elif vrf == "C":
                        vl = value.split('[')[0]
                        print("Erro: '" + vl + "' não possui esse índice")
                    elif vrf == "D":
                        vl = value.split('[')[0]
                        print("Erro: '" + vl + "' não possui essa entrada")
                    elif type_verifier(var,vrf,self.regs) == 0:
                        print("Erro: '" + value + "' não é do tipo 'boolean'")
                    else:
                        self.regs.boolean[var] = value
            else:
                self.regs.boolean[var] = value
        else: 
            value = None
            self.regs.boolean[var] = value

    def decl_string(self,tree):
        var = tree.children[1].value
        if len(tree.children) == 3:
            value = self.visit(tree.children[2])
            if not('"' in str(value)):
                if isinstance(value,int) or value == 'true' or value == 'false':
                    print("Erro: '" + str(value) + "' não é do tipo 'string'")
                else:
                    vrf = value_verifier(value,self.regs)
                    if vrf == "A":
                        print("Erro: Variável '" + value + "' vazia")
                    elif vrf == "B":
                        print("Erro: Variável '" + value + "' inexsitente")
                    elif vrf == "C":
                        vl = value.split('[')[0]
                        print("Erro: '" + vl + "' não possui esse índice")
                    elif vrf == "D":
                        vl = value.split('[')[0]
                        print("Erro: '" + vl + "' não possui essa entrada")
                    elif type_verifier(var,vrf,self.regs) == 0:
                        print("Erro: '" + value + "' não é do tipo 'string'")
                    else:
                        self.regs.string[var] = value
            else:
                self.regs.string[var] = value
        else: 
            value = None
            self.regs.string[var] = value

    def decl_list(self,tree):
        name = tree.children[1].value
        if len(tree.children) == 3:
            var = self.visit(tree.children[2])
        else: var = []
        self.regs.list[name] = var

    def decl_tuple(self,tree):
        name = tree.children[1].value
        if len(tree.children) == 3:
            var = self.visit(tree.children[2])
        else: var = ()
        self.regs.tuple[name] = var

    def decl_set(self,tree):
        name = tree.children[1].value
        if len(tree.children) == 3:
            var = self.visit(tree.children[2])
        else: var = {}
        self.regs.set[name] = var

    def decl_dict(self,tree):
        name = tree.children[1].value
        if len(tree.children) == 3:
            var = self.visit(tree.children[2])
        else: var = dict()
        self.regs.dict[name] = var

    def decl_atrib(self,tree):
        return self.visit(tree.children[1])

    def decl_atrib_list(self,tree):
        res = []
        i = 2
        while i < len(tree.children):
            res.append(self.visit(tree.children[i]))
            i += 2
        return res

    def decl_atrib_tuple(self,tree):
        aux = []
        i = 2
        while i < len(tree.children):
            aux.append(self.visit(tree.children[i]))
            i += 2
        return tuple(aux)

    def decl_atrib_set(self,tree):
        res = set()
        i = 2
        while i < len(tree.children):
            res.add(self.visit(tree.children[i]))
            i += 2
        return res

    def decl_atrib_dict(self,tree):
        res = dict()
        i = 2
        while i < len(tree.children):
            elem = tree.children[i]
            res[str(self.visit(elem)[0])] = self.visit(elem)[2]
            i += 2
        return res

    def instrs(self,tree):
        self.visit_children(tree)

    def instr(self,tree):
        if self.level > 0: self.inside += 1
        self.visit_children(tree)
    
    def instr_atrib(self,tree):
        flag = 1
        self.instrs['atrib'] += 1
        var = tree.children[0].value
        value = self.visit(tree.children[1])
        if isinstance(value,int) or ('[' not in value and '"' in value) or value == 'true' or value == 'false':
            flag = 0
        
        vrf1 = var_verifier(var,self.regs)
        vrf2 = value_verifier(value,self.regs)

        if vrf1 == 3:
            print("Erro: Variável '" + var + "' inexsitente")
        elif vrf1 == 4:
            print("Erro: Tuplos são imutáveis")
        elif vrf1 == 5:
            v = var.split('[')[0]
            print("Erro: '" + v + "' não possui esse índice")
        elif flag and vrf2 == "A":
            print("Erro: Variável '" + value + "' vazia")
        elif flag and vrf2 == "B":
            print("Erro: Variável '" + value + "' inexsitente")
        elif flag and vrf2 == "C":
            vl = value.split('[')[0]
            print("Erro: '" + vl + "' não possui esse índice")
        elif flag and vrf2 == "D":
            vl = value.split('[')[0]
            print("Erro: '" + vl + "' não possui essa entrada")
        else:
            if type_verifier(var,vrf2,self.regs) == 0:
                print("Erro: '" + var + "' e '" + value + "' são de tipos diferentes")

    def instr_read(self,tree):
        self.instrs['read'] += 1
        var = self.visit(tree.children[2])
        vrf = var_verifier(var,self.regs)
        if vrf == 3:
            print("Erro: Variável '" + var + "' inexsitente")

    def instr_write(self,tree):
        self.instrs['write'] += 1
        var = self.visit(tree.children[2])
        vrf = var_verifier(var,self.regs)
        if vrf == 3:
            print("Erro: Variável '" + var + "' inexsitente")

    def instr_if(self,tree):
        self.instrs['if'] += 1
        if len(tree.children) == 7:
            self.level += 1
            self.visit(tree.children[5])
            self.level -= 1
        else: self.visit(tree.children[4])

    def instr_if_else(self,tree):
        self.instrs['if_else'] += 1
        if len(tree.children) == 5:
            self.level += 1
            self.visit(tree.children[3])
            self.level -= 1
        else: self.visit(tree.children[2])

    def instr_for(self,tree):
        self.instrs['for'] += 1
        if len(tree.children) == 8:
            self.level += 1
            self.visit(tree.children[6])
            self.level -= 1
        else: self.visit(tree.children[4])

    def instr_while(self,tree):
        self.instrs['while'] += 1
        if len(tree.children) == 7:
            self.level += 1
            self.visit(tree.children[5])
            self.level -= 1
        else: self.visit(tree.children[4])

    def instr_repeat(self,tree):
        self.instrs['repeat'] += 1
        self.level += 1
        self.visit(tree.children[2])
        self.level -= 1

    def logic(self,tree):
        return self.visit_children(tree)[0]

    def logic_not(self,tree):
        return self.visit_children(tree)[0]

    def relac(self,tree):
        return self.visit_children(tree)[0]

    def exp(self,tree):
        return self.visit_children(tree)[0]

    def termo(self,tree):
        return self.visit_children(tree)[0]

    def factor(self,tree):
        if len(tree.children) > 1: self.visit_children(tree)
        else:
            var = tree.children[0].value
            if tree.children[0].type == 'INT':
                return int(var)
            else:
                return var
            
        
grammar = open('lpis2.txt').read()
code = open('test_code.txt').read()

p = Lark(grammar)
parse_tree = p.parse(code)
data = LPIS2_Interpreter().visit(parse_tree)

for key in data:
    if key == "regs":
        print(key)
        for t in data[key]:
            print ("\t" + t + ": " + str(data[key][t]))
    else:
        print(key + ": " + str(data[key]))