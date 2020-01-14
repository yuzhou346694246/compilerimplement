class NodeVisitor:
    pass

class AstPrintVisitor(NodeVisitor):
    def __init__(self,root):
        self.root = root
        self.depth = 0
    
    def accept(self):
        self.visit(self.root)
    
    def visit(self,node):
        method = 'visit' + node.kind
        getattr(self, method)(node)
    
    def visitProgram(self, node):
        print('{}:{}'.format(node.kind,node.name))
        self.depthInc()
        self.visit(node.block)
        self.depthDec()
    
    def visitBlock(self, node):
        print('{}{}'.format(self.getstar(),node.kind))
        self.depthInc()
        self.visit(node.stmts)
        self.depthDec()

    def visitStmts(self, node):
        print('{}{}'.format(self.getstar(),node.kind))
        self.depthInc()
        for stmt in node.stmts:
            self.visit(stmt)
        self.depthDec()

    def visitDeclVar(self, node):
        print('{}:{}--{}'.format(self.getstar(),node.kind,node.name))
    
    def visitDeclRecord(self, node):
        print('{}:{}--{}'.format(self.getstar(),node.kind,node.name))
    
    def visitAssignStmt(self, node):
        print('{}:{}'.format(self.getstar(),node.kind))

    def getstar(self):
        x = ''.join(['*' for i in range(self.depth)])
        return x

    def depthInc(self):
        self.depth = self.depth + 1
    
    def depthDec(self):
        self.depth  = self.depth - 1
    