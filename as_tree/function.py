from variable import *
from factor import *

# the function class stores functions relevant to building functions within the program
class Function:
    def __init__(self, func_name, args):
        self.func_name = func_name
        self.args = args

    def invariant(self):
        if not (isinstance(self.func_name, Variable) and isinstance(self.args, list)):
            return False
        for i in self.args:
            if not isinstance(i, Factor):
                return False
        return True
    
    def interpret(self, env):
        if self.func_name in env:
            assert isinstance(env[self.func_name], function), "variable is not a function"
            return env[self.func_name](self.args)
        raise Exception("function name not found")
            