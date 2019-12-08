from collections import namedtuple
from syntaxmap import SyntaxMap
from parse import Parser
class AssignStmt:
    def __init__(self, var, right):
        self.kind = 'AssignStmt'
        self.var = var
        self.right = right

class IfStmt:
    def __init__(self, exp, stmt1, stmt2):
        self.kind = 'IfStmt'
        self.exp = exp
        self.stmt1 = stmt1
        self.stmt2 = stmt2

class WhileStmt:
    def __init__(self, exp, stmt):
        self.kind = 'WhileStmt'
        self.exp = exp
        self.stmt = stmt

class BlockStmt:
    def __init__(self, stmts):
        self.kind = 'BlockStmt'
        self.stmts = stmts

class Stmts:
    def __init__(self, stmts, stmt):
        self.kind = 'Stmts'
        self.stmts = stmts
        self.stmt = stmt

class ExpNode:
    def __init__(self, op, operand1, operand2):# 一元只使用operand1
        self.kind = op
        self.operand1 = operand1
        self.operand2 = operand2

class SingleNode:
    def __init__(self, kind, token):
        self.kind = kind
        self.token = token

sm = SyntaxMap()

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

@sm.syntaxmap(['Stmt','While','(','Exp',')','Stmt'],[3,5])
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
parser.generate(printInfo=True)