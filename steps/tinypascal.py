import sys
from os import path
sys.path.append(path.join(path.dirname(__file__), '..'))
from lalrparse import Parser

# bool -> bool || join | join
# join -> join && equality | equality
# equality -> equality == rel | equality != rel | rel
# rel -> expr < expr | expr <= expr | expr >= expr | expr > expr | expr
# expr -> expr + term | expr - term | term
# term -> term * unary | term / unary | unary
# unary -> ! unary | - unary | factor
# factor -> ( bool ) | loc | num | real | true | false
# loc -> loc[bool] | id
productions = [
    ['Program','Block'],
    ['Block','{','Decls','Stmts','}'],
    ['Decls','Decls','Decl'],
    ['Decls'],
    ['Decl','Type','id',';'],
    ['Type','int'],
    ['Stmts','Stmts','Stmt'],
    ['Stmts'],
    ['Stmt','Loc','=','Bool',';'],
    ['Stmt','if','(','Bool',')','Stmt'],
    ['Stmt','if','(','Bool',')','Stmt','else','Stmt'],
    ['Stmt','while','(','Bool',')','Stmt'],
    ['Stmt','do','stmt','while','(','Bool',')',';'],
    ['Stmt','break',';'],
    ['Stmt','Block'],
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
    ['Factor','Loc'],
    ['Factor','num'],
    ['Factor','real'],
    ['Factor','true'],
    ['Factor','false'],
    ['Loc','Loc','[','Bool',']'],
    ['Loc','id']
]
terminal = ['{','}','=',';','int','if','else','while','do','break',
            '||','&&','==','!=','<','<=','>','>=','+','-','*','/','!',
            '(',')','[',']','num','false','true','real','id']
nonterminal = ['Program','Block','Stmt','Type','Decls','Decl','Stmts',
                'Bool','Join','Equality','Rel','Expr','Term','Unary','Factor','Loc']

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

parser = Parser(productions,  terminal, nonterminal,precs, precedence, assosiation)
parser.generate(printInfo=True)
tokens = ['id','>','id']
parser.parse(tokens)
'''
function hello()
    if 
''' 