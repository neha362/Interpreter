from interpreter import *

#begins the flow of the program, allowing users to add interpretable expressions
while True:
    print(Interpreter(input("expression: ")).interpret())