from lark import Lark
from lark.visitors import Interpreter
import re

class LPIS2_Interpreter(Interpreter): 
    def __init__(self):
        self.current = ""
        self.node = ""
        self.replace = 0
        self.then_else = 0
        self.cfg = ""
        self.sdg = ""
        self.output = {}

    def start(self,tree):
        self.cfg += '''digraph G {
    INICIO -> '''
        self.visit(tree.children[0])
        self.cfg += '''"SEPARADOR"
    "SEPARADOR" -> '''
        self.sdg += 'digraph G {'
        i = 0
        while (i < len(tree.children[2].children)):
            self.sdg += '\n\t"entry main" -> ' 
            self.visit(tree.children[2].children[i])
            i += 1
        self.output['cfg'] = self.cfg
        self.output['sdg'] = self.sdg
        return(self.output)

    def decls(self,tree):
        self.visit_children(tree)
          
    def decl(self,tree):
        self.visit_children(tree)

    def decl_int(self,tree):
        tipo = tree.children[0].value
        var = tree.children[1].value
        if len(tree.children) == 3:
            value = self.visit(tree.children[2])
            node = '"' + tipo + ' ' + var + ' = ' + value + '"'
        else: node = '"' + tipo + ' ' + var + '"'
        self.cfg += node + '\n\t' + node + ' -> '

    def decl_boolean(self,tree):
        tipo = tree.children[0].value
        var = tree.children[1].value
        if len(tree.children) == 3:
            value = self.visit(tree.children[2])
            node = '"' + tipo + ' ' + var + ' = ' + value + '"'
        else: node = '"' + tipo + ' ' + var + '"'
        self.cfg += node + '\n\t' + node + ' -> '

    def decl_string(self,tree):
        tipo = tree.children[0].value
        var = tree.children[1].value
        if len(tree.children) == 3:
            value = self.visit(tree.children[2])
            node = '"' + tipo + ' ' + var + ' = ' + value + '"'
        else: node = '"' + tipo + ' ' + var + '"'
        self.cfg += node + '\n\t' + node + ' -> '

    def decl_list(self,tree):
        tipo = tree.children[0].value
        var = tree.children[1].value
        if len(tree.children) == 3:
            self.node += '"' + tipo + ' ' + var
            self.visit(tree.children[2])
            self.cfg += self.node + '\n\t' + self.node + ' -> '
            self.node = ""
        else: 
            node = '"' + tipo + ' ' + var + '"'
            self.cfg += node + '\n\t' + node + ' -> '

    def decl_tuple(self,tree):
        tipo = tree.children[0].value
        var = tree.children[1].value
        if len(tree.children) == 3:
            self.node += '"' + tipo + ' ' + var
            self.visit(tree.children[2])
            self.cfg += self.node + '\n\t' + self.node + ' -> '
            self.node = ""
        else: 
            node = '"' + tipo + ' ' + var + '"'
            self.cfg += node + '\n\t' + node + ' -> '

    def decl_set(self,tree):
        tipo = tree.children[0].value
        var = tree.children[1].value
        if len(tree.children) == 3:
            self.node += '"' + tipo + ' ' + var
            self.visit(tree.children[2])
            self.cfg += self.node + '\n\t' + self.node + ' -> '
            self.node = ""
        else: 
            node = '"' + tipo + ' ' + var + '"'
            self.cfg += node + '\n\t' + node + ' -> '
        
    def decl_dict(self,tree):
        tipo = tree.children[0].value
        var = tree.children[1].value
        if len(tree.children) == 3:
            self.node += '"' + tipo + ' ' + var
            self.visit(tree.children[2])
            self.cfg += self.node + '\n\t' + self.node + ' -> '
            self.node = ""
        else: 
            node = '"' + tipo + ' ' + var + '"'
            self.cfg += node + '\n\t' + node + ' -> '    

    def decl_atrib(self,tree):
        self.visit(tree.children[1])
        aux = self.current
        self.current = ""
        return aux

    def decl_atrib_list(self,tree):
        i = 2
        j = 3
        self.node += ' ' + tree.children[0] + ' ' + tree.children[1]
        if len(tree.children) > 3:
            while i < len(tree.children):
                self.visit(tree.children[i])
                value = self.current
                self.current = ""
                self.node += str(value)
                self.node += tree.children[j]
                i += 2
                j += 2
        else:
            self.node += tree.children[2]
        self.node += '"'

    def decl_atrib_tuple(self,tree):
        i = 2
        j = 3
        self.node += ' ' + tree.children[0] + ' ' + tree.children[1]
        if len(tree.children) > 3:
            while i < len(tree.children):
                self.visit(tree.children[i])
                value = self.current
                self.current = ""
                self.node += str(value)
                self.node += tree.children[j]
                i += 2
                j += 2
        else:
            self.node += tree.children[2]
        self.node += '"'
    
    def decl_atrib_set(self,tree):
        i = 2
        j = 3
        self.node += ' ' + tree.children[0] + ' ' + tree.children[1]
        if len(tree.children) > 3:
            while i < len(tree.children):
                self.visit(tree.children[i])
                value = self.current
                self.current = ""
                self.node += str(value)
                self.node += tree.children[j]
                i += 2
                j += 2
        else:
            self.node += tree.children[2]
        self.node += '"'

    def decl_atrib_dict(self,tree):
        i = 2
        j = 3
        self.node += ' ' + tree.children[0] + ' ' + tree.children[1]
        if len(tree.children) > 3:
            while i < len(tree.children):
                elem = tree.children[i]
                key = self.visit(elem)[0]
                key = key.replace('"','\\"')
                dp = self.visit(elem)[1]
                self.current = ""
                self.visit(elem.children[2])
                value = self.current
                self.current = ""
                self.node += key + dp + ' ' + str(value)
                self.node += tree.children[j]
                i += 2
                j += 2
    
        else:
            self.node += tree.children[2]
        self.node += '"'

    def instrs(self,tree):
        self.visit_children(tree)

    def instr(self,tree):
        self.visit_children(tree)
    
    def instr_atrib(self,tree):
        var = tree.children[0].value
        var = var.replace('"','\\"')
        value = self.visit(tree.children[1])
        node = '"' + var + ' = ' + value + '"'
        if self.replace:
            self.cfg = self.cfg.replace('-> \n','-> ' + node + '\n')
            self.replace = 0
        self.cfg += node + '\n\t' + node + ' -> '
        self.sdg += node
        if self.then_else == 1:
            self.sdg += ' [ label="then" ];'
            self.then_else = 0
        elif self.then_else == 2:
            self.sdg += ' [ label="else" ];'
            self.then_else = 0

    def instr_read(self,tree):
        var = tree.children[2].value
        var = var.replace('"','\\"')
        node = '"' + tree.children[0] + tree.children[1] + var + tree.children[3] + '"'
        if self.replace:
            self.cfg = self.cfg.replace('-> \n','-> ' + node + '\n')
            self.replace = 0
        self.cfg += node + '\n\t' + node + ' -> '
        self.sdg += node
        if self.then_else == 1:
            self.sdg += ' [ label="then" ];'
            self.then_else = 0
        elif self.then_else == 2:
            self.sdg += ' [ label="else" ];'
            self.then_else = 0
    
    def instr_write(self,tree):
        self.visit(tree.children[2])
        var = self.current
        self.current = ""
        node = '"' + tree.children[0] + tree.children[1] + var + tree.children[3] + '"'
        if self.replace:
            self.cfg = self.cfg.replace('-> \n','-> ' + node + '\n')
            self.repalce = 0
        self.cfg += node + '\n\t' + node + ' -> '
        self.sdg += node
        if self.then_else == 1:
            self.sdg += ' [ label="then" ];'
            self.then_else = 0
        elif self.then_else == 2:
            self.sdg += ' [ label="else" ];'
            self.then_else = 0

    def instr_if(self,tree):
        self.visit(tree.children[2])
        cond = self.current
        self.current = ""
        node = '"' + tree.children[0] + tree.children[1] + str(cond) + tree.children[3] + '"'
        if self.replace:
            self.cfg = self.cfg.replace('-> \n','-> ' + node + '\n')
            self.replace = 0
        self.cfg += node + '\n\t' + node + '[shape=diamond];\n\t' + node + ' -> '
        self.sdg += node
        if self.then_else == 1:
            self.sdg += ' [ label="then" ];'
            self.then_else = 0
        elif self.then_else == 2:
            self.sdg += ' [ label="else" ];'
            self.then_else = 0
        i = 0
        while (i < len(tree.children[5].children)):
            self.sdg += '\n\t' + node + ' -> ' 
            self.visit(tree.children[5].children[i])
            i += 1
        self.cfg += '\n\t' + node + ' -> '
        self.replace = 1

    def instr_if_else(self,tree):
        self.visit(tree.children[2])
        cond = self.current
        self.current = ""
        node = '"' + tree.children[0] + tree.children[1] + str(cond) + tree.children[3] + '"'
        if self.replace:
            self.cfg = self.cfg.replace('-> \n','-> ' + node + '\n')
            self.replace = 0
        self.cfg += node + '\n\t' + node + '[shape=diamond];\n\t' + node + ' -> '
        self.sdg += node
        if self.then_else == 1:
            self.sdg += ' [ label="then" ];'
            self.then_else = 0
        elif self.then_else == 2:
            self.sdg += ' [ label="else" ];'
            self.then_else = 0
        i = 0
        while (i < len(tree.children[5].children)):
            self.sdg += '\n\t' + node + ' -> ' 
            self.then_else = 1
            self.visit(tree.children[5].children[i])
            i += 1
        self.cfg += '\n\t' + node + ' -> '
        i = 0
        while (i < len(tree.children[9].children)):
            self.sdg += '\n\t' + node + ' -> '
            self.then_else = 2
            self.visit(tree.children[9].children[i])
            i += 1
        self.replace = 1
        
    def instr_for(self,tree):
        self.visit(tree.children[5])
        cond = self.current
        cond = cond.replace('"','\\"')
        self.current = ""
        node = '"' + tree.children[0] + tree.children[1] + str(cond) + tree.children[9] + '"'
        decl = '"' + tree.children[2].value + ' = ' + self.visit(tree.children[3]) + '"'
        inc = '"' + tree.children[7].value + ' = ' + self.visit(tree.children[8]) + '"'
        if self.replace:
            self.cfg = self.cfg.replace('-> \n','-> ' + decl + '\n')
            self.replace = 0
        self.cfg += decl + '\n\t' + decl + ' -> '
        self.cfg += node + '\n\t' + node + '[shape=circle];\n\t' + node + ' -> '
        pre = re.search(r'".+" -> $',self.sdg)[0]
        self.sdg += decl
        if self.then_else == 1:
            self.sdg += ' [ label="then" ];'
        elif self.then_else == 2:
            self.sdg += ' [ label="else" ];'
        self.sdg += '\n\t' + pre + node
        if self.then_else == 1:
            self.sdg += ' [ label="then" ];'
            self.then_else = 0
        elif self.then_else == 2:
            self.sdg += ' [ label="else" ];'
            self.then_else = 0
        self.sdg += '\n\t' + node + ' -> ' + node
        i = 0
        while (i < len(tree.children[11].children)):
            self.sdg += '\n\t' + node + ' -> '
            self.visit(tree.children[11].children[i])
            i += 1
        self.sdg += '\n\t' + node + ' -> ' + inc
        self.cfg = self.cfg.replace('-> \n','-> ' + inc + '\n')
        self.cfg += inc + ' -> ' + node + '\n\t' + node + ' -> '

    def instr_while(self,tree):
        self.visit(tree.children[2])
        cond = self.current
        cond = cond.replace('"','\\"')
        self.current = ""
        node = '"' + tree.children[0] + tree.children[1] + str(cond) + tree.children[3] + '"'
        if self.replace:
            self.cfg = self.cfg.replace('-> \n','-> ' + node + '\n')
            self.replace = 0
        self.cfg += node + '\n\t' + node + '[shape=circle];\n\t' + node + ' -> '
        self.sdg += node
        if self.then_else == 1:
            self.sdg += ' [ label="then" ];'
            self.then_else = 0
        elif self.then_else == 2:
            self.sdg += ' [ label="else" ];'
            self.then_else = 0
        self.sdg += '\n\t' + node + ' -> ' + node
        i = 0
        while (i < len(tree.children[5].children)):
            self.sdg += '\n\t' + node + ' -> '
            self.visit(tree.children[5].children[i])
            i += 1
        self.cfg += node + '\n\t' + node + ' -> '

    def instr_repeat(self,tree):
        node = '"' + tree.children[0] + '"'
        if self.replace:
            self.cfg = self.cfg.replace('-> \n','-> ' + node + '\n')
            self.replace = 0
        self.cfg += node + '\n\t' + node + '[shape=circle];\n\t' + node + ' -> '
        self.sdg += node
        if self.then_else == 1:
            self.sdg += ' [ label="then" ];'
            self.then_else = 0
        elif self.then_else == 2:
            self.sdg += ' [ label="else" ];'
            self.then_else = 0
        self.sdg += '\n\t' + node + ' -> ' + node
        i = 0
        while (i < len(tree.children[2].children)):
            self.sdg += '\n\t' + node + ' -> '
            self.visit(tree.children[2].children[i])
            i += 1
        self.sdg += '\n\t' + node + ' -> '
        self.visit(tree.children[3])
        self.cfg += node


    def until(self,tree):
        self.visit(tree.children[2])
        cond = self.current
        cond = cond.replace('"','\\"')
        self.current = ""
        node = '"' + tree.children[0] + tree.children[1] + str(cond) + tree.children[3] + '"'
        self.cfg += node + '\n\t' + node + ' -> \n' + node + ' -> '
        self.sdg += node
        self.replace = 1

    def logic(self,tree):
        if len(tree.children) == 3:
            self.visit_children(tree.children[0])
            self.current += ' ' + tree.children[1] + ' '
            self.visit_children(tree.children[2])
        else: self.visit_children(tree)[0]

    def logic_not(self,tree):
        if len(tree.children) == 2:
            self.current += ' ' + tree.children[0] + ' '
            self.visit_children(tree.children[1])
        else: self.visit_children(tree)[0]

    def relac(self,tree):
        if len(tree.children) == 3:
            self.visit_children(tree.children[0])
            self.current += ' ' + tree.children[1] + ' '
            self.visit_children(tree.children[2])
        else: self.visit_children(tree)[0]

    def exp(self,tree):
        if len(tree.children) == 3:
            self.visit_children(tree.children[0])
            self.current += ' ' + tree.children[1] + ' '
            self.visit_children(tree.children[2])
        else: self.visit_children(tree)[0]

    def termo(self,tree):
        if len(tree.children) == 3:
            self.visit_children(tree.children[0])
            self.current += ' ' + tree.children[1] + ' '
            self.visit_children(tree.children[2])
        else: self.visit_children(tree)[0]

    def factor(self,tree):
        if len(tree.children) > 1:
            self.current += tree.children[0]
            self.visit(tree.children[1])
            self.current += tree.children[2]
        else:
            var = tree.children[0].value
            if tree.children[0].type == "STRING" or tree.children[0].type == "ELEM":
                var = var.replace('"','\\"')
            self.current += var
        
grammar = open('lpis2_graphs.txt').read()
code = open('test_code2.txt').read()

p = Lark(grammar)
parse_tree = p.parse(code)
data = LPIS2_Interpreter().visit(parse_tree)

data['cfg'] = data['cfg'].replace('-> \n','-> "FIM"\n')
data['cfg'] += '"FIM"\n}'
data['sdg'] += '\n}'

with open("cfg.dot",'w') as f:
    f.write(data['cfg'])

with open("sdg.dot",'w') as g:
    g.write(data['sdg'])