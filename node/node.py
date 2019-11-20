
class Expression:
    pass

class BinaryExpression(Expression):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right
    

class UnaryExpression(Expression):
    def __init__(self, op, exp):
        self.op = op
        self.exp = exp

class Function:
    pass
    
class Statement:
    pass

class IfStatement(Statement):
    def __init__(self, exp, ifstmts, elsestmts):
        self.exp = exp
        self.ifstmts = ifstmts
        self.elsestmts = elsestmts

class WhileStatement(Statement):
    def __init__(self, exp, stmts):
        self.exp = exp
        self.stmts = stmts

