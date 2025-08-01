from AST_Node import *

#class Declaration stores appropriate functions for declarations
class Declaration(AST_Node):
    def __init__(self, vars, type):
        self.vars = vars
        self.type = type