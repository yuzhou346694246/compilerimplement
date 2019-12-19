import sys
from os import path
sys.path.append(path.join(path.dirname(__file__), '..'))
from lalrparse import Parser
from analysis import calls
# 使用二义性这种语法，造成分析生成器非常慢
# 这里要查找原因
# 在下面的例子中
productions = [
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

terminal = ['+','-','*','/','UMINUS','POSITIVE','>','>=','<','<=','!=','==','||','!','&&','id','num']
nonterminal = ['E']

parser = Parser(productions, terminal, nonterminal, precs, precedence, assosiation)
# parser.generate(printInfo=True)
parser.generate()
parser.dumpjson('lrtables.json')
parser.htmlparse()
print(calls)
# tokens = ['-','id','+','id','*','id']
# parser.parse(tokens)