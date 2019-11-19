import sys
from os import path
sys.path.append(path.join(path.dirname(__file__), '..'))
from lalrparse import Parser

productions = [
    ['Stmts','Stmts','Stmt'],
    ['Stmts','Stmt'],
    ['Stmt','id','=','Exp',';'],
     # AttributeError: 'set' object has no attribute 'append'
    # ['Stmts','Stmt'],
    # ['Stmts'],
    # ['Stmt','id','=','Exp'],
    ['Stmt','IfStmt'],
    ['IfStmt','if','RE','Stmt'],
    ['IfStmt','if','RE','Stmt','else','Stmt'],
    # ['IfStmt','if','(','RE',')','Stmt'],
    ['Exp','RE'],
    ['Exp','E'],
    ['RE','E','>','E'],
    ['E','E','+','T'],
    ['E','T'],
    ['T','T','*','F'],
    ['T','F'],
    ['F','(','E',')'],
    ['F','id']
]
terminal = ['id','*','+','(',')','>',';','=','if','else']
nonterminal = ['Stmts','Stmt','IfStmt','Exp','RE','E','T','F']

precedence = {# 优先级 
    # '||':7,
    # '&&':7,
    # '!':8,
    # '>=':9,
    # '>':9,
    # '<':9,
    # '<=':9,
    # '==':9,
    # '!=':9,
    # '+':10,
    # '-':10,
    # '*':11,
    # '/':11,
    # 'UMINUS':15
}

assosiation = {# 结合律
    # '+':'L',
    # '-':'L',
    # '*':'L',
    # '/':'L',
    # 'UMINUS':'R'
}
precs = {
    # 'UMINUS':['E','-','E']
}

parser = Parser(productions, precs, terminal, nonterminal, precedence, assosiation)
parser.generate(printInfo=True)
# tokens = ['id','=','id','>','id',';','id','=','id','>','id']
# tokens = ['if','(','id','>','id',')','id','=','id',';']
# tokens = ['if','id','>','id','id','=','id','else','id','=','id',';']
tokens= ['id','=','id',';']
parser.parse(tokens)