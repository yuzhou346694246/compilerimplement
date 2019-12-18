import sys
from os import path
sys.path.append(path.join(path.dirname(__file__), '..'))
from lalrparse import Parser
# 消除二义性的表达式文法
# productions = [
#     ['RE','E','>','E'],
#     ['E','E','+','T'],
#     ['E','T'],
#     ['T','T','*','F'],
#     ['T','F'],
#     ['F','(','E',')'],
#     ['F','id']
# ]
# terminal = ['id','*','+','(',')','>']
# nonterminal = ['RE','E','T','F']

# productions = [
#     ['E','E','+','E'],
#     ['E','E','*','E'],
#     ['E','id']
# ]

# terminal = ['+','id','*']
# nonterminal = ['E']

# precedence = {
#     '+':10,
#     '*':11
# }
# (0) Stmts->Stmts Stmt
# (1) Stmts->Stmt
# (2) Stmt->id = Exp
# (3) Stmt->if ( Exp ) Stmt else Stmt
# (4) Stmt->if ( Exp ) Stmt
# (5) Stmt->while ( Exp ) Stmt
# (6) Stmt->{ Stmts }
# (7) Stmt->Type id
# (8) Stmt->record id { Fields }
# (9) Fields->Fields , Field
# (10) Fields->Field
# (11) Fields->
# (12) Field->Type id
# (13) Type->bool
# (14) Type->int
# (15) Type->id
productions = [
    ['Stmts','Stmts','Stmt'],
    ['Stmts','Stmt'],
    ['Stmt','id','=','E'],
    ['Stmt','if','(','E',')','Stmt'],
    # ['Stmt','if','(','E',')','Stmt','else','Stmt'],
    # ['Stmt','while','(','E',')','Stmt'],
    # ['Stmt','{','Stmts','}'],
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
    ['E','num'],
    ['E','id']
]
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

terminal = ['=','+','-','*','/','UMINUS','POSITIVE','>','>=','<',\
        '<=','!=','==','||','!','&&','id','num',\
        'if','(',')','else',\
        'while','{','}'
        ]
nonterminal = ['E','Stmts','Stmt']

parser = Parser(productions, terminal, nonterminal, precs, precedence, assosiation)
parser.generate(printInfo=True)
parser.dumpjson('lrtables.json')
tokens = ['-','id','+','id','*','id']
parser.parse(tokens)