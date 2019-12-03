import sys
from os import path
sys.path.append(path.join(path.dirname(__file__), '..'))
from lalrparse import Parser

# productions = [
#     ['S','i','S','e','S'],
#     ['S','i','S'],
#     ['S','1']
# ]

# terminal = ['i','e','1']
# nonterminal = ['S']
productions = [
    ['Params','Params',',','Param'],
    ['Params','Param'],
    ['Param','id'],
    # ['Params']
]
terminal = ['id',',']
nonterminal = ['Params','Param']

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

parser = Parser(productions, terminal, nonterminal, precs, precedence, assosiation)
parser.generate(printInfo=True)
tokens = ['id',',','id']
parser.parse(tokens)