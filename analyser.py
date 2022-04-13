from lark import Lark
from lark.visitors import Interpreter
from aux import *

class LPIS2_Interpreter(Interpreter):
    def __init__(self):
        self.regs = Registers()
        self.instrs = {}
        self.ifs = {}
        self.level = 0
        self.output = {}

    def start(self,tree):
        self.visit(tree)
        self.output['regs'] = self.regs.to_string()
        self.output['instrs'] = self.instrs
        self.output['ifs'] = self.ifs
        return(self.output)

    def decls(self,tree):
        self.visit_children(tree)

    def decl(self,tree):
        self.visit_children(tree)

    def decl_int(self,tree):
        name = tree.children[1].value
        if len(tree.children) == 3:
            var = self.visit(tree.children[2])
        else: var = None
        print(var_verifier(var,self.regs))
        self.regs.int[name] = var

    def decl_boolean(self,tree):
        name = tree.children[1].value
        if len(tree.children) == 3:
            var = self.visit(tree.children[2])
        else: var = None
        self.regs.boolean[name] = var

    def decl_string(self,tree):
        name = tree.children[1].value
        if len(tree.children) == 3:
            var = self.visit(tree.children[2])
        else: var = None
        self.regs.string[name] = var

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
            if tree.children[0].type == 'BOOLEAN':
                if var == "true": return True
                else: return False
            if tree.children[0].type == 'STRING':
                return str(var)
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