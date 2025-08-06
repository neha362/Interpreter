from abc import ABC, abstractmethod
from interpreter import *
from tokens import *
from lexer import *

tab = "  "

#class AST_Node holds the abstract interpret() function, which evaluates the node
class AST_Node():
    @abstractmethod
    def invariant(self):
        pass

    @abstractmethod
    def interpret(self, env={}):
        pass
    
    def to_string(self, tabs=0):
        print (type(self).__name__)
    
    def __str__(self):
        return self.to_string()
    
    def print_env(env):
        return str([str(i) + ": " + str(env[i]) for i in env])