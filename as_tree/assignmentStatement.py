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
    
    def interpret(self, env):
        if self.variable.id in env:
            value = self.expr.interpret(env)
            _, val_type = env[self.variable.id]
            value, val_type = check_val_type(value, val_type)
            env[self.variable.id] = value, val_type
            return True, env
        value = self.expr.interpret(env)
        if isinstance(value, int):
            val_type = INTEGER
        elif isinstance(value, float):
            val_type = REAL 
        elif isinstance(value, chr):
            val_type = CHAR
        elif isinstance(value, function):
            val_type = FUNCTION
        else:
            raise Exception("unknown type encountered" + type)
        env[self.variable.id] = value, val_type
        return True, env
    
    def to_string(self, tabs=0):
        string = ""
        for _ in range(tabs):
            string += self.tab
        return string + "|-> := \n" + self.variable.to_string(tabs + 1) + " " + "\n" + self.expr.to_string(tabs + 1)

    def __str__(self):
        return self.variable.__str__() + " := " + self.expr.__str__() 