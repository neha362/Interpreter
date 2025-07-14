from tokens import *
from lexer import Lexer
'''
BNF: 
expr := (expr) | term (ADDOP term)*
term := factor | (expr) | term (MULOP term)*
mulop := * | /
addop := + | -
factor := INTEGER
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
    # factor := INTEGER
    def eval_factor(self):
        assert self.lexer.token.name == INTEGER
        num = 0
        while (self.lexer.token.name == INTEGER):
            num = 10 * num + self.lexer.token.symbol
            self.lexer.next_token()
        return num
    
    # evaluates the rule for terms
    # term := factor | (expr) | term (MULOP term)*
    # MULOP := * | /
    def eval_term(self):
        if self.lexer.token.name == OPAREN:
            self.lexer.eat(OPAREN)
            x = self.eval_expr()
            self.lexer.eat(CPAREN)
            return x
        assert self.lexer.token.name == INTEGER or self.lexer.token.name == OPAREN
        num1 = self.eval_factor()
        while self.lexer.token.name == MULOP:
            op = self.lexer.token
            self.lexer.eat(MULOP)
            match op.symbol:
                case "*":
                    num1 = num1 * self.eval_term()
                case "/":
                    num1 = num1 // self.eval_term()
                case _:
                    raise Exception("illegal mulop argument")
        return num1
    
    # evaluates the rule for expressions
    # expr := (expr) | term (ADDOP term)*
    def eval_expr(self):
        if self.lexer.pos == -1:
            self.lexer.next_token()
        token = self.lexer.token.name
        if token == OPAREN:
            self.lexer.eat(OPAREN)
            x = self.eval_expr()
            self.lexer.eat(CPAREN)
            return x
        if token == INTEGER:
            num1 = self.eval_term()
            if self.lexer.token.name == EOF:
                return num1
            assert(self.lexer.token.name == ADDOP or self.lexer.token.name == CPAREN)
            while(self.lexer.token.name == ADDOP):
                op = self.lexer.token
                self.lexer.eat(ADDOP)
                match op.symbol:
                    case "+":
                        num1 += self.eval_term()
                    case "-":
                        num1 -= self.eval_term()
                    case _:
                        raise Exception("illegal operation passed")
            return num1
        return 0

