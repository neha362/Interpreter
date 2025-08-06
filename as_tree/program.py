from as_tree import *
from as_tree.statementList import *
from as_tree.variable import *
from as_tree.declarationList import *

#class Program stores appropriate functions for high-level programs
class Program(AST_Node):
    def __init__(self, name, declarations, statements, env={}):
        self.declarations = declarations
        self.statements = statements
        self.env = env
        self.name = name
    
    def invariant(self):
        return isinstance(self.statements, StatementList)and isinstance(self.name, Variable) and isinstance(self.declarations, DeclarationList)

    def interpret(self):
        if not self.invariant():
            raise Exception("invalid program node")
        self.env = self.declarations.interpret(self.env)
        for i in self.statements.interpret(self.env):
            if not i:
                return False
        return True 

    def to_string(self, tabs=0):
        return "PROGRAM (" + self.name.id + ")\n" + self.declarations.to_string(tabs + 1) + self.statements.to_string(tabs + 1)

    def __str__(self):
        return "PROGRAM (" + self.name.id + ")\n" + AST_Node.print_env(self.env) + "\n" + self.declarations.__str__() + "\n" + self.statements.__str__()