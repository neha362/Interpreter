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

    @abstractmethod
    def invariant(self):
        pass

    @abstractmethod
    def interpret(self):
        pass
    
    # placeholder to_string function inherited by other tree nodes
    def to_string(self, tabs=0):
        string = ""
        for _ in range(tabs):
            string += "\t"
        string += "|-> " + type(self).__name__ + ", op = " + ("" if self.op == None else self.op.symbol)
        string += "\n" + self.left.to_string(tabs + 1)
        if self.right != None:
            string += "\n" + self.right.to_string(tabs + 1)
        return string
    
    # placeholder __str__ overriden from object class for child classes
    def __str__(self):
        return self.left.__str__() + " " + self.op.symbol + " " + self.right.__str__()

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

    #resolves hierarchy issues with negation
    def __str__(self):
        if type(self.right) == Expr and self.right.op.symbol == "-" and self.op.symbol == "-":
            return self.left.__str__() + " " + self.op.symbol + " (" + self.right.__str__() + ")"
        return AST_Node.__str__(self)
    

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

    # resolves hierarchy issues, prints parentheses if a higher order node is a child
    def __str__(self):
        ret = ""
        if type(self) == Term and type(self.left) == Expr:
            ret += "(" + self.left.__str__() + ")"
        else:
            ret += self.left.__str__()
        ret += " " + self.op.symbol + " "
        if type(self) == Term and type(self.right) == Expr:
            ret += "(" + self.right.__str__() + ")"
        else:
            ret += self.right.__str__()
        return ret

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
    
    #resolves hierarchy issues, prints parentheses if higher order node is child
    def __str__(self):
        ret = ""
        if type(self) == Factor and type(self.left) in (Expr, Term):
            ret += "(" + self.left.__str__() + ")"
        else:
            ret += self.left.__str__()
        ret += " " + self.op.symbol + " "
        if type(self) == Factor and type(self.right) in (Expr, Term):
            ret += "(" + self.right.__str__() + ")"
        else:
            ret += self.right.__str__()
        return ret
    
# class Number extends the Factor node and implements the interpret method according to the BNF rule (number := INTEGER* | INTEGER* PERIOD INTEGER)
class Number(Factor):
    def __init__(self, values, neg=False):
        self.values = values
        self.neg = neg
    
    # every emlement in the list, either ht e
    def invariant(self):
        for i in self.values:
            if not (i.name == INTEGER or i.name == PERIOD):
                return False
        return len([x for x in self.values if x.name == PERIOD]) <= 1

    # returns the decimal value of the number
    def interpret(self):
        if not self.invariant():
            raise Exception("illegal number node")
        return (-1 if self.neg else 1) * float("".join([str(i.symbol) for i in self.values]))

    # prints out the number, as represented by the array of symbols
    def to_string(self, tabs=0):
        string = ""
        for _ in range(tabs):
            string += "\t"
        return string + "|-> " + type(self).__name__ + ", " + ("-" if self.neg else "") + str([i.symbol for i in self.values])

    # prints out the number, as represented by the array of symbols
    def __str__(self):
        return ("-" if self.neg else "") + "".join([str(i.symbol) for i in self.values])