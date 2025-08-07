from tokens import *
from as_tree import *
from as_tree.program import *
from as_tree.function import *
from as_tree.number import *
from as_tree.string import *
from as_tree.assignmentStatement import *
from lexer import *

class Parser:
    def __init__(self, expr):
        self.lexer = Lexer(expr)
        self.tree = None
    
    #begins the interpretation process and returns the evaluated value, if the expression is valid
    def build(self):
        self.tree = self.build_program()
        assert(self.lexer.token.name == EOF), "additional characters after expression " + self.lexer.token
    
    #builds a variable
    def build_variable(self):
        name = ""
        if self.lexer.token.name == QUOTE:
            self.lexer.eat(QUOTE)
            name = ""
            while self.lexer.token.name != QUOTE:
                name += self.lexer.token.symbol
                self.lexer.next_token(False)
            self.lexer.eat(QUOTE)
            return String(name)
        while self.lexer.token.name in (CHAR, INTEGER):
            assert str.isalnum(str(self.lexer.token.symbol)) or self.lexer.token.symbol in ("-", "_"), "expected valid variable characters but found " + self.lexer.token.symbol
            name += str(self.lexer.token.symbol)
            self.lexer.next_token(skip_spaces=False)
        if self.lexer.token.name == SPACE:
            self.lexer.next_token()
        assert not name in keywords, "variable " + name + " is a keyword"
        return Variable(name)


    # builds a factor node
    # factor := (expr) | number (^ factor) | variable*
    def build_factor(self):
        node1 = None
        if self.lexer.token.name == OPAREN:
            self.lexer.eat(OPAREN)
            node1 = self.build_expr()
            self.lexer.eat(CPAREN)
        elif self.lexer.token.name in (CHAR, QUOTE):
            node1 = self.build_variable()
        elif self.lexer.token.name == ADDOP:
            sign = self.lexer.token
            self.lexer.eat(ADDOP)
            node1 = self.build_factor()
            node1.neg = ((node1.neg) if sign.symbol == "+" else (not node1.neg))
        elif self.lexer.token.name in (INTEGER, PERIOD):
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
        assert self.lexer.token.name in (INTEGER, PERIOD, ADDOP), "number identified but incorrect token " + self.lexer.token
        if self.lexer.token.name == ADDOP:
            assert self.lexer.token.symbol == "-", "expected negative value but plus found instead"
            neg = True
            self.lexer.eat(ADDOP)
            x = self.build_factor()
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
    # MULOP := * | / | DIV
    def build_term(self):
        assert self.lexer.token.name in (EOF, CHAR, INTEGER, OPAREN, PERIOD, ADDOP), "building term but token unexpected " + self.lexer.token
        node = self.build_factor()
        while self.lexer.token.name in (MULOP, OPAREN, DIV) :
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
        node = self.build_term()
        while(self.lexer.token.name == ADDOP):
            assert(self.lexer.token.name in (ADDOP, CPAREN, MULOP, CARET, OPAREN, DIV)), "tried to build expr but token unexpected " + self.lexer.token
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
    
    #builds a declaration
    def build_declaration(self):
        variable = [self.build_variable()]
        while self.lexer.token.name == COMMA:
            self.lexer.eat(COMMA)
            variable.append(self.build_variable())
        self.lexer.eat(COLON)
        assert self.lexer.token.name in (INTEGER, REAL, CHAR)
        var_type = self.lexer.token.name
        self.lexer.eat(var_type)
        return Declaration(variable, var_type)

    #builds a declaration list
    def build_declaration_list(self):
        self.lexer.eat("VAR")
        decs = [self.build_declaration()]
        while self.lexer.token.name == SEMICOLON:
            self.lexer.eat(SEMICOLON)
            if self.lexer.token.name == BEGIN:
                break
            decs.append(self.build_declaration())
        return DeclarationList(decs)

    #builds a program (a compound statement bookended by "BEGIN" and "END")
    def build_program(self):
        if self.lexer.pos == -1:
            self.lexer.next_token()
        assert(self.lexer.token.name == "PROGRAM"), "expected PROGRAM but actual token is " + str(self.lexer.token)
        self.lexer.eat("PROGRAM")
        name = self.build_variable()
        self.lexer.eat(SEMICOLON)
        if self.lexer.token.name == EOF:
            return Program(EMPTY, {})
        decs = self.build_declaration_list()
        statements = self.build_statementList()
        self.lexer.eat(PERIOD)
        return Program(name, decs, statements)
    
    #builds a compound statement (multiple statements with beginning and end)
    def build_compoundStatement(self):
        self.lexer.eat(BEGIN)
        node = self.build_statementList()
        self.lexer.eat(END)
        return CompoundStatement(node)
    
    #builds a list of statements (can be only one element too)
    def build_statementList(self):
        nodes = [self.build_statement()]
        while self.lexer.token.name == SEMICOLON:
            self.lexer.eat(SEMICOLON)
            node = self.build_statement()
            nodes.append(node)
        return StatementList(nodes)
    
    #builds a statement 
    def build_statement(self):
        if self.lexer.token.name == BEGIN:
            return Statement(self.build_compoundStatement())
        elif self.lexer.token.name in (PERIOD, END, SEMICOLON):
            return Statement(EMPTY)
        variable = self.build_variable()
        if self.lexer.token.name == ASSIGNEQ:
            self.lexer.eat(ASSIGNEQ)
            return AssignmentStatement(variable, self.build_expr())
        assert self.lexer.token.name == OPAREN, "expected function but wrong token found " + str(self.lexer.token)
        self.lexer.eat(OPAREN)
        args = [self.build_factor()]
        while self.lexer.token.name == COMMA:
            self.lexer.eat(COMMA)
            args.append(self.build_factor())
        self.lexer.eat(CPAREN)
        return Function(variable, args)
    
    #builds an assignment statement (variable := value)
    def build_assignmentStatement(self):
        variable = self.build_variable()
        self.lexer.eat(ASSIGNEQ)
        return AssignmentStatement(variable, self.build_expr())
    

    

        
        
