from lalrparse import Parser

productions = [
    ['E','E','+','E'],
    ['E','E','*','E'],
    ['E','E','/','E'],
    ['E','(','E',')'],
    ['E','E','-','E'],
    ['E','E','||','E'],
    ['E','E','&&','E'],
    ['E','E','>=','E'],
    ['E','E','>','E'],
    ['E','E','<=','E'],
    ['E','E','<','E'],
    ['E','E','==','E'],
    ['E','E','!=','E'],
    ['E','-','E'],
    ['E','!','E'],
    ['E','id']
]

precs = {
    'UMINUS':['E','-','E']
}

terminal = ['(','id','+','*',')','-','/','||','&&','>=','>','<','<=',
    '==','!=','!'
]
nonterminal = ['E']
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
    'UMINUS':15
}

assosiation = {# 结合律
    '+':'L',
    '-':'L',
    '*':'L',
    '/':'L',
    'UMINUS':'R'
}


parser = Parser(productions, precs, terminal, nonterminal, precedence, assosiation)
parser.generate(printInfo=True)