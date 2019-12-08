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

productions = [
    ['E','E','+','E'],
    ['E','E','*','E'],
    ['E','id']
]

terminal = ['+','id','*']
nonterminal = ['E']

precedence = {
    '+':10,
    '*':11
}
#precedence = {# 优先级 
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
#}

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

parser = Parser(productions, terminal, nonterminal, precs, precedence, assosiation)
parser.generate(printInfo=True)
tokens = ['id','+','id','*','id']
parser.parse(tokens)