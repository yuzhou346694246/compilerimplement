#simple pascal grammar

'''
Program: program variable; Block
Block:Declarations Compound_statement
Declararations:(Variable_declaration ;)+
                | empty
Variable_declaration: id (, id)* : Type_spec
Type_spec: integer | real
Term: factor([mul | div ] factor) *
Factor:
'''