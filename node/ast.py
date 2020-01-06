from collections import namedtuple
from syntaxmap import SyntaxMap
from parse import Parser
from semantics import TypeCheck
from interpreter import Interperter
from os import path
import sys
sys.path.append(path.join(path.dirname(__file__), '..'))
from steps.lex import Lexer
from analysis import calls
class SyntaxNode:
    def __str__(self):
        return self.kind
    def __repr__(self):
        return self.kind

    
class Program(SyntaxNode):
    def __init__(self, token, stmts):
        self.kind = 'Program'
        self.name = token.text
        self.token = token
        self.stmts = stmts

class Stmt(SyntaxNode):
    pass

class AssignStmt(Stmt):
    def __init__(self, token, right):
        self.kind = 'AssignStmt'
        self.name = token.text
        self.token = token
        self.right = right

class IfStmt(Stmt):
    def __init__(self, exp, stmt1, stmt2):
        self.kind = 'IfStmt'
        self.exp = exp
        self.stmt1 = stmt1
        self.stmt2 = stmt2

class PrintStmt(Stmt):
    def __init__(self,exp):
        self.kind = 'PrintStmt'
        self.exp = exp

class WhileStmt(Stmt):
    def __init__(self, exp, stmt):
        self.kind = 'WhileStmt'
        self.exp = exp
        self.stmt = stmt

class BlockStmt(Stmt):
    def __init__(self, stmts):
        self.kind = 'BlockStmt'
        self.stmts = stmts

class Stmts(Stmt):
    def __init__(self, stmts, stmt):
        self.kind = 'Stmts'
        if stmts is None:
            self.stmts = []
        else:
            self.stmts = stmts.stmts
        self.stmts.append(stmt)
    
#     def __str__(self):
#         return 'Stmts'
    
#     def __repr__(self):
#         return self.kind

class Exp(SyntaxNode):
    pass

class Parentheses(Exp):
    def __init__(self,exp):
        self.kind = 'Parentheses'
        self.exp = exp

class UnaryOperator(Exp):
    def __init__(self, op, exp):
        self.kind = op
        self.exp = exp

class BinaryOperator(Exp):
    def __init__(self, op, left, right): 
        self.kind = op
        self.left = left
        self.right = right

class ConstInt(Exp):
    def __init__(self, token):
        self.kind = 'ConstInt'
        self.val = token.val
        self.token = token

class IdExp(Exp):
    def __init__(self, token):
        self.kind = 'IdExp'
        self.name = token.text
        self.token = token 

class CallExp(Exp):
    def __init__(self, token, aparams):
        self.kind = 'CallExp'
        self.token = token
        self.aparams = aparams 

class Params(SyntaxNode):
    def __init__(self, params):
        self.kind = 'Params'
        self.params = params

class Param(SyntaxNode):
    def __init__(self, token, typenode):
        self.kind = 'Param'
        self.token = token
        self.name = token.text
        self.typenode = typenode


class AParams(Exp):
    def __init__(self, aparams):
        self.kind = 'AParams'
        self.aparams = aparams

class AParam(Exp):
    def __init__(self, exp):
        self.kind = 'AParam'
        self.exp = exp
  

class DeclNode(SyntaxNode):
    pass

class DeclVar(DeclNode):# 声明变量节点
    def __init__(self, token,typenode):
        self.kind = 'DeclVar'
        self.name = token.text
        self.token = token
        self.typenode = typenode

class DeclType(SyntaxNode):
    pass

class DeclRecord(DeclType):
    def __init__(self, token, typenode):
        self.kind = 'DeclRecord'
        self.name = token.text
        self.typenode = typenode

class TypeNode(SyntaxNode):
    pass


class IntType(TypeNode):# 整数类型节点
    def __init__(self, token):
        self.kind = 'IntType'
        self.token = token

class BoolType(TypeNode):
    def __init__(self, token):
        self.kind = 'BoolType'
        self.token = token

class IdType(TypeNode):
    def __init__(self, token):
        self.kind = 'IdType'
        self.name = token.text
        self.token = token 

class RecordType(TypeNode):
    def __init__(self, fields):
        self.kind = 'RecordType'
        self.fields = fields

class RecordField(TypeNode):
    def __init__(self, token, typenode):
        self.kind = 'RecordField'
        self.name = token.text
        self.token = token
        self.typenode = typenode


    


sm = SyntaxMap()
'''
Stmts->Stmts  Stmt | Stmt
Stmt -> id = Exp |
        if ( Exp ) Stmt |
        if ( Exp ) Stmt else Stmt |
        While ( Exp ) Stmt |
        { Stmts }
        Type id 
Type -> int
Exp  -> Exp + Exp
Exp  -> id
Exp  -> num
'''

# @sm.syntaxmap(['Program','program','id',':','{','Stmts','}'],[2,4])
# def programfunc(token,stmts):
#     return Program(token,stmts)

@sm.syntaxmap(['Stmts','Stmts','Stmt'],[1,2])#
def stmtsfunc1(stmts, stmt):
    return Stmts(stmts, stmt)

@sm.syntaxmap(['Stmts','Stmt'],[1])
def stmtsfunc2(stmt):
    return Stmts(None, stmt)

@sm.syntaxmap(['Stmt','id','=','Exp'],[1,3])
def stmtfunc1(token, right):
    return AssignStmt(token, right)

@sm.syntaxmap(['Stmt','if','(','Exp',')','Stmt','else','Stmt'],[3,5,7])
def stmtfunc2(exp, stmt1, stmt2):
    return IfStmt(exp, stmt1, stmt2)

