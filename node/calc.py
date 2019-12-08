from syntaxmap import SyntaxMap
from parse import Parser
from lex import Lexer

sm = SyntaxMap()

@sm.syntaxmap(['T','T','*','F'],[1,2,3])
@sm.syntaxmap(['E','E','+','T'],[1,2,3])
def opexp(left,op,right):
    if op.kind == '+':
        return left+right
    if op.kind == '-':
        return left-right
    if op.kind == '*':
        return left*right
    if op.kind == '/':
        return left/right

@sm.syntaxmap(['E','T'],[1])
@sm.syntaxmap(['T','F'],[1])
def texp(val):
    return val

@sm.syntaxmap(['F','(','E',')'],[2])
def lpexp(val):
    return val

@sm.syntaxmap(['F','num'],[1])
def numexp(t):# t is a token
    return t.val

tokens = list(Lexer('1+10*123').lex())
# for t in tokens:
#     print(t)
# print(sm.productions())
# parser = Parser(productions, terminal, nonterminal)
parser = Parser(sm.productions, sm.terminal, sm.nonterminal)
parser.generate(printInfo=True)
parser.parse(tokens, sm.sdmap)