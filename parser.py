from tokens import *
from as_tree import *
from lexer import *

class Parser:
    def __init__(self, expr):
        self.lexer = Lexer(expr)
        self.tree = None
    
    #begins the interpretation process and returns the evaluated value, if the expression is valid
    def build(self):
        self.tree = self.build_program()
        assert(self.lexer.token.name == EOF), "additional characters after expression " + self.lexer.token
    
    def build_variable(self):
        name = ""
        while self.lexer.token.name in (CHAR, INTEGER):
            name += self.lexer.token.symbol
            self.lexer.next_token(skip_spaces=False)
        return Variable(name)


    # builds a factor node
    # factor := (expr) | number (^ factor)*
    def build_factor(self):
        node1 = None
        if self.lexer.token.name == OPAREN:
            self.lexer.eat(OPAREN)
            node1 = self.build_expr()
            self.lexer.eat(CPAREN)
        elif self.lexer.token.name == CHAR:
            node1 = self.build_variable()
        elif self.lexer.token.name in (INTEGER, PERIOD, ADDOP):
            node1 = self.build_number()
        while self.lexer.token.name == CARET:
            op = self.lexer.token
            self.lexer.eat(CARET)
            node1 = Factor(node1, self.build_factor(), op)
        return node1

    # builds a number node
    # number := INTEGER* | INTEGER* PERIOD INTEGER
    def build_number(self):
        decimal, num, neg = False, [], False
        assert self.lexer.token.name in (INTEGER, PERIOD, ADDOP), "number identified but incorrect token " + self.lexer.token.name
        if self.lexer.token.name == ADDOP:
            assert self.lexer.token.symbol == "-", "expected negative value but plus found instead"
            neg = True
            self.lexer.eat(ADDOP)
            x = self.build_number()
            x.neg = not x.neg
            return x
        while self.lexer.token.name in (INTEGER, PERIOD):
            if self.lexer.token.name == PERIOD:
                if decimal:
                    raise Exception ("number with too many decimal places")
                decimal = True
            num.append(self.lexer.token)
            self.lexer.next_token(False)
        if self.lexer.token.name == SPACE:
            self.lexer.next_token()
        return Number(num, neg)
    
    # builds a term node
    # term := factor (MULOP factor)*
    # MULOP := * | /
    def build_term(self):
        assert self.lexer.token.name in (EOF, CHAR, INTEGER, OPAREN, PERIOD, ADDOP), "building term but token unexpected " + self.lexer.token.symbol
        node = self.build_factor()
        while self.lexer.token.name in (MULOP, OPAREN) :
            op = self.lexer.token
            self.lexer.eat(op.name)
            match op.symbol:
                #handles tree rotation to ensure balanced tree
                case "*":
                    if type(node) == Term and type(node.left) == Term and node.op.symbol == "*":
                        node = Term(node.left, Term(node.right, self.build_term(), op), op)
                    else:
                        node = Term(node, self.build_factor(), op)
                case "(":
                    op = Token(MULOP, "*")
                    if type(node) == Term and type(node.left) == Term and node.op.symbol == "*":
                        node = Term(node.left, Term(node.right, self.build_expr(), op), op)
                    else:
                        node = Term(node, self.build_expr(), op)
                    self.lexer.eat(CPAREN)
                case _:
                    node = Term(node, self.build_factor(), op)
        return node
    
    # evaluates the rule for expressions
    # expr := term (ADDOP term)*
    def build_expr(self):
        token = self.lexer.token.name
        node = self.build_term()
        while(self.lexer.token.name == ADDOP):
            assert(self.lexer.token.name in (ADDOP, CPAREN, MULOP, CARET, OPAREN)), "tried to build expr but token unexpected " + self.lexer.token
            op = self.lexer.token
            self.lexer.eat(ADDOP)
            match op.symbol:
                #performs tree rotation to ensure balanced tree
                case "+":
                    if type(node) == Expr and type(node.left) == Expr and node.op.symbol == "+":
                        node = Expr(node.left, Expr(node.right, self.build_term(), op), op)
                    else:
                        node = Expr(node, self.build_term(), op)
                case _:
                    node = Expr(node, self.build_term(), op)
        return node
    
    def build_program(self):
        if self.lexer.pos == -1:
            self.lexer.next_token()
            if self.lexer.token.name == EOF:
                return Program(EMPTY)
        node = self.build_compoundStatement()
        self.lexer.eat(DOT)
        return Program(node)
    
    def build_compoundStatement(self):
        self.lexer.eat(BEGIN)
        node = self.build_statementList()
        self.lexer.eat(END)
        return CompoundStatement(node)
    
    def build_statementList(self):
        nodes = [self.build_statement()]
        while self.lexer.token.name == SEMICOLON:
            self.lexer.eat(SEMICOLON)
            node = self.build_statement()
            print(node.to_string())
            nodes.append(node)
        return StatementList(nodes)
    
    def build_statement(self):
        if self.lexer.token.name == BEGIN:
            return Statement(self.build_compoundStatement())
        elif self.lexer.token.name in (DOT, END, SEMICOLON):
            return Statement(EMPTY)
        return Statement(self.build_assignmentStatement())

    def build_assignmentStatement(self):
        variable = self.build_variable()
        if self.lexer.token.name == SPACE:
            self.lexer.next_token()
        self.lexer.eat(ASSIGNEQ)
        return AssignmentStatement(variable, self.build_expr())
    

    

        
        