@sm.syntaxmap(['Stmt','if','(','Exp',')','Stmt'],[3,5])
def stmtfunc3(exp, stmt):
    return IfStmt(exp, stmt, None)

@sm.syntaxmap(['Stmt','while','(','Exp',')','Stmt'],[3,5])
def stmtfunc4(exp, stmt):
    return WhileStmt(exp, stmt)

@sm.syntaxmap(['Stmt','{','Stmts','}'],[2])
def stmtfunc5(stmts):
    return BlockStmt(stmts)

@sm.syntaxmap(['Stmt','print','Exp'],[2])
def stmtprint(exp):
    return PrintStmt(exp)

@sm.syntaxmap(['Stmt','Type','id'],[1,2])
def stmtfunc6(typenode, token):
    #idnode = SingleNode('id', token)
    return DeclVar(token,typenode)

@sm.syntaxmap(['Stmt','record','id','{','Fields','}'],[2,4])
def stmtfunc7(token, fields):
    typenode = RecordType(fields)
    return DeclRecord(token, typenode)

@sm.syntaxmap(['Fields','Fields',',','Field'],[1,3])
def fieldsfunc1(fields,field):
    fields.append(field)
    return fields

@sm.syntaxmap(['Fields','Field'],[1])
def fieldsfunc2(field):
    return [field]

@sm.syntaxmap(['Fields'],[])
def fieldsfunc3():
    return []

@sm.syntaxmap(['Field','Type','id'],[1,2])
def fieldfunc1(typenode, token):
    return RecordField(token, typenode)

@sm.syntaxmap(['Type','int'],[1])
# @sm.syntaxmap(['Type','bool'],[1])
def typefunc1(token):
    if token.kind == 'int':
        return IntType(token)
    # if token.kind == 'bool':
    #     return BoolType(token)

@sm.syntaxmap(['Type','id'],[1])
def typefunc2(token):
    return IdType(token)

@sm.syntaxmap(['Exp','Exp','+','Exp'],[1,2,3])
@sm.syntaxmap(['Exp','Exp','-','Exp'],[1,2,3])
@sm.syntaxmap(['Exp','Exp','*','Exp'],[1,2,3])
@sm.syntaxmap(['Exp','Exp','/','Exp'],[1,2,3])
def expfunc1(left,op,right):
    if op.kind == '+':
        return BinaryOperator('Plus',left,right)
    if op.kind == '-':
        return BinaryOperator('Minus',left,right)
    if op.kind == '*':
        return BinaryOperator('Multiply',left,right)
    if op.kind == '/':
        return BinaryOperator('Divide',left,right)

@sm.syntaxmap(['Exp','Exp','>','Exp'],[1,2,3])
@sm.syntaxmap(['Exp','Exp','<','Exp'],[1,2,3])
@sm.syntaxmap(['Exp','Exp','>=','Exp'],[1,2,3])
@sm.syntaxmap(['Exp','Exp','<=','Exp'],[1,2,3])
@sm.syntaxmap(['Exp','Exp','!=','Exp'],[1,2,3])
@sm.syntaxmap(['Exp','Exp','==','Exp'],[1,2,3])
@sm.syntaxmap(['Exp','Exp','||','Exp'],[1,2,3])
@sm.syntaxmap(['Exp','Exp','&&','Exp'],[1,2,3])
def exprelfunc(left,op,right):
    if op.kind == '>':
        return BinaryOperator('GT',left,right)
    if op.kind == '<':
        return BinaryOperator('ST',left,right)
    if op.kind == '>=':
        return BinaryOperator('GE',left,right)
    if op.kind == '<=':
        return BinaryOperator('SE',left,right)
    if op.kind == '!=':
        return BinaryOperator('NE',left,right)
    if op.kind == '==':
        return BinaryOperator('EQ',left,right)
    if op.kind == '||':
        return BinaryOperator('OR',left,right)
    if op.kind == '&&':
        return BinaryOperator('AND',left,right)

@sm.syntaxmap(['Exp','!','Exp'],[1,2])
@sm.syntaxmap(['Exp','-','Exp'],[1,2])
def expunaryfunc(op, exp):
    if op.kind == '!':
        return UnaryOperator('NOT',exp)
    if op.kind == '-':
        return UnaryOperator('NEG',exp)

@sm.syntaxmap(['Exp','(','Exp',')'],[2])
def expparentheses(exp):
    return Parentheses(exp)

@sm.syntaxmap(['Exp','id'],[1])
@sm.syntaxmap(['Exp','num'],[1])
def expfunc2(token):
    if token.kind == 'id':
        return IdExp(token)
    
    if token.kind == 'num':
        return ConstInt(token)

# @sm.syntaxmap(['Exp','id','(','AParams',')'],[1,3])
# def expcall(token, aparams):
#     return CallExp(token, aparams)



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

precs = {
    'UMINUS':['Exp','-','Exp']
}

parser = Parser(sm.productions, sm.terminal, sm.nonterminal,precs,precedence)

Parser.printitems(sm.productions, printno=True)
# print(sm.terminal)
t2p = {'id':'[a-zA-Z_]\w*','num':'\d+'}
lexer = Lexer('node/test2.dm',sm.terminal,t2p)
# lexer = Lexer('test2.dm',sm.terminal,t2p)
# print(list(lexer.lex()))
# for t in lexer.lex():
#     print(t)

parser.generate()
parser.dumpjson()
# parser.loadjson()
parser.htmlparse('test.html')
tokens = list(lexer.lex())
# tree = parser.parse(tokens ,sm.sdmap)
# typeCheck = TypeCheck(tree)
# typeCheck.init()
# typeCheck.accept()
# inter = Interperter(tree)
# inter.accept()
print(calls)