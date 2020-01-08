import sys
from os import path
sys.path.append(path.join(path.dirname(__file__), '..'))
from lalrparse import Parser
from analysis import calls
##
## 这里的语句中我们使用分号作为语句分隔符，相对于不适用语句分隔符，速度差10秒，前者10s，后者需要20s。
productions = [
    ['Stmts','Stmts','Stmt'],
    ['Stmts'],
    ['Stmts','Stmt'],
    ['Stmt','id','=','E',';'],
    ['Stmt','if','(','E',')','Stmt'],
    ['Stmt','if','(','E',')','Stmt','else','Stmt'],
    ['Stmt','while','(','E',')','Stmt'],
    ['Stmt','{','Stmts','}'],
    ['E','E','+','E'],
    ['E','E','-','E'],
    ['E','E','*','E'],
    ['E','E','/','E'],
    ['E','E','==','E'],
    ['E','E','!=','E'],
    ['E','E','>','E'],
    ['E','E','>=','E'],
    ['E','E','<=','E'],
    ['E','E','<','E'],
    ['E','E','||','E'],
    ['E','E','&&','E'],
    ['E','!','E'],
    ['E','-','E'],
    ['E','+','E'],
    ['E','(','E',')'],
    ['E','num'],
    ['E','id']
]

# terminal = ['=','{','}','(',')',';']
terminal = ['while','else','=','{','}','(',')','+','-','*','/','UMINUS','POSITIVE','>','>=','<','<=','!=','==','||','!','&&','id','num',';']
nonterminal = ['Stmts','Stmt','E']
precedence = {# 优先级 
    '||':7,
    '&&':7,
    '!':8,
    '>=':9,
    '>':9,
    '<':9,
    '<=':9,
    '==':9,
    '!=':9,
    '+':10,
    '-':10,
    '*':11,
    '/':11,
    'UMINUS':15,
    'POSITIVE':15
}

assosiation = {# 结合律
    # '+':'L',
    # '-':'L',
    # '*':'L',
    # '/':'L',
    # 'UMINUS':'R'
}
precs = {
    'UMINUS':['E','-','E'],
    'POSITIVE':['E','+','E']
}
parser = Parser(productions, terminal, nonterminal, precs, precedence, assosiation)
parser.generate()
print(calls)