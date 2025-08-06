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
        assert self.token.name == token, "incorrect token specified to eat, expected " + token + " but got " + self.token.__str__()
        self.next_token()

    #advances the parser to the next token in the expression and returns the next token, if valid
    #throws exception if next token is not recognized
    def next_token(self, skip_spaces=True):
        self.pos += 1
        if self.pos >= len(self.expr):
            self.token = Token(EOF, None)
            return Token(EOF, None)
        curr_char = self.expr[self.pos]
        match curr_char.lower():
            case " ":
                if skip_spaces:
                    return self.next_token()
                else:
                    self.token = Token(SPACE, " ")
            case "\n":
                self.token = Token(SPACE, " ") if not skip_spaces else self.next_token()
            case "\t":
                self.token = Token(SPACE, " ") if not skip_spaces else self.next_token()
            case "{":
                while self.pos < len(self.expr):
                    self.pos += 1
                    if self.expr[self.pos] == "}":
                        return self.next_token()
                if self.pos == len(self.expr):
                    raise Exception("unclosed comment")
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
            case ":":
                if not self.pos == len(self.expr) - 1 and self.expr[self.pos + 1] == "=":
                    self.token = Token(ASSIGNEQ, ":=")
                    self.pos += 1
                else:
                    self.token = Token(COLON, ":")
            case ";":
                self.token = Token(SEMICOLON, ";")
            case ",":
                self.token = Token(COMMA, ",")
            case "'":
                self.token = Token(QUOTE, "'")
            case _:
                if curr_char.isnumeric():
                    self.token = Token(INTEGER, int(curr_char))
                else:
                    self.token = Token(CHAR, curr_char)
                    for keyword in keywords:
                        if self.pos <= len(self.expr) - len(keyword) and self.expr[self.pos:self.pos + len(keyword)].upper() == keyword:
                            self.token = Token(keyword, keyword)
                            self.pos += len(keyword) - 1
        if self.token == None:
            raise Exception("token not recognized")
        return self.token