class NodeVisitor:
    pass

class AstPrintVisitor(NodeVisitor):
    def __init__(self,root):
        self.root = root
        self.depth = 0
    
    def accept(self):
        self.visit(self.root)
    
    def visit(self, node):
        if node.kind in ['Plus','Minus','Multiply','Divide','GT','ST','GE','SE','NE','EQ','OR','AND']:
            self.visitPlus(node)
        else:
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
        print('{}{}'.format(self.getstar(),node.kind))
        self.depthInc()
        print('{}{}'.format(self.getstar(),node.name))
        self.visit(node.typenode)
        self.depthDec()
    
    def visitDeclRecord(self, node):
        print('{}{}'.format(self.getstar(),node.kind,node.name))
        self.depthInc()
        print('{}name:{}'.format(self.getstar(),node.name))
        print('{}fields'.format(self.getstar()))
        self.depthInc()
        for field in node.fields:
            self.visit(field)
        self.depthDec()
        self.depthDec()
    
    def visitIntType(self, node):
        print('{}{}'.format(self.getstar(),node.kind))
    
    def visitIdType(self, node):
        print('{}{}:{}'.format(self.getstar(), node.kind,self.name))

    def visitRecordField(self , node):
        print('{}Field:{}'.format(self.getstar(),node.name))
        self.depthInc()
        self.visit(node.typenode)
        self.depthDec()
    
    def visitAssignStmt(self, node):
        print('{}{}'.format(self.getstar(),node.kind))
        self.depthInc()
        print('{}{}'.format(self.getstar(),node.name))
        self.visit(node.right)
        self.depthDec()

    def visitConstInt(self,node):
        print('{}{}'.format(self.getstar(),node.token.text))

    def getstar(self):
        x = '|    '*self.depth + '|__'
        return x

    def depthInc(self):
        self.depth = self.depth + 1
    
    def depthDec(self):
        self.depth  = self.depth - 1
    
    def visitFunction(self, node):
        print('{}{}:{}'.format(self.getstar(),node.kind, node.name))
        self.depthInc()
        self.visit(node.params)
        self.visit(node.rettype)
        # self.depthDec()

        # self.depthInc()
        # for stmt in node.stmts:
        #     self.visit(stmt)
        self.visit(node.stmts)
        self.depthDec()
    
    def visitParams(self,node):
        print('{}{}'.format(self.getstar(),node.kind))
        self.depthInc()
        for param in node.params:
            self.visit(param)
        self.depthDec()
    
    def visitParam(self, node):
        print('{}{}'.format(self.getstar(),node.kind))
        self.depthInc()
        print('{}{}'.format(self.getstar(),node.name))
        self.visit(node.typenode)
        self.depthDec()
    
    def visitPlus(self, node):
        print('{}{}'.format(self.getstar(),node.kind))
        self.depthInc()
        self.visit(node.left)
        self.visit(node.right)
        self.depthDec()

    def visitIdExp(self, node):
        print('{}{}:{}'.format(self.getstar(),node.kind,node.name))
    
    def visitCallExp(self, node):
        print('{}Call:{}'.format(self.getstar(),node.name))
        self.depthInc()
        self.visit(node.aparams)
        self.depthDec()
    
    def visitAParams(self, node):
        print('{}{}'.format(self.getstar(),node.kind))
        self.depthInc()
        for aparam in node.aparams:
            self.visit(aparam)
        self.depthDec()
    
    def visitAParam(self, node):
        print('{}{}'.format(self.getstar(),node.kind))
        self.depthInc()
        self.visit(node.exp)
        self.depthDec()
    
    def visitInvokeFunction(self, node):
        print('{}Invoke:{}'.format(self.getstar(),node.name))
        self.depthInc()
        self.visit(node.aparams)
        self.depthDec()

class AstTraversalVisitor(NodeVisitor):
    def __init__(self,root):
        self.root = root
        self.depth = 0
    
    def accept(self):
        yield from self.visit(self.root)
    
    def visit(self,node):
        method = 'visit' + node.kind
        yield from getattr(self, method)(node)
    
    def visitProgram(self, node):
        # yield from [node.kind,'{']
        # yield node.kind
        # yield '{'
        # yield node.name,
        # yield ':',
        # yield 'Block',
        # yield ':',
        
        # yield '}'
        yield '{}:{}'.format(node.kind,node.name)
        # self.depthInc()
        yield '['
        yield from self.visit(node.block)
        yield ']'
        # self.depthDec()
    
    def visitBlock(self, node):
        # print('{}{}'.format(self.getstar(),node.kind))
        yield node.kind
        # self.depthInc()
        yield '['
        yield from self.visit(node.stmts)
        yield ']'
        # self.depthDec()

    def visitStmts(self, node):
        # print('{}{}'.format(self.getstar(),node.kind))
        yield node.kind
        # self.depthInc()
        yield '['
        for stmt in node.stmts:
            yield from self.visit(stmt)
        yield ']'
        # self.depthDec()

    def visitDeclVar(self, node):
        # print('{}{}'.format(self.getstar(),node.kind))
        yield node.kind
        # self.depthInc()
        yield '['
        # print('{}{}'.format(self.getstar(),node.name))
        yield node.name
        yield from self.visit(node.typenode)
        # self.depthDec()
        yield ']'
    
    def visitDeclRecord(self, node):
        # print('{}{}'.format(self.getstar(),node.kind,node.name))
        yield node.kind
        yield '['
        # self.depthInc()
        # print('{}name:{}'.format(self.getstar(),node.name))
        yield node.name
        yield 'fields'
        # print('{}fields'.format(self.getstar()))
        # self.depthInc()
        yield '['
        for field in node.fields:
            yield from self.visit(field)
        yield ']'
        yield ']'
        # self.depthDec()
        # self.depthDec()
    
    def visitIntType(self, node):
        # print('{}{}'.format(self.getstar(),node.kind))
        yield node.kind
    
    def visitIdType(self, node):
        # print('{}{}:{}'.format(self.getstar(), node.kind,self.name))
        yield '{}:{}'.format(node.kind,self.name)

    def visitRecordField(self , node):
        # print('{}Field:{}'.format(self.getstar(),node.name))
        yield 'Field:{}'.format(node.name)
        # self.depthInc()
        yield '['
        yield from self.visit(node.typenode)
        yield ']'
        # self.depthDec()
    
    def visitAssignStmt(self, node):
        # print('{}{}'.format(self.getstar(),node.kind))
        yield node.kind
        # self.depthInc()
        # print('{}{}'.format(self.getstar(),node.name))
        yield '['
        yield node.name
        yield from self.visit(node.right)
        # self.depthDec()
        yield ']'

    def visitConstInt(self,node):
        # print('{}{}'.format(self.getstar(),node.token.text))
        yield node.token.text

    def getstar(self):
        x = '|    '*self.depth + '|__'
        return x

    def depthInc(self):
        self.depth = self.depth + 1
    
    def depthDec(self):
        self.depth  = self.depth - 1
    
    