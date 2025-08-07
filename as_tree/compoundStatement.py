from as_tree.AST_Node import *
from as_tree.statementList import *

#class CompoundStatement stores appropriate functions for compound statements
class CompoundStatement(AST_Node):
    def __init__(self, statements):
        self.statements = statements
        self.env = None
    
    def invariant(self):
        return isinstance(self.statements, StatementList)

    def interpret(self, env):
        res, self.env = self.statements.interpret(env)
        return res, env

    def to_string(self, tabs=0):
        if isinstance(self.statements, list):
            string = ""
            for i in self.statements:
                string += i.to_string(tabs) + "\n" 
            return string
        string = ""
        for _ in range(tabs):
            string += self.tab
        string += "|-> " + type(self).__name__ + " " + (str(self.env) if self.env != None else "") + "\n" + self.statements.to_string(tabs + 1)
        return string

    def __str__(self):
        return "COMPOUND STATEMENT \n\t" + (AST_Node.print_env(self.env) if self.env != None else "") + "\n" + self.statements.__str__()
    
EMPTY = CompoundStatement([])