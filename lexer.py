from tokens import *
from interpreter import *

class Lexer:
    #allows for the initialization of the variables that track the parser's position in the inputted expression
    def __init__(self, expr):
        self.expr = expr
        self.pos = -1
        self.token = None

    #checks if the next token is the expected type, then consumes that token
    def eat(self, token):
        assert self.token.name == token, "incorrect token specified to eat"
        self.next_token()

    #advances the parser to the next token in the expression and returns the next token, if valid
    #throws exception if next token is not recognized
    def next_token(self, skip_spaces=True):
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
                    self.token = Token(SPACE, " ") if not skip_spaces else self.next_token()
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
                case ".":
                    self.token = Token(PERIOD, ".")
                case "^":
                    self.token = Token(CARET, "^")
                case _:
                    raise Exception("illegal symbol encountered:", curr_char)
        return self.token