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
class SyntaxMap:
    def __init__(self):
        self.sdmap = []

    def syntaxmap(self, grammar, params):
        def decorator(f):
            self.sdmap.append([grammar, params,f])
            @wraps(f)
            def wrapper(*args, **kwds):
                return f(*args, **kwds)
            return wrapper
        return decorator
    
    @property
    def productions(self):
        if hasattr(self, '_productions'):
            return self._productions
        self._productions = [g for g,_,_ in self.sdmap]
        self._p2TAndN()
        return self._productions
    
    @property
    def terminal(self):
        if hasattr(self, '_terminal'):
            return self._terminal
        else:
            self.productions()
            return self._terminal

    @property
    def nonterminal(self):
        if hasattr(self, '_nonterminal'):
            return self._nonterminal
        else:
            self.productions()
            return self._terminal

    def _p2TAndN(self):
        nont = []
        tt = []
        for p in self._productions:
            if p[0] not in nont:
                nont.append(p[0])
        
        for p in self._productions:
            for t in p[1:]:
                if t not in nont and t not in tt:
                    tt.append(t)

        # for p in self._productions:
            # if p[0][0].isupper() :
            #     if p[0] not in nont:
            #         nont.append(p[0])

            # for t in p[1:]:
            #     if t.islower():
            #         if t not in tt:
            #             tt.append(t)

            #     if not t.isalnum():
            #         if t not in tt:
            #             tt.append(t)
        self._nonterminal = nont
        self._terminal = tt

# sm = SyntaxMap()

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

# tokens = list(Lexer('1+10*123').lex())
# parser = Parser(sm.productions, sm.terminal, sm.nonterminal)
# parser.generate(printInfo=True)
# parser.parse(tokens, sm.sdmap)

# print(sdmap)