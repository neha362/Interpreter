from as_tree.variable import *
from as_tree.factor import *

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
        func = self.func_name.interpret(env)
        assert isinstance(func, function), "variable is not a function"
        return func(self.args)
    
    def to_string(self, tabs=0):
        string = ""
        for _ in range(tabs):
            string += tab
        string += "|-> Function\n"
        for _ in range(tabs + 1):
            string += tab
        string += "|-> Name: " + str(self.func_name) + "\n"
        for _ in range(tabs + 1):
            string += tab
        string += "|-> Inputs: " + str(self.args) + "\n"
        return string

    def __str__(self):
        return str(self.func_name) + " (" + str(self.args) + ")"