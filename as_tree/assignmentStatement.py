from as_tree.statement import *
from as_tree.variable import Variable, check_val_type
from as_tree.expr import *

#the AssignmentStatement class contains relevant functions for assignment statements
class AssignmentStatement(Statement):
    def __init__(self, variable, expr):
        assert isinstance(variable, Variable) and isinstance(expr, Expr), "assignment statement invariant violated "
        self.variable = variable
        self.expr = expr
    
    def invariant(self):
        return isinstance(self.variable, Variable) and isinstance(self.expr, Expr)
    
    def interpret(self, global_env):
        if self.variable.id in global_env:
            value = self.expr.interpret(global_env)
            _, val_type = global_env[self.variable.id]
            value, val_type = check_val_type(value, val_type)
            global_env[self.variable.id] = value, val_type
            return True, global_env
        #TODO:add declarations required in scope
        raise Exception("variable not in environment")
    
    def to_string(self, tabs=0):
        string = ""
        for _ in range(tabs):
            string += self.tab
        return string + "|-> := \n" + self.variable.to_string(tabs + 1) + " " + "\n" + self.expr.to_string(tabs + 1)

    def __str__(self):
        return self.variable.__str__() + " := " + self.expr.__str__() 