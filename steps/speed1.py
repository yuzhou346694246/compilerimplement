import sys
from os import path
sys.path.append(path.join(path.dirname(__file__), '..'))
from lalrparse import Parser
from analysis import calls
# 使用二义性这种语法，造成分析生成器非常慢
# 这里要查找原因
productions = [
    ['Bool','Bool','||','Join'],
    ['Bool','Join'],
    ['Join','Join','&&','Equality'],
    ['Join','Equality'],
    ['Equality','Equality','==','Rel'],
    ['Equality','Equality','!=','Rel'],
    ['Equality','Rel'],
    ['Rel','Expr','<','Expr'],
    ['Rel','Expr','<=','Expr'],
    ['Rel','Expr','>','Expr'],
    ['Rel','Expr','>=','Expr'],
    ['Rel','Expr'],
    ['Expr','Expr','+','Term'],
    ['Expr','Expr','-','Term'],
    ['Expr','Term'],
    ['Term','Term','*','Unary'],
    ['Term','Term','/','Unary'],
    ['Term','Unary'],
    ['Unary','!','Unary'],
    ['Unary','-','Unary'],
    ['Unary','Factor'],
    ['Factor','(','Bool',')'],
    ['Factor','num'],
    ['Factor','id']
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
    # 'UMINUS':['E','-','E'],
    # 'POSITIVE':['E','+','E']
}

terminal = ['+','-','*','/','>','>=','<','<=','!=','==','||','!','&&','id','num']
nonterminal = ['Bool','Join','Equality','Rel','Expr','Term','Unary','Factor']

parser = Parser(productions, terminal, nonterminal, precs, precedence, assosiation)
# parser.generate(printInfo=True)
parser.generate()
parser.htmlparse('temp2.html')
parser.dumpjson('lrtables.json')
print(calls)
# tokens = ['-','id','+','id','*','id']
# parser.parse(tokens)