from interpreter import *
import sys

#begins the flow of the program, allowing users to add interpretable expressions
while True:
    try:
        # expr = input("expression: ")
        # if expr == "quit":
        #     sys.exit()
        expr = "BEGIN BEGIN number := 2; a := number; b := 10 * a + 10 * number / 4; c := a - - b END; x := 11;END."
        interpreter = Interpreter(expr)
        print(interpreter.input() + " = " + str(interpreter.interpret()))
    except Exception as e:
        print(e)
        print("there was an error in your expression. please try entering a different value!")
    finally:
        break