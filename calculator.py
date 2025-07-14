#tokens: 
INTEGER, MULOP, ADDOP, EOF, SPACE, OPAREN, CPAREN = "INTEGER", "MULOP", "ADDOP", "EOF", "SPACE", "OPAREN", "CPAREN"
'''

expr := factor | (expr) | expr mulop expr | expr addop expr
mulop := * | /
addop := + | -
factor := integer
''' 

'''class Token represents a token and contains its __str__ function. There are seven types of tokens that are recognized by the program: single-digit integers, mulops (* or /), addops (+ or -), spaces, oparens ("("), cparens(")"), and the end of file.'''
class Token:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol
    
    def __str__(self):
        return "" + self.name + ", " + str(self.symbol)
    
'''class Interpreter parses an expression and evaluates the sentence based on the BNF form of the expression. '''
class Interpreter:
    #allows for the initialization of the variables that track the parser's position in the inputted expression
    def __init__(self, expr):
        self.expr = expr
        self.pos = -1
        self.token = None
    
    #begins the interpretation process and returns the evaluated value, if the expression is valid
    def interpret(self):
        return self.eval_expr()

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
    
    # checks whether the next token is the same type as the expected token and advances the parser to the next token
    def eat(self, token):
        assert self.token.name == token
        self.next_token()
    
    # evaluates the rule for a factor
    # factor := INTEGER
    def eval_factor(self):
        assert self.token.name == INTEGER
        num = 0
        while (self.token.name == INTEGER):
            num = 10 * num + self.token.symbol
            self.next_token()
        return num

    # consumes white space while the next token is a whitespace character (SPACE)
    def eat_spaces(self):
        while (self.token.name == SPACE):
            self.eat(SPACE)
    
    # evaluates the rule for mulops
    # mulop := * | /
    def eval_mulop(self, num1):
        assert self.token.name == MULOP
        match self.token.symbol:
            case "*":
                self.next_token()
                num1 = num1 * self.eval_factor()
            case "/":
                self.next_token()
                num1 = num1 // self.eval_factor()
            case _:
                raise Exception("illegal mulop argument")
        return num1
    
    # evaluates the rule for addops
    # addop := + | -
    def eval_addop(self, num1):
        assert self.token.name == ADDOP
        match self.token.symbol:
            case "+":
                self.next_token()
                num1 = num1 + self.eval_factor()
            case "-":
                self.next_token()
                num1 = num1 - self.eval_factor()
            case _:
                raise Exception("illegal addop argument")
        return num1
        
    # evaluates the rule for expressions
    # expr := factor | (expr) | expr mulop expr | expr addop expr
    def eval_expr(self):
        if self.pos == -1:
            self.next_token()
        token = self.token.name
        if token == OPAREN:
            self.eat(OPAREN)
            x = self.eval_expr()
            assert(self.token.name == CPAREN)
            self.eat(CPAREN)
            return x
        if token == SPACE:
            self.eat(token)
            return self.eval_expr()
        if token == INTEGER:
            num1 = self.eval_factor()
            if self.token.name == EOF:
                return num1
            assert(self.token.name == MULOP or self.token.name == ADDOP or self.token.name == CPAREN)
            while(self.token.name == MULOP or self.token.name == ADDOP):
                op = self.token
                match op.name:
                    case "ADDOP":
                        num1 = self.eval_addop(num1)
                    case "MULOP":
                        num1 = self.eval_mulop(num1)
                    case _:
                        raise Exception("illegal operation passed")
            return num1
        return 0

#begins the flow of the program, allowing users to add interpretable expressions
while True:
    print(Interpreter(input("expression: ")).interpret())