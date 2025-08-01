from factor import *

#class Variable contains the relevant functions for variables
class Variable(Factor):
    def __init__(self, id):
        assert isinstance(id, str), "variable name not a string"
        self.id = id
        self.neg = False

    def invariant(self):
        return isinstance(self.id, str)
    
    def interpret(self, env):
        if self.id in env:
            return env[self.id] * (-1 if self.neg else 1)
        raise Exception("variable not defined: " + self.id)
    
    def to_string(self, tabs=0):
        string = ""
        for _ in range(tabs):
            string += tab
        string += "|-> Variable\n"
        for _ in range(tabs + 1):
            string += tab
        string += "|-> ID: " + self.id + "\n"
        return string
    
    def __str__(self):
        return ("-" if self.neg else "") + self.id