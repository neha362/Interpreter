from as_tree.binop import *

#class Expr extends the AST Node and implements the interpret method according to the BNF
class Expr(Binop):
    def __init__(self, left, right, op):
        if op.name != ADDOP:
            raise Exception("illegal add node")
        Binop.__init__(self, left, right, op)

    # the left child node must be an Expr and the right node -- if not None -- must also be an Expr
    def invariant(self):
        return (self.right == None or self.op.name == ADDOP)

    #interprets according to the Expr rule (expr := term (ADDOP expr)*)
    def interpret(self, env):
        if not self.invariant():
            raise Exception("illegal expr node")
        if self.op == None:
            return self.left.interpret(env)
        if self.op.symbol == "+":
            return self.left.interpret(env) + self.right.interpret(env)
        return self.left.interpret(env) - self.right.interpret(env)

    #resolves hierarchy issues with negation
    def __str__(self):
        if type(self.right) == Expr and self.right.op.symbol == "-" and self.op.symbol == "-":
            return self.left.__str__() + " " + self.op.symbol + " (" + self.right.__str__() + ")"
        return Binop.__str__(self)