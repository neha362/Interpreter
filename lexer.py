from tokens import *
from interpreter import *

class Lexer:
    #allows for the initialization of the variables that track the parser's position in the inputted expression
    def __init__(self, expr):
        self.expr = expr
        self.pos = -1
        self.token = None

    # consumes white space while the next token is a whitespace character (SPACE)
    def eat_spaces(self):
        while (self.token.name == SPACE):
            self.eat(SPACE)

    #advances the parser to the next token in the expression and returns the next token, if valid
    #throws exception if next token is not recognized
    def next_token(self):
        self.pos += 1
        if self.pos >= len(self.expr):
            self.token = Token(EOF, None)
            return Token(EOF, None)
        curr_char = self.expr[self.pos]
        if curr_char.isnumeric():
            self.token = Token(INTEGER, int(curr_char))
        else: 
            match curr_char:
                case " ":
                    self.token = self.next_token()
                case "(":
                    self.token = Token(OPAREN, "(")
                case ")":
                    self.token = Token(CPAREN, ")")
                case "+":
                    self.token = Token(ADDOP, "+")
                case "-":
                    self.token = Token(ADDOP, "-")
                case "*":
                    self.token = Token(MULOP, "*")
                case "/":
                    self.token = Token(MULOP, "/")
                case _:
                    raise Exception("illegal symbol encountered:", curr_char)
        print(self.token)
        return self.token