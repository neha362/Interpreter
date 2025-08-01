from compoundStatement import *
from assignmentStatement import *

# class Statement stores appropriate functions for statements
class Statement(AST_Node):
    def __init__(self, statement):
        assert isinstance(statement, CompoundStatement) or isinstance(statement, AssignmentStatement) or statement == EMPTY, "statement invariant violated"
        self.statement = statement
    
    def invariant(self):
        return isinstance(self.statement, CompoundStatement) or isinstance(self.statement, AssignmentStatement) or self.statement == EMPTY
    
    def interpret(self, env):
        if self.statement == EMPTY:
            return True, env
        res, _ = self.statement.interpret(env)
        return res, env
    
    def to_string(self, tabs=0):
        string = ""
        for _ in range(tabs):
            string += tab
        
        string += "|-> " + type(self).__name__ + "\n" + self.statement.to_string(tabs + 1)
        return string
    
    def __str__(self):
        return "STATEMENT: " + self.statement.__str__()