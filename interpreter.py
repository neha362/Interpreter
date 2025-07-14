from tokens import *
from lexer import Lexer
'''
BNF: 
expr := (expr) | term (ADDOP expr)*
term := factor | (expr) | factor (MULOP term)*
mulop := * | /
addop := + | -
factor := number | (expr) | number (^ factor)*
number := INTEGER* | INTEGER* PERIOD INTEGER
''' 

'''class Interpreter parses an expression and evaluates the sentence based on the BNF form of the expression. '''
class Interpreter:

    def __init__(self, expr):
        self.lexer = Lexer(expr)
    
    #begins the interpretation process and returns the evaluated value, if the expression is valid
    def interpret(self):
        return self.eval_expr()
    
    # checks whether the next token is the same type as the expected token and advances the parser to the next token
    
    # evaluates the rule for a factor
    # factor := number | (expr) | number (^ factor)*
    def eval_factor(self):
        num1 = 0
        if self.lexer.token.name == OPAREN:
            self.lexer.eat(OPAREN)
            num1 = self.eval_expr()
            self.lexer.eat(CPAREN)
            print("token:", self.lexer.token)
        elif self.lexer.token.name in (INTEGER, PERIOD):
            num1 = self.eval_number()
        while self.lexer.token.name == CARET:
            self.lexer.eat(CARET)
            num1 = num1 ** self.eval_factor()
        print("eval factor", num1)
        return num1

    # evaluates the rule for a number
    # number := INTEGER* | INTEGER* PERIOD INTEGER
    def eval_number(self):
        period, decimal, num = 0, False, 0
        assert self.lexer.token.name in (INTEGER, PERIOD)
        while self.lexer.token.name in (INTEGER, PERIOD):
            print(self.lexer.token)
            if self.lexer.token.name == PERIOD:
                if decimal:
                    raise Exception ("number with too many decimal places")
                decimal = True
                self.lexer.eat(PERIOD)
            if decimal:
                period += 1
            num = (10 if period == 0 else 1) * num + self.lexer.token.symbol / (10 ** period)
            self.lexer.next_token(False)
        if self.lexer.token.name == SPACE:
            self.lexer.next_token()
        print("eval number", num)
        return int(num) if period == 0 else num
    
    # evaluates the rule for terms
    # term := factor (MULOP term)*
    # MULOP := * | /
    def eval_term(self):
        assert self.lexer.token.name in (EOF, INTEGER, OPAREN, PERIOD) 
        num1 = self.eval_factor()
        while self.lexer.token.name == MULOP:
            op = self.lexer.token
            self.lexer.eat(MULOP)
            match op.symbol:
                case "*":
                    num1 = num1 * self.eval_term()
                case "/":
                    num1 = num1 / self.eval_term()
                case _:
                    raise Exception("illegal mulop argument")
        print("eval term", num1, self.lexer.token.name)
        return num1
    
    # evaluates the rule for expressions
    # expr := term (ADDOP term)*
    def eval_expr(self):
        if self.lexer.pos == -1:
            self.lexer.next_token()
        token = self.lexer.token.name
        num1 = self.eval_term()
        while(self.lexer.token.name == ADDOP):
            assert(self.lexer.token.name in (ADDOP, CPAREN, MULOP, CARET))
            op = self.lexer.token
            self.lexer.eat(ADDOP)
            match op.symbol:
                case "+":
                    num1 += self.eval_expr()
                case "-":
                    num1 -= self.eval_expr()
                case _:
                    raise Exception("illegal operation passed")
        print("eval expr", num1)
        return num1

