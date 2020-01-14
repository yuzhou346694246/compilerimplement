from collections import namedtuple
from syntaxmap import SyntaxMap
from parse import Parser
from semantics import TypeCheck
from interpreter import Interperter
from collections import Counter
from os import path
import sys
sys.path.append(path.join(path.dirname(__file__), '..'))
from steps.lex import Lexer
from analysis import calls

productions = [
    ['Stmts','Stmts','Stmt'],
    ['Stmts'],
    ['Stmts','Stmt'],
    ['Stmt','id','=','E',';'],
    ['Stmt','if','(','E',')','Stmt'],
    ['Stmt','if','(','E',')','Stmt','else','Stmt'],
    ['Stmt','while','(','E',')','Stmt'],
    ['Stmt','{','Stmts','}'],
    ['Stmt','print','Exp',';'],
    ['Stmt','Type','id',';'],
    ['Type','int'],
    ['Type','id'],
    ['Stmt','record','id','{','Fields','}'],
    ['Fields','Fields',',','Field'],
    ['Fields','Field'],
    ['Fields'],
    ['Field','Type','id'],
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
    # ['E','+','E'],
    ['E','(','E',')'],
    ['E','num'],
    ['E','id']
]

# terminal = ['=','{','}','(',')',';']
terminal = ['while','if','int','print',',','else','=','{','}','(',')','+','-','*','/','UMINUS','POSITIVE','>','>=','<','<=','!=','==','||','!','&&','id','num',';']
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
parser.htmlparse('test.html')
# Parser.printitems(productions, printno=True)
# cnt = Counter([p[0] for p in productions])
parser.htmlparse('test.html')
print(cnt)
print(calls)
print(sorted(terminal))
print(len(terminal))