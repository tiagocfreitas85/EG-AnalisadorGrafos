from lark import Lark
from lark.visitors import Interpreter
from aux import *
from sugestions import *

class LPIS2_Interpreter(Interpreter): 
    def __init__(self):
        self.regs = Registers()
        self.used = set()
        self.instrs = {'atrib': 0, 'read': 0, 'write': 0, 'if': 0, 'if_else': 0, 'for': 0, 'while': 0, 'repeat': 0}
        self.current = ""
        self.level = 0
        self.inside = 0
        self.htmli = ""
        self.output = {}

    def start(self,tree):
        self.visit(tree.children[0])
        self.htmli += '<div class="code">' + tree.children[1].value + '</div>\n'
        self.visit_children(tree.children[2])
        self.output['regs'] = self.regs.to_string()
        self.output['used'] = self.used
        self.output['instrs'] = self.instrs
        self.output['inside'] = self.inside
        self.output['html'] = self.htmli
        return(self.output)

    def decls(self,tree):
        self.visit_children(tree)
          
    def decl(self,tree):
        self.visit_children(tree)
        self.htmli += ';</div>\n'

    def decl_int(self,tree):
        var = tree.children[1].value
        
        var_error = None
        if var_verifier(var,self.regs) == 1 or var_verifier(var,self.regs) == 2:
            var_error = "variável '" + var + "' já está declarada"
        error = None
        if len(tree.children) == 3:
            value = self.visit(tree.children[2])
            if not(value.isdigit() or " " in value):
                if '"' in value or value == 'true' or value == 'false':
                    error = value + " não é do tipo 'int'"
                    print(error)
                else:
                    vrf = value_verifier(value,self.regs)
                    if vrf == "A":
                        error = "variável '" + value + "' vazia"
                        print(error)
                    elif vrf == "B":
                        error = "variável '" + value + "' inexistente"
                        print(error)
                    elif vrf == "C":
                        vl = value.split('[')[0]
                        error = "'" + vl + "' não possui esse índice"
                        print(error)
                    elif vrf == "D":
                        vl = value.split('[')[0]
                        error = "'" + vl + "' não possui essa entrada"
                        print(error)
                    elif type_verifier(var,vrf,self.regs) == 0:
                        error = "'" + value + "' não é do tipo 'int'"
                        print(error)
                    else:
                        self.regs.int[var] = value
            else:
                if value.isdigit():
                    self.regs.int[var] = value
                else:
                    self.regs.int[var] = value
            if error != None and var_error != None:
                self.htmli += '<div class="code">' + tree.children[0].value + ' ' + error_html(var_error,var) + ' = ' + error_html(error,str(value))
            elif error != None and var_error == None:
                self.htmli += '<div class="code">' + tree.children[0].value + ' ' + var + ' = ' + error_html(error,str(value))
            elif error == None and var_error != None:
                self.htmli += '<div class="code">' + tree.children[0].value + ' ' + error_html(var_error,var) + ' = ' + str(value)
            else:
                self.htmli += '<div class="code">' + tree.children[0].value + ' ' + var + ' = ' + str(value)

        else:
            if var_error == None:
                self.htmli += '<div class="code">' + tree.children[0].value + ' ' + var
                value = None
                self.regs.int[var] = value
            else:
                self.htmli += '<div class="code">' + tree.children[0].value + ' ' + error_html(var_error,var)
        

    def decl_boolean(self,tree):
        var = tree.children[1].value
        var_error = None
        if var_verifier(var,self.regs) == 1 or var_verifier(var,self.regs) == 2:
            var_error = "variável '" + var + "' já está declarada"
        error = None
        if len(tree.children) == 3:
            value = self.visit(tree.children[2])
            if not(value == 'true' or value == 'false' or " " in value):
                if value.isdigit() or '"' in value:
                    error = str(value) + " não é do tipo 'boolean'"
                    print(error)
                else:
                    vrf = value_verifier(value,self.regs)
                    if vrf == "A":
                        error = "variável '" + value + "' vazia"
                        print(error)
                    elif vrf == "B":
                        error = "variável '" + value + "' inexistente"
                        print(error)
                    elif vrf == "C":
                        vl = value.split('[')[0]
                        error = "'" + vl + "' não possui esse índice"
                        print(error)
                    elif vrf == "D":
                        vl = value.split('[')[0]
                        error = "'" + vl + "' não possui essa entrada"
                        print(error)
                    elif type_verifier(var,vrf,self.regs) == 0:
                        error = "'" + value + "' não é do tipo 'boolean'"
                        print(error)
                    else:
                        self.regs.boolean[var] = value
            else:
                self.regs.boolean[var] = value
            if error != None and var_error != None:
                self.htmli += '<div class="code">' + tree.children[0].value + ' ' + error_html(var_error,var) + ' = ' + error_html(error,str(value))
            elif error != None and var_error == None:
                self.htmli += '<div class="code">' + tree.children[0].value + ' ' + var + ' = ' + error_html(error,str(value))
            elif error == None and var_error != None:
                self.htmli += '<div class="code">' + tree.children[0].value + ' ' + error_html(var_error,var) + ' = ' + str(value)
            else:
                self.htmli += '<div class="code">' + tree.children[0].value + ' ' + var + ' = ' + str(value)
        else:
            if var_error == None:
                self.htmli += '<div class="code">' + tree.children[0].value + ' ' + var
                value = None
                self.regs.boolean[var] = value
            else:
                self.htmli += '<div class="code">' + tree.children[0].value + ' ' + error_html(var_error,var)
        

    def decl_string(self,tree):
        var = tree.children[1].value
        var_error = None
        if var_verifier(var,self.regs) == 1 or var_verifier(var,self.regs) == 2:
            var_error = "variável '" + var + "' já está declarada"
        error = None
        if len(tree.children) == 3:
            value = self.visit(tree.children[2])
            if not('"' in str(value)):
                if value.isdigit() or value == 'true' or value == 'false':
                    error = "'" + str(value) + "' não é do tipo 'string'"
                    print(error)
                else:
                    vrf = value_verifier(value,self.regs)
                    if vrf == "A":
                        error = "variável '" + value + "' vazia"
                        print(error)
                    elif vrf == "B":
                        error = "variável '" + value + "' inexistente"
                        print(error)
                    elif vrf == "C":
                        vl = value.split('[')[0]
                        error = "'" + vl + "' não possui esse índice"
                        print(error)
                    elif vrf == "D":
                        vl = value.split('[')[0]
                        error = "'" + vl + "' não possui essa entrada"
                        print(error)
                    elif type_verifier(var,vrf,self.regs) == 0:
                        error = "'" + value + "' não é do tipo 'string'"
                        print(error)
                    else:
                        self.regs.string[var] = value
            else:
                self.regs.string[var] = value
            if error != None and var_error != None:
                self.htmli += '<div class="code">' + tree.children[0].value + ' ' + error_html(var_error,var) + ' = ' + error_html(error,str(value))
            elif error != None and var_error == None:
                self.htmli += '<div class="code">' + tree.children[0].value + ' ' + var + ' = ' + error_html(error,str(value))
            elif error == None and var_error != None:
                self.htmli += '<div class="code">' + tree.children[0].value + ' ' + error_html(var_error,var) + ' = ' + str(value)
            else:
                self.htmli += '<div class="code">' + tree.children[0].value + ' ' + var + ' = ' + str(value)
        else: 
            if var_error == None:
                self.htmli += '<div class="code">' + tree.children[0].value + ' ' + var
                value = None
                self.regs.string[var] = value
            else:
                self.htmli += '<div class="code">' + tree.children[0].value + ' ' + error_html(var_error,var)

    def decl_list(self,tree):
        var = tree.children[1].value
        var_error = None
        if var_verifier(var,self.regs) == 1 or var_verifier(var,self.regs) == 2:
            var_error = "variável '" + var + "' já está declarada"
        if var_error != None:
            self.htmli += '<div class="code">' + tree.children[0].value + ' ' + error_html(var_error,var) + ' = ' + str(self.visit(tree.children[2]))
        else:
            self.htmli += '<div class="code">' + tree.children[0].value + ' ' + var
            self.regs.list[var] = self.visit(tree.children[2])

    def decl_tuple(self,tree):
        name = tree.children[1].value
        self.htmli += '<div class="code">' + tree.children[0].value + ' ' + name
        if len(tree.children) == 3:
            var = self.visit(tree.children[2])
        else: var = ()
        self.regs.tuple[name] = var

    def decl_set(self,tree):
        name = tree.children[1].value
        self.htmli += '<div class="code">' + tree.children[0].value + ' ' + name
        if len(tree.children) == 3:
            var = self.visit(tree.children[2])
        else: var = {}
        self.regs.set[name] = var
        

    def decl_dict(self,tree):
        name = tree.children[1].value
        self.htmli += '<div class="code">' + tree.children[0].value + ' ' + name
        if len(tree.children) == 3:
            var = self.visit(tree.children[2])
        else: var = dict()
        self.regs.dict[name] = var
        

    def decl_atrib(self,tree):
        self.visit(tree.children[1])
        aux = self.current
        self.current = ""
        return aux

    def decl_atrib_list(self,tree):
        res = []
        i = 2
        j = 3
        self.htmli += ' ' + tree.children[0] + ' ' + tree.children[1]
        if len(tree.children) > 3:
            while i < len(tree.children):
                self.visit(tree.children[i])
                value = self.current
                self.current = ""
                res.append(value)
                self.htmli += str(value)
                self.htmli += tree.children[j]
                i += 2
                j += 2
        else:
            self.htmli += tree.children[2]

        return res

    def decl_atrib_tuple(self,tree):
        res = []
        i = 2
        j = 3
        self.htmli += ' ' + tree.children[0] + ' ' + tree.children[1]
        if len(tree.children) > 3:
            while i < len(tree.children):
                self.visit(tree.children[i])
                value = self.current
                self.current = ""
                res.append(value)
                self.htmli += str(value)
                self.htmli += tree.children[j]
                i += 2
                j += 2
        else:
            self.htmli += tree.children[2]

        return tuple(res)

    def decl_atrib_set(self,tree):
        res = set()
        i = 2
        j = 3
        self.htmli += ' ' + tree.children[0] + ' ' + tree.children[1]
        if len(tree.children) > 3:
            while i < len(tree.children):
                self.visit(tree.children[i])
                value = self.current
                self.current = ""
                res.add(value)
                self.htmli += str(value)
                self.htmli += tree.children[j]
                i += 2
                j += 2
        else:
            self.htmli += tree.children[2]

        return res

    def decl_atrib_dict(self,tree):
        res = dict()
        i = 2
        j = 3
        self.htmli += ' ' + tree.children[0] + ' ' + tree.children[1]
        if len(tree.children) > 3:
            while i < len(tree.children):
                elem = tree.children[i]
                key = self.visit(elem)[0]
                dp = self.visit(elem)[1]
                self.current = ""
                self.visit(elem.children[2])
                value = self.current
                self.current = ""
                res[str(key)] = value
                self.htmli += key + dp + ' ' + str(value)
                self.htmli += tree.children[j]
                i += 2
                j += 2
    
        else:
            self.htmli += tree.children[2]
        return res

    def instrs(self,tree):
        self.visit_children(tree)

    def instr(self,tree):
        self.visit_children(tree)
    
    def instr_atrib(self,tree):
        flag = 1
        var_error = None
        val_error = None
        error = None
        self.instrs['atrib'] += 1
        if self.level > 0:
            self.inside += 1
        var = tree.children[0].value
        value = self.visit(tree.children[1])
        if value.isdigit() or ('[' not in value and '"' in value) or value == 'true' or value == 'false' or " " in value:
            flag = 0
        
        vrf1 = var_verifier(var,self.regs)
        if flag:
            vrf2 = value_verifier(value,self.regs)
        else: vrf2 = value
        

        if vrf1 == 3:
            var_error = "variável '" + var + "' inexistente"
            print(var_error)
        elif vrf1 == 4:
            var_error = "tuplos são imutáveis"
            print(var_error)
        elif vrf1 == 5:
            v = var.split('[')[0]
            var_error = "'" + v + "' não possui esse índice"
            print(var_error)
        elif flag and vrf2 == "A":
            val_error = "variável '" + value + "' vazia"
            print(val_error)
        elif flag and vrf2 == "B":
            val_error = "variável '" + value + "' inexistente"
            print(val_error)
        elif flag and vrf2 == "C":
            vl = value.split('[')[0]
            val_error = "'" + vl + "' não possui esse índice"
            print(val_error)
        elif flag and vrf2 == "D":
            vl = value.split('[')[0]
            val_error = "'" + vl + "' não possui essa entrada"
            print(val_error)
        else:
            if not(" " in value):
                if type_verifier(var,vrf2,self.regs) == 0:
                    error = "'" + var + "' e '" + str(value) + "' são de tipos diferentes"
                    print(error)
        
        i = 0
        self.htmli += '<div class="code">'
        while i != self.level:
            self.htmli += '\t'
            i += 1
        if error == None:
            if var_error != None and val_error != None:
                self.htmli += error_html(var_error,var) + ' = ' + error_html(val_error,str(value)) + tree.children[2] + '</div>\n'
            elif var_error != None and val_error == None:
                self.htmli += error_html(var_error,var) + ' = ' + str(value) + tree.children[2] + '</div>\n'
            elif var_error == None and val_error != None:
                self.htmli += var + ' = ' + error_html(val_error,str(value)) + tree.children[2] + '</div>\n'
                self.used.add(var)
            else:
                self.htmli += var + ' = ' + str(value) + tree.children[2] + '</div>\n'
                self.used.add(var)
        else:
            self.htmli += error_html(error,var + ' = ' + str(value)) + tree.children[2] + '</div>\n'

    def instr_read(self,tree):
        self.instrs['read'] += 1
        if self.level > 0:
            self.inside += 1
        error = None
        var = tree.children[2].value
        vrf = var_verifier(var,self.regs)
        if vrf == 3:
            error = "variável '" + var + "' inexistente"
            print(error)
        
        i = 0
        self.htmli += '<div class="code">'
        while i != self.level:
            self.htmli += '\t'
            i += 1
        if error != None:
            self.htmli += tree.children[0] + tree.children[1] + error_html(error,var) + tree.children[3] + tree.children[4] + '</div>\n'
        else:
            self.used.add(var)
            self.htmli += tree.children[0] + tree.children[1] + var + tree.children[3] + tree.children[4] + '</div>\n'
    
    def instr_write(self,tree):
        self.instrs['write'] += 1
        if self.level > 0:
            self.inside += 1
        self.visit(tree.children[2])
        var = self.current
        self.current = ""

        i = 0
        self.htmli += '<div class="code">'
        while i != self.level:
            self.htmli += '\t'
            i += 1
        self.htmli += tree.children[0] + tree.children[1] + str(var) + tree.children[3] + tree.children[4] + '</div>\n'
        vrf = var_verifier(var,self.regs)
        if vrf == 1 or vrf == 2:
            self.used.add(var)


    def instr_if(self,tree):
        self.instrs['if'] += 1
        if self.level > 0:
            self.inside += 1
        self.visit(tree.children[2])
        var = self.current
        self.current = ""
        i = 0
        self.htmli += '<div class="code">'
        while i != self.level:
            self.htmli += '\t'
            i += 1
        self.htmli += tree.children[0] + tree.children[1] + str(var) + tree.children[3] + tree.children[4]
        vrf = var_verifier(var,self.regs)
        if vrf == 1 or vrf == 2:
            self.used.add(var)
        self.level += 1
        if (len(tree.children[5].children) == 1) and (tree.children[5].children[0].children[0].data == 'instr_if'):
            self.htmli += ' //aninhado'
        self.htmli += '</div>\n'
        self.visit_children(tree.children[5])
        self.level -= 1
        i = 0
        self.htmli += '<div class="code">'
        while i != self.level:
            self.htmli += '\t'
            i += 1
        self.htmli += tree.children[6] + '</div>\n'
        

    def instr_if_else(self,tree):
        self.instrs['if_else'] += 1
        if self.level > 0:
            self.inside += 1
        self.visit(tree.children[2])
        var = self.current
        self.current = ""
        i = 0
        self.htmli += '<div class="code">'
        while i != self.level:
            self.htmli += '\t'
            i += 1
        self.htmli += tree.children[0] + tree.children[1] + str(var) + tree.children[3] + tree.children[4] + '</div>\n'
        vrf = var_verifier(var,self.regs)
        if vrf == 1 or vrf == 2:
            self.used.add(var)
        self.level += 1
        self.visit_children(tree.children[5])
        self.level -= 1
        i = 0
        self.htmli += '<div class="code">'
        while i != self.level:
            self.htmli += '\t'
            i += 1
        self.htmli += tree.children[6] + tree.children[7] + tree.children[8] + '</div>\n'
        self.level += 1
        self.visit_children(tree.children[9])
        self.level -= 1
        i = 0
        self.htmli += '<div class="code">'
        while i != self.level:
            self.htmli += '\t'
            i += 1
        self.htmli += tree.children[10] + '</div>\n'

    def instr_for(self,tree):
        self.instrs['for'] += 1
        if self.level > 0:
            self.inside += 1
        self.visit(tree.children[4])
        var = self.current
        self.current = ""
        i = 0
        self.htmli += '<div class="code">'
        while i != self.level:
            self.htmli += '\t'
            i += 1
        self.htmli += tree.children[0] + tree.children[1] + tree.children[2] + tree.children[3] + str(var) + tree.children[5] + tree.children[6] + '</div>\n'
        self.level += 1
        self.visit_children(tree.children[7])
        self.level -= 1
        i = 0
        self.htmli += '<div class="code">'
        while i != self.level:
            self.htmli += '\t'
            i += 1
        self.htmli += tree.children[8] + '</div>\n'

    def instr_while(self,tree):
        self.instrs['while'] += 1
        if self.level > 0:
            self.inside += 1
        self.visit(tree.children[2])
        var = self.current
        self.current = ""
        i = 0
        self.htmli += '<div class="code">'
        while i != self.level:
            self.htmli += '\t'
            i += 1
        self.htmli += tree.children[0] + tree.children[1] + str(var) + tree.children[3] + tree.children[4] + '</div>\n'
        vrf = var_verifier(var,self.regs)
        if vrf == 1 or vrf == 2:
            self.used.add(var)
        self.level += 1
        self.visit_children(tree.children[5])
        self.level -= 1
        i = 0
        self.htmli += '<div class="code">'
        while i != self.level:
            self.htmli += '\t'
            i += 1
        self.htmli += tree.children[6] + '</div>\n'

    def instr_repeat(self,tree):
        self.instrs['repeat'] += 1
        if self.level > 0:
            self.inside += 1
        i = 0
        self.htmli += '<div class="code">'
        while i != self.level:
            self.htmli += '\t'
            i += 1
        self.htmli += tree.children[0] + tree.children[1] + '</div>\n'
        self.level += 1
        self.visit_children(tree.children[2])
        self.visit(tree.children[3])
        self.level -= 1
        i = 0
        self.htmli += '<div class="code">'
        while i != self.level:
            self.htmli += '\t'
            i += 1
        self.htmli += tree.children[4] + '</div>\n'

    def until(self,tree):
        self.visit(tree.children[2])
        var = self.current
        self.current = ""
        i = 0
        self.htmli += '<div class="code">'
        vrf = var_verifier(var,self.regs)
        if vrf == 1 or vrf == 2:
            self.used.add(var)
        while i != self.level:
            self.htmli += '\t'
            i += 1
        self.htmli += tree.children[0] + tree.children[1] + str(var) + tree.children[3] + tree.children[4] + '</div>\n'

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
            self.current += var
        
