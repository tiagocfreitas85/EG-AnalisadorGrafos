from lark import Lark
from lark.visitors import Interpreter
import re
import pydot

class LPIS2_Interpreter(Interpreter): 
    def __init__(self):
        self.current = ""
        self.instrs = {'atrib': [], 'read': [], 'write': [], 'if': [], 'if_else': [], 'for': [], 'while': [], 'repeat': []}
        self.node = ""
        self.replace = 0
        self.true = 0
        self.then_else = 0
        self.node_counter = 0
        self.edge_counter = 0
        self.cfg = ""
        self.sdg = ""
        self.output = {}

    def start(self,tree):
        self.node_counter += 1
        self.cfg += '''digraph G {
    INICIO -> '''
        self.sdg += 'digraph G {'
        i = 0
        while (i < len(tree.children[0].children)):
            if i % 2 == 0:
                self.sdg += '\n\t"entry main" -> '
                self.edge_counter += 1
                self.visit(tree.children[0].children[i])
            i += 1
        self.node_counter += 1
        self.cfg += '''"SEPARADOR"
    "SEPARADOR" -> '''
        self.edge_counter += 1
        i = 0
        while (i < len(tree.children[2].children)):
            self.sdg += '\n\t"entry main" -> '
            self.visit(tree.children[2].children[i])
            i += 1
        
        self.output['node_counter'] = self.node_counter
        self.output['edge_counter'] = self.edge_counter
        self.output['cfg'] = self.cfg
        self.output['sdg'] = self.sdg
        return(self.output)

    def decls(self,tree):
        self.visit_children(tree)
          
    def decl(self,tree):
        self.visit_children(tree)

    def decl_int(self,tree):
        self.node_counter += 1
        tipo = tree.children[0].value
        var = tree.children[1].value
        if len(tree.children) == 3:
            value = self.visit(tree.children[2])
            node = '"' + tipo + ' ' + var + ' = ' + value + '"'
        else: node = '"' + tipo + ' ' + var + '"'
        self.cfg += node + '\n\t' + node + ' -> '
        self.sdg += node

    def decl_boolean(self,tree):
        self.node_counter += 1
        tipo = tree.children[0].value
        var = tree.children[1].value
        if len(tree.children) == 3:
            value = self.visit(tree.children[2])
            node = '"' + tipo + ' ' + var + ' = ' + value + '"'
        else: node = '"' + tipo + ' ' + var + '"'
        self.cfg += node + '\n\t' + node + ' -> '
        self.sdg += node

    def decl_string(self,tree):
        self.node_counter += 1
        tipo = tree.children[0].value
        var = tree.children[1].value
        if len(tree.children) == 3:
            value = self.visit(tree.children[2])
            node = '"' + tipo + ' ' + var + ' = ' + value + '"'
        else: node = '"' + tipo + ' ' + var + '"'
        self.cfg += node + '\n\t' + node + ' -> '
        self.sdg += node

    def decl_list(self,tree):
        self.node_counter += 1
        tipo = tree.children[0].value
        var = tree.children[1].value
        if len(tree.children) == 3:
            self.node += '"' + tipo + ' ' + var
            self.visit(tree.children[2])
            self.cfg += self.node + '\n\t' + self.node + ' -> '
            self.sdg += self.node
            self.node = ""
        else: 
            node = '"' + tipo + ' ' + var + '"'
            self.cfg += node + '\n\t' + node + ' -> '
            self.sdg += node

    def decl_tuple(self,tree):
        self.node_counter += 1
        tipo = tree.children[0].value
        var = tree.children[1].value
        if len(tree.children) == 3:
            self.node += '"' + tipo + ' ' + var
            self.visit(tree.children[2])
            self.cfg += self.node + '\n\t' + self.node + ' -> '
            self.sdg += self.node
            self.node = ""
        else: 
            node = '"' + tipo + ' ' + var + '"'
            self.cfg += node + '\n\t' + node + ' -> '
            self.sdg += node

    def decl_set(self,tree):
        self.node_counter += 1
        tipo = tree.children[0].value
        var = tree.children[1].value
        if len(tree.children) == 3:
            self.node += '"' + tipo + ' ' + var
            self.visit(tree.children[2])
            self.cfg += self.node + '\n\t' + self.node + ' -> '
            self.sdg += self.node
            self.node = ""
        else: 
            node = '"' + tipo + ' ' + var + '"'
            self.cfg += node + '\n\t' + node + ' -> '
            self.sdg += node
        
    def decl_dict(self,tree):
        self.node_counter += 1
        tipo = tree.children[0].value
        var = tree.children[1].value
        if len(tree.children) == 3:
            self.node += '"' + tipo + ' ' + var
            self.visit(tree.children[2])
            self.cfg += self.node + '\n\t' + self.node + ' -> '
            self.sdg += self.node
            self.node = ""
        else: 
            node = '"' + tipo + ' ' + var + '"'
            self.cfg += node + '\n\t' + node + ' -> '
            self.sdg += node    

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
        self.node_counter += 1
        self.edge_counter += 1
        var = tree.children[0].value
        var = var.replace('"','\\"')
        value = self.visit(tree.children[1])
        node = '"' + var + ' = ' + value + '"'
        if node in self.instrs['atrib']:
            new_node = node[:-1] + '\'"'
            self.instrs['atrib'].append(new_node)
            node = new_node
        else:
            self.instrs['atrib'].append(node)
        if self.replace:
            if self.true == 1:
                self.cfg = self.cfg.replace('-> \n','-> ' + node + '[ label= "true" ];\n')
            elif self.then_else == 1:
                self.cfg = self.cfg.replace('-> \n','-> ' + node + '[ label= "then" ];\n')
            elif self.then_else == 2:
                self.cfg = self.cfg.replace('-> \n','-> ' + node + '[ label= "else" ];\n')
            else:
                self.cfg = self.cfg.replace('-> \n','-> ' + node + '\n')
            self.replace = 0
        self.sdg += node
        if self.true == 1: 
            self.cfg += node + '[ label= "true" ];\n\t' + node + ' -> '
            self.true = 0
        elif self.then_else == 1:
            self.cfg += node + '[ label= "then" ];\n\t' + node + ' -> '
            self.sdg += ' [ label="then" ];'
            self.then_else = 0
        elif self.then_else == 3:
            self.sdg += ' [ label="then" ];'
            self.then_else = 0
        elif self.then_else == 2:
            self.cfg += node + '[ label= "else" ];\n\t' + node + ' -> '
            self.sdg += ' [ label="else" ];'
            self.then_else = 0
        elif self.then_else == 4:
            self.sdg += ' [ label="else" ];'
            self.then_else = 0
        else: 
            self.cfg += node + '\n\t' + node + ' -> '
        

    def instr_read(self,tree):
        self.node_counter += 1
        self.edge_counter += 1
        var = tree.children[2].value
        var = var.replace('"','\\"')
        node = '"' + tree.children[0] + tree.children[1] + var + tree.children[3] + '"'
        if node in self.instrs['read']:
            new_node = node[:-1] + '\'"'
            self.instrs['read'].append(new_node)
            node = new_node
        else:
            self.instrs['read'].append(node)
        if self.replace:
            if self.true == 1:
                self.cfg = self.cfg.replace('-> \n','-> ' + node + '[ label= "true" ];\n')
            elif self.then_else == 1:
                self.cfg = self.cfg.replace('-> \n','-> ' + node + '[ label= "then" ];\n')
            elif self.then_else == 2:
                self.cfg = self.cfg.replace('-> \n','-> ' + node + '[ label= "else" ];\n')
            else:
                self.cfg = self.cfg.replace('-> \n','-> ' + node + '\n')
            self.replace = 0
        self.sdg += node
        if self.true == 1: 
            self.cfg += node + '[ label= "true" ];\n\t' + node + ' -> '
            self.true = 0
        elif self.then_else == 1:
            self.cfg += node + '[ label= "then" ];\n\t' + node + ' -> '
            self.sdg += ' [ label="then" ];'
            self.then_else = 0
        elif self.then_else == 3:
            self.sdg += ' [ label="then" ];'
            self.then_else = 0
        elif self.then_else == 2:
            self.cfg += node + '[ label= "else" ];\n\t' + node + ' -> '
            self.sdg += ' [ label="else" ];'
            self.then_else = 0
        elif self.then_else == 4:
            self.sdg += ' [ label="else" ];'
            self.then_else = 0
        else: 
            self.cfg += node + '\n\t' + node + ' -> '
    
    def instr_write(self,tree):
        self.node_counter += 1
        self.edge_counter += 1
        self.visit(tree.children[2])
        var = self.current
        self.current = ""
        node = '"' + tree.children[0] + tree.children[1] + var + tree.children[3] + '"'
        if node in self.instrs['write']:
            new_node = node[:-1] + '\'"'
            self.instrs['write'].append(new_node)
            node = new_node
        else:
            self.instrs['write'].append(node)
        if self.replace:
            if self.true == 1:
                self.cfg = self.cfg.replace('-> \n','-> ' + node + '[ label= "true" ];\n')
            elif self.then_else == 1:
                self.cfg = self.cfg.replace('-> \n','-> ' + node + '[ label= "then" ];\n')
            elif self.then_else == 2:
                self.cfg = self.cfg.replace('-> \n','-> ' + node + '[ label= "else" ];\n')
            else:
                self.cfg = self.cfg.replace('-> \n','-> ' + node + '\n')
            self.replace = 0
        self.sdg += node
        if self.true == 1: 
            self.cfg += node + '[ label= "true" ];\n\t' + node + ' -> '
            self.true = 0
        elif self.then_else == 1:
            self.cfg += node + '[ label= "then" ];\n\t' + node + ' -> '
            self.sdg += ' [ label="then" ];'
            self.then_else = 0
        elif self.then_else == 3:
            self.sdg += ' [ label="then" ];'
            self.then_else = 0
        elif self.then_else == 2:
            self.cfg += node + '[ label= "else" ];\n\t' + node + ' -> '
            self.sdg += ' [ label="else" ];'
            self.then_else = 0
        elif self.then_else == 4:
            self.sdg += ' [ label="else" ];'
            self.then_else = 0
        else: 
            self.cfg += node + '\n\t' + node + ' -> '

    def instr_if(self,tree):
        self.node_counter += 1
        self.edge_counter += 2
        self.visit(tree.children[2])
        cond = self.current
        self.current = ""
        node = '"' + tree.children[0] + tree.children[1] + str(cond) + tree.children[3] + '"'
        if node in self.instrs['if']:
            new_node = node[:-1] + '\'"'
            self.instrs['if'].append(new_node)
            node = new_node
        else:
            self.instrs['if'].append(node)
        if self.replace:
            if self.true == 1:
                self.cfg = self.cfg.replace('-> \n','-> ' + node + '[ label= "true" ];\n')
            elif self.then_else == 1:
                self.cfg = self.cfg.replace('-> \n','-> ' + node + '[ label= "then" ];\n')
            elif self.then_else == 2:
                self.cfg = self.cfg.replace('-> \n','-> ' + node + '[ label= "else" ];\n')
            else:
                self.cfg = self.cfg.replace('-> \n','-> ' + node + '\n')
            self.replace = 0
        self.sdg += node
        if self.true == 1: 
            self.cfg += node + '[ label= "true" ];\n\t'
            self.true = 0
        elif self.then_else == 1:
            self.cfg += node + '[ label= "then" ];\n\t' + node + ' -> '
            self.sdg += ' [ label="then" ];'
            self.then_else = 0
        elif self.then_else == 3:
            self.sdg += ' [ label="then" ];'
            self.then_else = 0
        elif self.then_else == 2:
            self.cfg += node + '[ label= "else" ];\n\t' + node + ' -> '
            self.sdg += ' [ label="else" ];'
            self.then_else = 0
        elif self.then_else == 4:
            self.sdg += ' [ label="else" ];'
            self.then_else = 0
        else: 
            self.cfg += node + '\n\t'
        self.cfg += node + '[shape=diamond];\n\t' + node + ' -> '
        i = 0
        while (i < len(tree.children[5].children)):
            self.sdg += '\n\t' + node + ' -> '
            if i == 0: self.true = 1
            self.visit(tree.children[5].children[i])
            i += 1
        self.cfg += '\n\t' + node + ' -> '
        self.replace = 1

    def instr_if_else(self,tree):
        self.node_counter += 1
        self.edge_counter += 2
        self.visit(tree.children[2])
        cond = self.current
        self.current = ""
        node = '"' + tree.children[0] + tree.children[1] + str(cond) + tree.children[3] + '"'
        if node in self.instrs['if_else']:
            new_node = node[:-1] + '\'"'
            self.instrs['if_else'].append(new_node)
            node = new_node
        else:
            self.instrs['if_else'].append(node)
        if self.replace:
            if self.true == 1:
                self.cfg = self.cfg.replace('-> \n','-> ' + node + '[ label= "true" ];\n')
            elif self.then_else == 1:
                self.cfg = self.cfg.replace('-> \n','-> ' + node + '[ label= "then" ];\n')
            elif self.then_else == 2:
                self.cfg = self.cfg.replace('-> \n','-> ' + node + '[ label= "else" ];\n')
            else:
                self.cfg = self.cfg.replace('-> \n','-> ' + node + '\n')
            self.replace = 0
        
        self.sdg += node
        if self.true == 1: 
            self.cfg += node + '[ label= "true" ];\n\t'
            self.true = 0
        elif self.then_else == 1:
            self.cfg += node + '[ label= "then" ];\n\t' + node + ' -> '
            self.sdg += ' [ label="then" ];'
            self.then_else = 0
        elif self.then_else == 3:
            self.sdg += ' [ label="then" ];'
            self.then_else = 0
        elif self.then_else == 2:
            self.cfg += node + '[ label= "else" ];\n\t' + node + ' -> '
            self.sdg += ' [ label="else" ];'
            self.then_else = 0
        elif self.then_else == 4:
            self.sdg += ' [ label="else" ];'
            self.then_else = 0
        else:
            self.cfg += node + '\n\t'
        self.cfg += node + '[shape=diamond];\n\t' + node + ' -> '
        i = 0
        while (i < len(tree.children[5].children)):
            self.sdg += '\n\t' + node + ' -> '
            if i == 0: self.then_else = 1
            else: self.then_else = 3
            self.visit(tree.children[5].children[i])
            i += 1
        self.cfg += '\n\t' + node + ' -> '
        i = 0
        while (i < len(tree.children[9].children)):
            self.sdg += '\n\t' + node + ' -> '
            if i == 0: self.then_else = 2
            else: self.then_else = 4
            self.visit(tree.children[9].children[i])
            i += 1
        self.replace = 1
        
    def instr_for(self,tree):
        self.node_counter += 1
        self.edge_counter += 1
        self.visit(tree.children[5])
        cond = self.current
        cond = cond.replace('"','\\"')
        self.current = ""
        node = '"' + tree.children[0] + tree.children[1] + str(cond) + tree.children[9] + '"'
        if node in self.instrs['for']:
            new_node = node[:-1] + '\'"'
            self.instrs['for'].append(new_node)
            node = new_node
        else:
            self.instrs['for'].append(node)
        decl = '"' + tree.children[2].value + ' = ' + self.visit(tree.children[3]) + '"'
        if decl in self.instrs['for']:
            new_decl = decl[:-1] + '\'"'
            self.instrs['for'].append(new_decl)
            decl = new_decl
        else:
            self.instrs['for'].append(decl)
        inc = '"' + tree.children[7].value + ' = ' + self.visit(tree.children[8]) + '"'
        if inc in self.instrs['for']:
            new_inc = inc[:-1] + '\'"'
            self.instrs['for'].append(new_inc)
            inc = new_inc
        else:
            self.instrs['for'].append(inc)
        if self.replace:
            if self.true == 1:
                self.cfg = self.cfg.replace('-> \n','-> ' + decl + '[ label= "true" ];\n')
            elif self.then_else == 1:
                self.cfg = self.cfg.replace('-> \n','-> ' + decl + '[ label= "then" ];\n')
            elif self.then_else == 2:
                self.cfg = self.cfg.replace('-> \n','-> ' + decl + '[ label= "else" ];\n')
            else:
                self.cfg = self.cfg.replace('-> \n','-> ' + node + '\n')
            self.replace = 0
        if self.true == 1:
            self.cfg += decl + '[ label= "true" ];\n\t' + decl + ' -> '
            self.true = 0
        elif self.then_else == 1:
            self.cfg += decl + '[ label= "then" ];\n\t' + decl + ' -> '
        elif self.then_else == 2:
            self.cfg += decl + '[ label= "else" ];\n\t' + decl + ' -> '
        else:
            self.cfg += decl + '\n\t' + decl + ' -> '
        self.cfg += node + '\n\t' + node + '[shape=circle];\n\t' + node + ' -> '
        pre = re.search(r'".+" -> $',self.sdg)[0]
        self.edge_counter += 3
        self.sdg += decl
        self.node_counter += 1
        if self.then_else == 1 or self.then_else == 3:
            self.sdg += ' [ label="then" ];'
        elif self.then_else == 2 or self.then_else == 4:
            self.sdg += ' [ label="else" ];'
        self.sdg += '\n\t' + pre + node
        if self.then_else == 1 or self.then_else == 3:
            self.sdg += ' [ label="then" ];'
            self.then_else = 0
        elif self.then_else == 2 or self.then_else == 4:
            self.sdg += ' [ label="else" ];'
            self.then_else = 0
        i = 0
        while (i < len(tree.children[11].children)):
            self.sdg += '\n\t' + node + ' -> '
            if i == 0: self.true = 1
            self.visit(tree.children[11].children[i])
            i += 1
        self.sdg += '\n\t' + node + ' -> ' + inc
        self.node_counter += 1
        self.cfg = self.cfg.replace('-> \n','-> ' + inc + '\n')
        self.cfg += inc + '\n\t' + inc + ' -> ' + node + '\n\t' + node + ' -> '

    def instr_while(self,tree):
        self.node_counter += 1
        self.edge_counter += 2
        self.visit(tree.children[2])
        cond = self.current
        cond = cond.replace('"','\\"')
        self.current = ""
        node = '"' + tree.children[0] + tree.children[1] + str(cond) + tree.children[3] + '"'
        if node in self.instrs['while']:
            new_node = node[:-1] + '\'"'
            self.instrs['while'].append(new_node)
            node = new_node
        else:
            self.instrs['while'].append(node)
        if self.replace:
            if self.true == 1:
                self.cfg = self.cfg.replace('-> \n','-> ' + node + '[ label= "true" ];\n')
            elif self.then_else == 1:
                self.cfg = self.cfg.replace('-> \n','-> ' + node + '[ label= "then" ];\n')
            elif self.then_else == 2:
                self.cfg = self.cfg.replace('-> \n','-> ' + node + '[ label= "else" ];\n')
            else:
                self.cfg = self.cfg.replace('-> \n','-> ' + node + '\n')
            self.replace = 0
        if self.true == 1:
            self.cfg += node + '[ label= "true" ];'
            self.true = 0
        elif self.then_else == 1:
            self.cfg += node + '[ label= "then" ];'
        elif self.then_else == 2:
            self.cfg += node + '[ label= "else" ];'
        else:
            self.cfg += node
        self.cfg += '\n\t' + node + '[shape=circle];\n\t' + node + ' -> '
        self.sdg += node
        if self.then_else == 1 or self.then_else == 3:
            self.sdg += ' [ label="then" ];'
            self.then_else = 0
        elif self.then_else == 2 or self.then_else == 4:
            self.sdg += ' [ label="else" ];'
            self.then_else = 0
        i = 0
        while (i < len(tree.children[5].children)):
            self.sdg += '\n\t' + node + ' -> '
            if i == 0: self.true = 1
            self.visit(tree.children[5].children[i])
            i += 1
        self.cfg += node + '\n\t' + node + ' -> '

    def instr_repeat(self,tree):
        self.node_counter += 1
        node = '"' + tree.children[0] + '"'
        if node in self.instrs['repeat']:
            new_node = node[:-1] + '\'"'
            self.instrs['repeat'].append(new_node)
            node = new_node
        else:
            self.instrs['repeat'].append(node)
        if self.replace:
            if self.true == 1:
                self.cfg = self.cfg.replace('-> \n','-> ' + node + '[ label= "true" ];\n')
            elif self.then_else == 1:
                self.cfg = self.cfg.replace('-> \n','-> ' + node + '[ label= "then" ];\n')
            elif self.then_else == 2:
                self.cfg = self.cfg.replace('-> \n','-> ' + node + '[ label= "else" ];\n')
            else:
                self.cfg = self.cfg.replace('-> \n','-> ' + node + '\n')
            self.replace = 0
        if self.true == 1:
            self.cfg += node + '[ label= "true" ];'
            self.true = 0
        elif self.then_else == 1:
            self.cfg += node + '[ label= "then" ];'
        elif self.then_else == 2:
            self.cfg += node + '[ label= "else" ];'
        else:
            self.cfg += node
        self.cfg += '\n\t' + node + '[shape=circle];\n\t' + node + ' -> '
        self.sdg += node
        if self.then_else == 1 or self.then_else == 3:
            self.sdg += ' [ label="then" ];'
            self.then_else = 0
        elif self.then_else == 2 or self.then_else == 4:
            self.sdg += ' [ label="else" ];'
            self.then_else = 0
        i = 0
        while (i < len(tree.children[2].children)):
            self.sdg += '\n\t' + node + ' -> '
            self.edge_counter += 1
            self.visit(tree.children[2].children[i])
            i += 1
        self.sdg += '\n\t' + node + ' -> '
        self.edge_counter += 3
        self.node_counter += 1
        self.visit(tree.children[3])
        self.cfg += node + '[ label= "true" ];'

    def until(self,tree):
        self.visit(tree.children[2])
        cond = self.current
        cond = cond.replace('"','\\"')
        self.current = ""
        node = '"' + tree.children[0] + tree.children[1] + str(cond) + tree.children[3] + '"'
        if node in self.instrs['repeat']:
            new_node = node[:-1] + '\'"'
            self.instrs['repeat'].append(new_node)
            node = new_node
        else:
            self.instrs['repeat'].append(node)
        self.cfg += node + '\n\t' + node + ' -> \n\t' + node + ' -> '
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

