from as_tree.expr import *

#class Term extends the Expr Node and implements the interpret method according to the BNF
class Term(Expr):
    def __init__(self, left, right, op):
        if right != None and op.name != MULOP and op.name != DIV or right == None and op != None:
            raise Exception("illegal term node")
        Binop.__init__(self, left, right, op)
    
    # the left node must be of type Term and the right node -- if not None -- must also be of type Term
    def invariant(self):
        return (self.right == None or self.op.name == MULOP or self.op.name == DIV)
    
    #interpets the node according to the BNF rule for terms (term := factor (MULOP term)*)
    def interpret(self, env):
        if not self.invariant():
            raise Exception("illegal term node")
        if self.op == None:
            return self.left.interpret(env)
        if self.op.symbol == "*":
            return self.left.interpret(env) * self.right.interpret(env)
        if self.op.symbol == DIV:
            return self.left.interpret(env) // self.right.interpret(env)
        return self.left.interpret(env) / self.right.interpret(env)

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