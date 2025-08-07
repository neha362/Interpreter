from as_tree.factor import Factor
from tokens import *
from as_tree.string import String

#class Variable contains the relevant functions for variables
class Variable(Factor):
    def __init__(self, id):
        assert isinstance(id, str), "variable name not a string"
        self.id = id
        self.neg = False

    def invariant(self):
        return isinstance(self.id, str)
    
    def interpret(self, env={}):
        if isinstance(self, String):
            return self.value
        if self.id in env:
            value, valtype = env[self.id]
            check_val_type(value, valtype)
            if valtype in (INTEGER, REAL):
                return value * (-1 if self.neg else 1)
            return value
        raise Exception("variable not defined: " + self.id)
    
    def to_string(self, tabs=0):
        string = ""
        for _ in range(tabs):
            string += self.tab
        string += "|-> Variable\n"
        for _ in range(tabs + 1):
            string += self.tab
        string += "|-> ID: " + self.id + "\n"
        return string
    
    def __str__(self):
        return ("-" if self.neg else "") + self.id
    
def check_val_type(value, val_type):
        match val_type:
            case "INTEGER":
                return int(value), INTEGER
            case "REAL":
                return float(value), REAL
            case "CHAR":
                return chr(value), CHAR
            case "FUNCTION":
                return value, FUNCTION
            case _:
                raise Exception("unknown type found", val_type)