def graphs(code):
    grammar = open('lpis2.txt').read()
    test_code = open(code).read()

    p = Lark(grammar)
    parse_tree = p.parse(test_code)
    data = LPIS2_Interpreter().visit(parse_tree)
    data['node_counter'] += 1

    mccabe = int(data['edge_counter']) - int(data['node_counter']) + 2
    data['cfg'] = data['cfg'].replace('-> \n','-> "FIM"\n')
    data['cfg'] += '"FIM"\n}'
    data['sdg'] += '\n}'
    
    with open("images/cfg.dot",'w') as f:
        f.write(data['cfg'])

    with open("images/sdg.dot",'w') as g:
        g.write(data['sdg'])

    (cfg,) = pydot.graph_from_dot_file('images/cfg.dot')
    cfg.write_png('images/cfg.png')

    (sdg,) = pydot.graph_from_dot_file('images/sdg.dot')
    sdg.write_png('images/sdg.png')

    with open("page.html",'r') as page:
        html = page.read()
        html += '''\n<h1>CFG</h1>
        <img src="images/cfg.png" alt="erro cfg">
        <h1>SDG</h1>
        <img src="images/sdg.png" alt="erro sdg">
        <p>Da forma como proposto e contruído o grafo SDG, nunca ocorrerão casos/zonas de código inalcansável (grafos de ilha).</p>
        <p>Complexidade de McCabe = ''' + str(data['edge_counter']) + ' - ' + str(data['node_counter']) + ' + 2 = ' + str(mccabe)

    with open("page.html",'w') as page:
        page.write(html)