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
        assert self.token.name == token, "incorrect token specified to eat, expected " + token + " but got " + self.token.name
        self.next_token()

    #advances the parser to the next token in the expression and returns the next token, if valid
    #throws exception if next token is not recognized
    def next_token(self, skip_spaces=True):
        self.pos += 1
        if self.pos >= len(self.expr):
            self.token = Token(EOF, None)
            return Token(EOF, None)
        curr_char = self.expr[self.pos]
        
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
            case ".":
                self.token = Token(DOT, ".")
            case "B":
                if self.pos <= len(self.expr) - 5 and self.expr[self.pos:self.pos + 5] == "BEGIN":
                    self.token = Token(BEGIN, "BEGIN")
                    self.pos += 4
            case "E":
                if self.pos <= len(self.expr) - 3 and self.expr[self.pos:self.pos + 3] == "END":
                    self.token = Token(END, "END")
                    self.pos += 2
            case ":":
                if not self.pos == len(self.expr) - 1 and self.expr[self.pos + 1] == "=":
                    self.token = Token(ASSIGNEQ, ":=")
                    self.pos += 1
            case ";":
                self.token = Token(SEMICOLON, ";")
            case _:
                if curr_char.isnumeric():
                    self.token = Token(INTEGER, int(curr_char))
                elif curr_char.isalnum():
                    self.token = Token(CHAR, curr_char)
                else:
                    raise Exception("illegal symbol encountered:", curr_char)
        if self.token == None:
            raise Exception("token not recognized")
        return self.token