from interpreter import *
import sys

#begins the flow of the program, allowing users to add interpretable expressions
while True:
    try:
        expr = input("expression: ")
        if expr == "quit":
            sys.exit()
        interpreter = Interpreter(expr)
        print(interpreter.input() + " = " + str(interpreter.interpret()))
    except Exception as e:
        print("there was an error in your expression. please try entering a different value!")