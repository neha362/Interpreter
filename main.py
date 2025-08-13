from interpreter import *
import sys
from parser import *


def expr_eval(): 
#begins the flow of the program, allowing users to add interpretable expressions
    while True:
        try:
            expr = input("expression: ")
            if expr == "quit":
                sys.exit()
            expr = Parser(expr).build_expr()
            print(expr.to_string() + " = " + expr.interpret({}))
        except Exception as e:
            print(e)
            print("there was an error in your expression. please try entering a different value!")
        finally:
            break

def string_eval():
    #evaluates a pre-set string
    expr = "BEGIN begin number := 2; a := number; b := 10 * a + 10 * number / 4; c := a - - b END; x := 11;END."
    interpreter = Interpreter(expr)
    print(interpreter.input() + " = " + str(interpreter.interpret()))
    print(interpreter.input())

def file_eval(file):
    try:
        my_file = open(file)
        interpreter = Interpreter(my_file.read())
        x = str(interpreter.interpret())
    # except Exception as e:
    #     print(e)
    finally:
        my_file.close()

file_eval("part10.txt")
file_eval("newfile.txt")