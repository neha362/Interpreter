from interpreter import *
import sys

#begins the flow of the program, allowing users to add interpretable expressions
while True:
    expr = input("expression: ")
    if expr == "quit":
        sys.exit()
    interpreter = Interpreter(expr)
    print(interpreter.input() + " = " + str(interpreter.interpret()))