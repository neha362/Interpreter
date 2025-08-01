from AST_Node import *
from statementList import *
from variable import *
from declarationList import *

#class Program stores appropriate functions for high-level programs
class Program(AST_Node):
    def __init__(self, name, declarations, statements):
        self.declarations = declarations
        self.statements = statements
        self.env = env
        self.name = name
    
    def invariant(self):
        return isinstance(self.statements, StatementList)and isinstance(self.name, Variable) and isinstance(self.declarations, DeclarationList)

    def interpret(self):
        if not self.invariant():
            raise Exception("invalid program node")
        self.env = self.declarations.interpret()
        self.name = self.name.interpret()
        for i in self.statements.interpret(self.env):
            if not i:
                return False
        return True 

    def to_string(self, tabs=0):
        return "PROGRAM (" + self.name + ")\n" + self.statements.to_string(tabs + 1)

    def __str__(self):
        return "PROGRAM (" + self.name + ")\n" + self.statements.__str__()