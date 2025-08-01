from AST_Node import *
from declaration import *

#class DeclarationList stores appropriate functions for a list of declarations
class DeclarationList(AST_Node):
    def __init__(self, declarations):
        self.declarations = declarations

    def invariant(self):
        for i in self.declarations:
            if not isinstance(i, Declaration):
                return False
        return True
    
    def interpret(self, env):
        for i in self.declarations:
            env = i.interpret(env)
        self.env = env
        return self.env
    
    def to_string(self, tabs=0):
        string = ""
        for _ in range(tabs):
            string += tab
        string += "DECLARATIONS\n"
        for i in self.declarations:
            string += i.to_string(tabs + 1)
        return string
    
    def __str__(self):
        string = "DECLARATION LIST\n"
        for i in self.statements:
            string +=  tab + i.__str__() + "\n"
        return string
    