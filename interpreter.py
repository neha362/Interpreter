from tokens import *
from lexer import Lexer
from parser import *
from as_tree import *
'''
BNF: 
expr := term (ADDOP expr)*
term := factor (MULOP term)*
mulop := * | /
addop := + | -
factor := (expr) | number (^ factor)*
number :=  ADDOP? INTEGER* (PERIOD INTEGER*)?
''' 

'''class Interpreter parses an expression and evaluates the sentence based on the BNF form of the expression. '''
class Interpreter:
    # defines the parser and builds the AST
    def __init__(self, expr):
        self.parser = Parser(expr)
        self.parser.build()
    
    #takes the tree built by the parser and interpets it
    def interpret(self):
        print(self.parser.tree.to_string())
        return self.parser.tree.interpret()

    def input(self):
        return self.parser.tree.__str__()