from AST_Node import *
from statement import *
from variable import *
from expr import *


#the AssignmentStatement class contains relevant functions for assignment statements
class AssignmentStatement(Statement):
    def __init__(self, variable, expr):
        assert isinstance(variable, Variable) and isinstance(expr, Expr), "assignment statement invariant violated "
        self.variable = variable
        self.expr = expr
    
    def invariant(self):
        return isinstance(self.variable, Variable) and isinstance(self.expr, Expr)
    
    def interpret(self, env):
        env[self.variable.id] = self.expr.interpret(env)
        return True, env
    
    def to_string(self, tabs=0):
        string = ""
        for _ in range(tabs):
            string += tab
        return string + "|-> := \n" + self.variable.to_string(tabs + 1) + " " + "\n" + self.expr.to_string(tabs + 1)

    def __str__(self):
        return self.variable.__str__() + " := " + self.expr.__str__() 