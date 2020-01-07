from syntaxmap import SyntaxMap
from parse import Parser
from os import path
import sys
sys.path.append(path.join(path.dirname(__file__), '..'))

from analysis import calls
from lex import Lexer
# from analysis import calls
sm = SyntaxMap()

# @sm.syntaxmap(['T','T','*','F'],[1,2,3])
# @sm.syntaxmap(['E','E','+','T'],[1,2,3])
# def opexp(left,op,right):
#     if op.kind == '+':
#         return left+right
#     if op.kind == '-':
#         return left-right
#     if op.kind == '*':
#         return left*right
#     if op.kind == '/':
#         return left/right

# @sm.syntaxmap(['E','T'],[1])
# @sm.syntaxmap(['T','F'],[1])
# def texp(val):
#     return val

# @sm.syntaxmap(['F','(','E',')'],[2])
# def lpexp(val):
#     return val

# @sm.syntaxmap(['F','num'],[1])
# def numexp(t):# t is a token
#     return t.val
@sm.syntaxmap(['E','E','+','E'],[1,2,3])
@sm.syntaxmap(['E','E','-','E'],[1,2,3])
@sm.syntaxmap(['E','E','*','E'],[1,2,3])
@sm.syntaxmap(['E','E','/','E'],[1,2,3])
def simplefunc(left,op,right):
    if op.kind == '+':
        return left+ right
    if op.kind == '-':
        return left-right
    if op.kind == '*':
        return left*right
    if op.kind == '/':
        return left/right

@sm.syntaxmap(['E','E','||','E'],[1,2,3])
@sm.syntaxmap(['E','E','&&','E'],[1,2,3])
def logicfunc(left,op,right):
    if op.kind == '||':
        return left or right
    if op.kind == '&&':
        return left and right

@sm.syntaxmap(['E','E','>','E'],[1,2,3])
@sm.syntaxmap(['E','E','>=','E'],[1,2,3])
@sm.syntaxmap(['E','E','<=','E'],[1,2,3])
@sm.syntaxmap(['E','E','<','E'],[1,2,3])
@sm.syntaxmap(['E','E','==','E'],[1,2,3])
@sm.syntaxmap(['E','E','!=','E'],[1,2,3])
def comparefunc(left,op,right):
    if op.kind == '>':
        return left > right
    if op.kind == '>=':
        return left >= right
    if op.kind == '<':
        return left < right
    if op.kind == '<=':
        return left <= right
    if op.kind == '==':
        return left == right
    if op.kind == '!=':
        return left != right

@sm.syntaxmap(['E','num'],[1])
def numfunc(token):
    return token.val

precedence = {
    '||':5,
    '&&':5,
    '>':6,
    '>=':6,
    '<=':6,
    '<':6,
    '==':6,
    '!=':6,
    '+':7,
    '-':7,
    '*':8,
    '/':8
}
tokens = list(Lexer('1+10*123').lex())
# for t in tokens:
#     print(t)
# print(sm.productions())
# parser = Parser(productions, terminal, nonterminal)
parser = Parser(sm.productions, sm.terminal, sm.nonterminal, precedence=precedence)
parser.generate(printInfo=True)
parser.parse(tokens, sm.sdmap)
print(calls)