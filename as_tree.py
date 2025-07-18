from abc import ABC, abstractmethod
from interpreter import *
from tokens import *
from lexer import *

'''
BNF: 
expr := term (ADDOP expr)*
term := factor (MULOP term)*
mulop := * | /
addop := + | -
factor := (expr) | number (^ factor)*
number := INTEGER* | INTEGER* PERIOD INTEGER
''' 

#class AST_Node holds the abstract interpret() function, which evaluates the node
class AST_Node():
    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op

    def invariant(self):
        return not (self.left == None and self.right == None)

    @abstractmethod
    def interpret(self):
        pass

#class Expr extends the AST Node and implements the interpret method according to the BNF
class Expr(AST_Node):
    def __init__(self, left, right, op):
        if op.name != ADDOP:
            raise Exception("illegal add node")
        AST_Node.__init__(self, left, right, op)

    def invariant(self):
        return AST_Node.invariant(self) and isinstance(self.left, Expr) and isinstance(self.right, Expr) and self.op.name == ADDOP

    def interpret(self):
        if not self.invariant():
            raise Exception("illegal expr node")
        return self.left.interpret() ** self.right.interpret()

#class Term extends the Expr Node and implements the interpret method according to the BNF
class Term(Expr):
    def __init__(self, left, right, op):
        if op.name != MULOP:
            raise Exception("illegal term node")
        AST_Node.__init__(self, left, right, op)
    
    def invariant(self):
        return AST_Node.invariant(self) and isinstance(self.left, Term) and isinstance(self.right, Term) and self.op.name == MULOP
    
        
# class Factor extends the Term Node and implements the interpret method according to the BNF
class Factor(Term):
    def __init__(self, left, right, op):
        if op.name != CARET:
            raise Exception("illegal factor node")
        AST_Node.__init__(self, left, right, op)

    def invariant(self):
        if self.right == None:
            return isinstance(self.left, Expr)
        return self.left != None and self.op != None and isinstance(self.left, Term) and isinstance(self.right, Term)
    
# class Number extends the Factor node and implements the interpret method according to the BNF rule
class Number(Term):
    def __init__(self, left, right):
        if self.left == None or self.left:
            raise Exception("illegal number node")