from functools import wraps
from parse import Parser
from lex import Lexer


productions = [
    ['E','E','+','T'],
    ['E','T'],
    ['T','T','*','F'],
    ['T','F'],
    ['F','(','E',')'],
    ['F','num']
]
terminal = ['*','+','(',')','num']
nonterminal = ['E','T','F']

# productions = [
#     ['E','E','+','T'],
#     ['E','T'],
#     ['T','num']
# ]
# terminal = ['+','num']
# nonterminal = ['E','T']


sdmap = []

def syntaxmap(grammar, params):
    def decorator(f):
        sdmap.append([grammar, params,f])
        @wraps(f)
        def wrapper(*args, **kwds):
            return f(*args, **kwds)
        return wrapper
    return decorator

@syntaxmap(['T','T','*','F'],[1,2,3])
@syntaxmap(['E','E','+','T'],[1,2,3])
def opexp(left,op,right):
    if op.kind == '+':
        return left+right
    if op.kind == '-':
        return left-right
    if op.kind == '*':
        return left*right
    if op.kind == '/':
        return left/right

@syntaxmap(['E','T'],[1])
@syntaxmap(['T','F'],[1])
def texp(val):
    return val

@syntaxmap(['F','(','E',')'],[2])
def lpexp(val):
    return val

@syntaxmap(['F','num'],[1])
def numexp(t):
    return t.val

tokens = list(Lexer('1+10*123').lex())
# for t in tokens:
#     print(t)

parser = Parser(productions, terminal, nonterminal)
parser.generate(printInfo=True)
parser.parse(tokens, sdmap)

# print(sdmap)