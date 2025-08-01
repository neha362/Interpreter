from statement import *

# class StatementList stores appropriate function for statement lists
class StatementList(AST_Node):
        def __init__(self, statements):
            self.statements = statements
            self.env = None
        
        def invariant(self):
            for i in self.statements:
                if not isinstance(i, Statement):
                    return False
            return True
        
        def interpret(self, env):
            ret = []
            for i in self.statements:
                res, env = i.interpret(env)
                ret.append(res)
            self.env = env
            return ret, env
        
        def to_string(self, tabs=0):
            string = ""
            for _ in range(tabs):
                string += tab
            string += "|-> " + type(self).__name__ + " " + (str(self.env) if self.env != None else "")
            for i in self.statements:
                string += "\n" + i.to_string(tabs + 1)
            return string

        def __str__(self):
            string = "STATEMENT LIST " + (str(self.env) if self.env != None else "") + "\n"
            for i in self.statements:
                string +=  tab + i.__str__() + "\n"
            return string