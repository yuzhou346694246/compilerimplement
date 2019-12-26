import sys
from os import path
sys.path.append(path.join(path.dirname(__file__), '..'))
from lalrparse import Parser

productions = [
    ['Function','function','id','(','Params',')','Stmts'],
    ['Params','Params',',','Param'],
    ['Params','Param'],
    ['Params'],
    ['Param','id'],
    ['Stmts','Stmts','Stmt'],
    ['Stmts','Stmt'],
    ['Stmt','id','=','Exp',';'],
    ['Stmt','IfStmt'],
    ['Stmt','WhileStmt'],
    ['WhileStmt','while','RE','Stmts'],
    ['IfStmt','if','RE','Stmts'],
    ['IfStmt','if','RE','Stmts','else','Stmts'],
    ['Exp','RE'],
    ['Exp','E'],
    ['RE','E','>','E'],
    ['E','E','+','T'],
    ['E','T'],
    ['T','T','*','F'],
    ['T','F'],
    ['F','(','E',')'],
    ['F','id'],
    ['F','number'],
    ['F','id','(','AParams',')'],
    ['AParams'],
    ['AParams','AParams',',','AParam'],
    ['AParams','AParam'],
    ['AParam','Exp'],

]
terminal = ['id','*','+','(',')','>',';','=','if','else','while','function','number',',']
nonterminal = ['Stmts','WhileStmt','Stmt','IfStmt','Exp','RE','E','T','F','Function','Param','Params']

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

parser = Parser(productions,  terminal, nonterminal,precs, precedence, assosiation)
parser.generate(printInfo=True)
parser.checkerror()
# tokens = ['id','=','id','>','id',';','id','=','id','>','id']
# tokens = ['if','(','id','>','id',')','id','=','id',';']
tokens = ['if','id','>','id','id','=','id',';','else','id','=','id',';']
# tokens= ['id','=','id',';']
tokens = ['while','id','>','id','id','=','id',';','if','id','>','id','id','=','id',';','else','id','=','id',';']
tokens = ['function','id','(',')','while','id','>','id','id','=','id',';','if','id','>','id','id','=','id',';','else','id','=','id',';']
parser.parse(tokens)
