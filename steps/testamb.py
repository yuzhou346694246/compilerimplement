## 测试二义性文法生成速度
# - (1)
# E-> E + T
# E-> E - T
# T-> T * F
# T-> T / F
# F-> num
# - (2)
# E-> E + E
# E-> E - E
# E-> E * E
# E-> E / E
# E-> num
import sys
from os import path
sys.path.append(path.join(path.dirname(__file__), '..'))
from lalrparse import Parser
from analysis import calls
productions = [
    ['E','E','+','E'],
    ['E','E','-','E'],
    ['E','E','*','E'],
    ['E','E','/','E'],
    ['E','num'],
    ['E','id']
]
terminal = ['+','-','*','/','id','num']
nonterminal = ['E']

precedence = {# 优先级 
    '+':10,
    '-':10,
    '*':11,
    '/':11
}


assosiation = {# 结合律
    # '+':'L',
    # '-':'L',
    # '*':'L',
    # '/':'L',
    # 'UMINUS':'R'
}


# productions = [
#     ['E','E','+','T'],
#     ['E','E','-','T'],
#     ['E','T'],
#     ['T','T','*','F'],
#     ['T','T','/','F'],
#     ['T','F'],
#     ['F','num'],
#     ['F','id']
# ]
# terminal = ['+','-','*','/','id','num']
# nonterminal = ['E','T','F']
precs = {
    # 'UMINUS':['E','-','E'],
    # 'POSITIVE':['E','+','E']
}

parser = Parser(productions, terminal, nonterminal, precs, precedence, assosiation)
parser.generate()#printInfo=True)
parser.htmlparse()
print(calls)
tokens = ['id','+','id','*','id']
parser.parse(tokens)