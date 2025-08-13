from as_tree.compoundStatement import *

# class Statement stores appropriate functions for statements
class Statement(AST_Node):
    def __init__(self, statement):
        assert isinstance(statement, CompoundStatement) or isinstance(statement, AssignmentStatement) or statement == EMPTY, "statement invariant violated"
        self.statement = statement
    
    def invariant(self):
        return isinstance(self.statement, CompoundStatement) or isinstance(self.statement, AssignmentStatement) or self.statement == EMPTY
    
    def interpret(self, global_env):
        if self.statement == EMPTY:
            return True, global_env
        res, _ = self.statement.interpret(global_env)
        return res, global_env
    
    def to_string(self, tabs=0):
        string = ""
        string += self.statement.to_string(tabs)
        return string
    
    def __str__(self):
        return "STATEMENT: " + self.statement.__str__()