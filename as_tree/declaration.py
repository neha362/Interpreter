from as_tree.AST_Node import *

#class Declaration stores appropriate functions for declarations
class Declaration(AST_Node):
    def __init__(self, vars, type):
        self.vars = vars
        self.type = type

    def invariant(self):
        for i in self.vars:
            if not isinstance(i, Variable):
                return False
        return self.vars and type in (INTEGER, CHAR, REAL, FUNCTION)

    def interpret(self, env):
        for i in self.vars:
            if i.id in env:
                raise Exception("variable already defined")
            env[i.id] = (None if self.type == CHAR else 0, self.type)
        return env

    def to_string(self, tabs=0):
        string = ""
        for _ in range(tabs):
            string += "\t"
        string += "|-> " + str(self.vars[0])
        for i in self.vars[1:]:
            string += ", " + str(i)
        return string + ": " + self.type
    
    def __str__(self):
        return str([str(i) for i in self.vars]) + ": " + self.type