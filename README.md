# Interpreter
A basic interpreter, loosely built following the guidelines specified in Ruslan Spivak's tutorial (https://ruslanspivak.com/lsbasi). 

Updates (as of Jul 24, 2025):
- Running the line "python main.py" boots up the UI
- Users can enter in mathematical expressions with the following supported operations: **+, \*, -, /, (), ^**
- The project contains a tokenizer and lexer (which break down the expression into recognizable symbols), a parser (which builds an abstract syntax tree to organize the expression), and an interpreter (which traverses the tree to evaluate the expression)
- Tree rotations ensure that the resulting AST is balanced, allowing for efficient traversal
  
