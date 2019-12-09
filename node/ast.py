from collections import namedtuple
from syntaxmap import SyntaxMap
from parse import Parser
from os import path
import sys
sys.path.append(path.join(path.dirname(__file__), '..'))
from steps.lex import Lexer
class AssignStmt:
    def __init__(self, var, right):
        self.kind = 'AssignStmt'
        self.var = var
        self.right = right
    
    def __str__(self):
        return 'AssignStmt'
    
    def __repr__(self):
        return self.kind

class IfStmt:
    def __init__(self, exp, stmt1, stmt2):
        self.kind = 'IfStmt'
        self.exp = exp
        self.stmt1 = stmt1
        self.stmt2 = stmt2

    def __str__(self):
        return 'IfStmt'
    
    def __repr__(self):
        return self.kind

class WhileStmt:
    def __init__(self, exp, stmt):
        self.kind = 'WhileStmt'
        self.exp = exp
        self.stmt = stmt
    
    def __str__(self):
        return 'WhileStmt'
    
    def __repr__(self):
        return self.kind

class BlockStmt:
    def __init__(self, stmts):
        self.kind = 'BlockStmt'
        self.stmts = stmts
    
    def __str__(self):
        return 'BlockStmt'
    
    def __repr__(self):
        return self.kind

class Stmts:
    def __init__(self, stmts, stmt):
        self.kind = 'Stmts'
        self.stmts = stmts
        self.stmt = stmt
    
    def __str__(self):
        return 'Stmts'
    
    def __repr__(self):
        return self.kind

class ExpNode:
    def __init__(self, op, operand1, operand2):# 一元只使用operand1
        self.kind = op
        self.operand1 = operand1
        self.operand2 = operand2
    
    def __str__(self):
        return self.kind
    
    def __repr__(self):
        return 'ExpNode:' + self.kind

class SingleNode:
    def __init__(self, kind, token):
        self.kind = kind
        self.token = token
    
    def __str__(self):
        return self.kind
    
    def __repr__(self):
        return self.kind+':'+self.token.text

sm = SyntaxMap()
'''
Stmts->Stmts ; Stmt | Stmt
Stmt -> id = Exp |
        if ( Exp ) Stmt |
        if ( Exp ) Stmt else Stmt |
        While ( Exp ) Stmt |
        { Stmts }
Exp  -> Exp + Exp
Exp  -> id
Exp  -> num
'''

@sm.syntaxmap(['Stmts','Stmts',';','Stmt'],[1,3])
def stmtsfunc1(stmts, stmt):
    return Stmts(stmts, stmt)

@sm.syntaxmap(['Stmts','Stmt'],[1])
def stmtsfunc2(stmt):
    return Stmts(None, stmt)

@sm.syntaxmap(['Stmt','id','=','Exp'],[1,3])
def stmtfunc1(var, right):
    return AssignStmt(var, right)

@sm.syntaxmap(['Stmt','if','(','Exp',')','Stmt','else','Stmt'],[3,5,7])
def stmtfunc2(exp, stmt1, stmt2):
    return IfStmt(exp, stmt1, stmt2)

@sm.syntaxmap(['Stmt','if','(','Exp',')','Stmt'],[3,5])
def stmtfunc3(exp, stmt):
    return IfStmt(exp, stmt, None)

@sm.syntaxmap(['Stmt','while','(','Exp',')','Stmt'],[3,5])
def stmtfunc4(exp, stmt):
    return WhileStmt(exp, stmt)

@sm.syntaxmap(['Stmt','{','Stmts','}'],[3])
def stmtfunc5(stmts):
    return BlockStmt(stmts)

@sm.syntaxmap(['Exp','Exp','+','Exp'],[1,2,3])
def expfunc1(left,op,right):
    if op.kind == '+':
        return ExpNode('+',left,right)

@sm.syntaxmap(['Exp','id'],[1])
@sm.syntaxmap(['Exp','num'],[1])
def expfunc2(token):
    if token.kind == 'id':
        return SingleNode('id', token)
    
    if token.kind == 'num':
        return SingleNode('num', token)

parser = Parser(sm.productions, sm.terminal, sm.nonterminal)

# print(sm.terminal)
t2p = {'id':'[a-zA-Z_]\w*','num':'\d+'}
lexer = Lexer('node/test.dm',sm.terminal,t2p)
# print(list(lexer.lex()))
# for t in lexer.lex():
#     print(t)

parser.generate(printInfo=True)
tokens = list(lexer.lex())
parser.parse(tokens ,sm.sdmap)