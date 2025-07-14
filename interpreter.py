from tokens import *
from lexer import Lexer
'''
BNF: 
expr := factor | (expr) | expr mulop expr | expr addop expr
mulop := * | /
addop := + | -
factor := integer
''' 


    
'''class Interpreter parses an expression and evaluates the sentence based on the BNF form of the expression. '''
class Interpreter:

    def __init__(self, expr):
        self.lexer = Lexer(expr)

    
    #begins the interpretation process and returns the evaluated value, if the expression is valid
    def interpret(self):
        return self.eval_expr()
    
    # checks whether the next token is the same type as the expected token and advances the parser to the next token
    def eat(self, token):
        assert self.lexer.token.name == token
        self.lexer.next_token()
    
    # evaluates the rule for a factor
    # factor := INTEGER
    def eval_factor(self):
        assert self.lexer.token.name == INTEGER
        num = 0
        while (self.lexer.token.name == INTEGER):
            num = 10 * num + self.lexer.token.symbol
            self.lexer.next_token()
        return num
    
    # evaluates the rule for mulops
    # mulop := * | /
    def eval_mulop(self, num1):
        assert self.lexer.token.name == MULOP
        match self.lexer.token.symbol:
            case "*":
                self.lexer.next_token()
                num1 = num1 * self.eval_factor()
            case "/":
                self.lexer.next_token()
                num1 = num1 // self.eval_factor()
            case _:
                raise Exception("illegal mulop argument")
        return num1
    
    # evaluates the rule for addops
    # addop := + | -
    def eval_addop(self, num1):
        assert self.lexer.token.name == ADDOP
        match self.lexer.token.symbol:
            case "+":
                self.lexer.next_token()
                num1 = num1 + self.eval_factor()
            case "-":
                self.lexer.next_token()
                num1 = num1 - self.eval_factor()
            case _:
                raise Exception("illegal addop argument")
        return num1
        
    # evaluates the rule for expressions
    # expr := factor | (expr) | expr mulop expr | expr addop expr
    def eval_expr(self):
        if self.lexer.pos == -1:
            self.lexer.next_token()
        token = self.lexer.token.name
        if token == OPAREN:
            self.eat(OPAREN)
            x = self.eval_expr()
            assert(self.lexer.token.name == CPAREN)
            self.eat(CPAREN)
            return x
        if token == SPACE:
            self.eat(token)
            return self.eval_expr()
        if token == INTEGER:
            num1 = self.eval_factor()
            if self.lexer.token.name == EOF:
                return num1
            assert(self.lexer.token.name == MULOP or self.lexer.token.name == ADDOP or self.lexer.token.name == CPAREN)
            while(self.lexer.token.name == MULOP or self.lexer.token.name == ADDOP):
                op = self.lexer.token
                match op.name:
                    case "ADDOP":
                        num1 = self.eval_addop(num1)
                    case "MULOP":
                        num1 = self.eval_mulop(num1)
                    case _:
                        raise Exception("illegal operation passed")
            return num1
        return 0

