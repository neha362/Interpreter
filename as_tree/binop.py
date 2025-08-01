from AST_Node import *

#class Binop stores appropriate functions for binary operations
class Binop(AST_Node):
    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op
    
    # placeholder to_string function inherited by other tree nodes
    def to_string(self, tabs=0):
        string = ""
        for _ in range(tabs):
            string += tab
        string += "|-> " + type(self).__name__ + ", op = " + ("" if self.op == None else self.op.symbol)
        string += "\n" + self.left.to_string(tabs + 1)
        if self.right != None:
            string += "\n" + self.right.to_string(tabs + 1)
        return string
    
    # placeholder __str__ overriden from object class for child classes
    def __str__(self):
        return self.left.__str__() + " " + self.op.symbol + " " + self.right.__str__()
    
    