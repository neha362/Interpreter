 #tokens
INTEGER, MULOP, ADDOP, EOF, SPACE, OPAREN, PERIOD, CPAREN, CARET, DOT, ASSIGNEQ, SEMICOLON, CHAR, COMMA, COLON, QUOTE, FUNCTION = "INTEGER", "MULOP", "ADDOP", "EOF", "SPACE", "OPAREN", "PERIOD", "CPAREN", "CARET", "DOT", "ASSIGNEQ", "SEMICOLON", "CHAR", "COMMA", "COLON", "QUOTE", "FUNCTION"

#keywords
PROGRAM, VAR, BEGIN, END, INTEGER, REAL, DIV, CHAR = "PROGRAM","VAR", "BEGIN", "END", "INTEGER", "REAL", "DIV", "CHAR"

keywords = {PROGRAM, VAR, BEGIN, END, INTEGER, REAL, DIV, CHAR }

'''class Token represents a token and contains its __str__ function. There are seven types of tokens that are recognized by the program: single-digit integers, mulops (* or /), addops (+ or -), periods, spaces, oparens ("("), cparens(")"), and the end of file.'''
class Token:

    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol
    
    def __str__(self):
        return "" + self.name + ", " + str(self.symbol)