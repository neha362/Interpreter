from tokens import *
from lexer import Lexer
from parser import *


'''class Interpreter parses an expression and evaluates the sentence based on the BNF form of the expression. '''
class Interpreter:
    # defines the parser and builds the AST
    def __init__(self, expr):
        self.parser = Parser(expr)
        self.parser.build()
    
    #takes the tree built by the parser and interpets it
    def interpret(self):
        return self.parser.tree.interpret()

    def input(self):
        return self.parser.tree.__str__()