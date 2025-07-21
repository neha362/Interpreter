from tokens import *
from as_tree import *
'''
BNF: 
expr := term (ADDOP term)*
term := factor (MULOP factor)*
mulop := * | /
addop := + | -
factor := (expr) | number (^ factor)*
number := INTEGER* | INTEGER* PERIOD INTEGER
''' 
class Parser:
    def __init__(self, expr):
        self.lexer = Lexer(expr)
    
    #begins the interpretation process and returns the evaluated value, if the expression is valid
    def build(self):
        self.build_expr()
    # checks whether the next token is the same type as the expected token and advances the parser to the next token
    
    # builds a factor node
    # factor := (expr) | number (^ factor)*
    def build_factor(self):
        node1 = None
        if self.lexer.token.name == OPAREN:
            self.lexer.eat(OPAREN)
            node1 = self.build_expr()
            self.lexer.eat(CPAREN)
        elif self.lexer.token.name in (INTEGER, PERIOD):
            node1 = self.build_number()
        while self.lexer.token.name == CARET:
            self.lexer.eat(CARET)
            node1 = Factor(node1, self.build_factor(), CARET)
        return node1

    # builds a number node
    # number := INTEGER* | INTEGER* PERIOD INTEGER
    def build_number(self):
        decimal, num = False, []
        assert self.lexer.token.name in (INTEGER, PERIOD)
        while self.lexer.token.name in (INTEGER, PERIOD):
            if self.lexer.token.name == PERIOD:
                if decimal:
                    raise Exception ("number with too many decimal places")
                decimal = True
            num.append(self.lexer.token)
            self.lexer.next_token(False)
        if self.lexer.token.name == SPACE:
            self.lexer.next_token()
        return Number(num)
    
    # builds a term node
    # term := factor (MULOP factor)*
    # MULOP := * | /
    def build_term(self):
        assert self.lexer.token.name in (EOF, INTEGER, OPAREN, PERIOD) 
        node = self.build_factor()
        while self.lexer.token.name == MULOP:
            op = self.lexer.token
            self.lexer.eat(MULOP)
            match op.symbol:
                case "*":
                    node = Term(node, self.build_factor(), op)
                case _:
                    node = Term(self.build_factor(), node, op)
        return node
    
    # evaluates the rule for expressions
    # expr := term (ADDOP term)*
    def build_expr(self):
        if self.lexer.pos == -1:
            self.lexer.next_token()
        token = self.lexer.token.name
        node = self.build_term()
        while(self.lexer.token.name == ADDOP):
            assert(self.lexer.token.name in (ADDOP, CPAREN, MULOP, CARET))
            op = self.lexer.token
            self.lexer.eat(ADDOP)
            match op.symbol:
                case "+":
                    node = Expr(node, self.build_term(), op)
                case _:
                    node -= Expr(self.build_term(), node, op)
        return node

