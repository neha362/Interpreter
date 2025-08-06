from as_tree.term import *
from as_tree.binop import *
from as_tree.expr import *

# class Factor extends the Term Node and implements the interpret method according to the BNF
class Factor(Term):
    def __init__(self, left, right, op):
        if op.name != CARET:
            raise Exception("illegal factor node")
        Binop.__init__(self, left, right, op)

    # the right term must either be None or the operation must be exponential and the left node must be a number
    def invariant(self):
        if self.right == None:
            return isinstance(self.left, Expr) or self.op == None
        return self.op.name == CARET and isinstance(self.left, Number) and isinstance(self.right, Factor)
    
    #interprets the node according to the BNF rule for factor (factor := (expr) | number (^ factor)*)
    def interpret(self, env):
        if self.op == None:
            return self.left.interpret(env)
        return self.left.interpret(env) ** self.right.interpret(env)
    
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
    