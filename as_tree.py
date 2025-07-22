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
        print(self.to_string(0))

    @abstractmethod
    def invariant(self):
        pass

    @abstractmethod
    def interpret(self):
        pass

    def to_string(self, tabs):
        string = ""
        for _ in range(tabs):
            string += "\t"
        string += "|-> " + type(self).__name__ + ", op = " + ("" if self.op == None else self.op.symbol)
        string += "\n" + self.left.to_string(tabs + 1)
        if self.right != None:
            string += "\n" + self.right.to_string(tabs + 1)
        return string


#class Expr extends the AST Node and implements the interpret method according to the BNF
class Expr(AST_Node):
    def __init__(self, left, right, op):
        if op.name != ADDOP:
            raise Exception("illegal add node")
        AST_Node.__init__(self, left, right, op)

    # the left child node must be an Expr and the right node -- if not None -- must also be an Expr
    def invariant(self):
        return (self.right == None or self.op.name == ADDOP)

    #interprets according to the Expr rule (expr := term (ADDOP expr)*)
    def interpret(self):
        if not self.invariant():
            raise Exception("illegal expr node")
        if self.op == None:
            return self.left.interpret()
        if self.op.symbol == "+":
            return self.left.interpret() + self.right.interpret()
        return self.left.interpret() - self.right.interpret()

#class Term extends the Expr Node and implements the interpret method according to the BNF
class Term(Expr):
    def __init__(self, left, right, op):
        if right != None and op.name != MULOP or right == None and op != None:
            raise Exception("illegal term node")
        AST_Node.__init__(self, left, right, op)
    
    # the left node must be of type Term and the right node -- if not None -- must also be of type Term
    def invariant(self):
        return (self.right == None or self.op.name == MULOP)
    
    #interpets the node according to the BNF rule for terms (term := factor (MULOP term)*)
    def interpret(self):
        if not self.invariant():
            raise Exception("illegal term node")
        if self.op == None:
            return self.left.interpret()
        if self.op.symbol == "*":
            return self.left.interpret() * self.right.interpret()
        return self.left.interpret() / self.right.interpret()

# class Factor extends the Term Node and implements the interpret method according to the BNF
class Factor(Expr):
    def __init__(self, left, right, op):
        if op.name != CARET:
            raise Exception("illegal factor node")
        AST_Node.__init__(self, left, right, op)

    # the right term must either be None or the operation must be exponential and the left node must be a number
    def invariant(self):
        if self.right == None:
            return isinstance(self.left, Expr) or self.op == None
        return self.op.name == CARET and isinstance(self.left, Number) and isinstance(self.right, Factor)
    
    #interprets the node according to the BNF rule for factor (factor := (expr) | number (^ factor)*)
    def interpret(self):
        if self.op == None:
            return self.left.interpret()
        return self.left.interpret() ** self.right.interpret()
    
# class Number extends the Factor node and implements the interpret method according to the BNF rule (number := INTEGER* | INTEGER* PERIOD INTEGER)
class Number(Factor):
    def __init__(self, values):
        self.values = values
    
    # every emlement in the list, either ht e
    def invariant(self):
        for i in self.values:
            if not i.name == INTEGER or i.name == PERIOD:
                return False
        return len([x for x in self.values if x.name == PERIOD]) <= 1

    def interpret(self):
        if not self.invariant():
            raise Exception("illegal number node")
        num, decimal = 0, False
        period = 0
        for i in self.values:
            if i.name == PERIOD:
                if decimal:
                    raise Exception("number with too many decimal places")
                decimal = True
                continue
            if i.name == INTEGER and decimal:
                period += 1
            num = (10 if period == 0 else 1) * num + i.symbol / (10 ** period)
        return num

    def to_string(self, tabs):
        string = ""
        for _ in range(tabs):
            string += "\t"
        return string + "|-> " + type(self).__name__ + ", " + str([i.symbol for i in self.values])