grammar = open('lpis2.txt').read()
code = open('test_code.txt').read()
begin = open('html_begin.html').read()

p = Lark(grammar)
parse_tree = p.parse(code)
data = LPIS2_Interpreter().visit(parse_tree)

html = begin + data['html']
html += '''
</code></pre>
'''


for key in data:
    if key == "regs":
        print(key)
        html += '''
        <h1>Registos</h1><p>'''
        for t in data[key]:
            print ("\t" + t + ": " + str(data[key][t]))
            html += '''
            <li>\t''' + t + ": " + str(data[key][t]) + "</li>"
        html += "</p>"
    elif key == "instrs":
        print(key + ": " + str(data[key]))
        html += '''
        <h1>Intruções</h1><p>
        ''' 
        html += str(data[key]) + "</p>"
        total = sum(data[key].values())
        html += '''
        <p><b>Total: </b>''' + str(total) + '</p>'
        print("total_instrs" + str(total))
    elif key == "used":
        print(key + ": " + str(data[key]))
        html += '''
        <h1>Variáveis usadas</h1><p>
        ''' 
        html += str(data[key]) + "</p>"
    elif key == "inside":
        print(key + ": " + str(data[key]))
        html += '''
        <p><b>Total dentro de outras estruturas: </b>''' + str(data[key]) + '</p>'

f = open("page.html",'w',encoding = 'utf-8')

html = add_suggestions(html)
f.write(html)
f.close()
    