# 语义分析
from st import SymbolTable, IntegerTypeDescriptor, RecordTypeDescriptor, TypeAttribute, VarAttribute, Symbol
class TypeCheck:
    def __init__(self, root):
        self.root = root
        self.table = SymbolTable()
    
    def init(self):
        desc = IntegerTypeDescriptor()
        attribute = TypeAttribute(desc)
        self.table.enter('int',attribute)
    
    def visit(self, node):
        method = 'visit' + node.kind
        getattr(self, method)(node)
        # if node.kind == 'AssignStmt':
        #     pass
        # if node.kind == 'IfStmt':
        #     pass
        # if node.kind == 'WhileStmt':
        #     pass
        # if node.kind == 'BlockStmt':
        #     pass
        # if node.kind == 'Stmts':
        #     pass
        # if node.kind == 'Plus':
        #     pass
        # if node.kind == 'ConstInt':
        #     pass
        # if node.kind == 'IdNode':
        #     pass
        # if node.kind == 'DeclVar':
        #     pass
        # if node.kind == 'DeclRecord':
        #     pass
        # if node.kind == 'IntType':
        #     pass
        # if node.kind == 'IdType':
        #     pass
        # if node.kind == 'RecordType':
        #     pass
        # if node.kind == 'RecordField':
        #     pass

    def visitStmts(self, node):
        for stmt in node.stmts:
            self.visit(stmt)
    
    def visitWhileStmt(self, node):
        self.visit(node.exp)
        self.visit(node.stmt)
    
    def visitBlockStmt(self, node):
        self.table.openscope()# 进入作用域
        for stmt in node.stmts:
            self.visit(stmt)
        self.table.closescope()

    def visitIntType(self ,node):
        typedescriptor = self.table.get('int')
        node.typedescriptor = typedescriptor

    def visitIdType(self, node):
        name = node.name
        sym = self.table.get(name)
        if sym is None or sym.attribute.kind != 'Type':
            print('Type {} is not define'.format(name))
        node.typedescriptor = sym.attribute.typedescriptor

    def visitAssignStmt(self, node):
        name = node.name
        sym = self.table.get(name)
        if sym is None:
            print('{} not define'.format(name))
        ltype = sym.attribute.typedescriptor
        # rnode = visit(node.right)
        if ltype != node.right.typedescriptor:
            print('assign type ')
    
    def visitPlus(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if left.typedescriptor == right.typedescriptor:
            node.typedescriptor = left.typedescriptor
        else:
            print('Plus:operand type is not same!')

    def visitConstInt(self, node):
        typedescriptor = self.table.get('int')
        node.val = int(node.token.text)
        node.typedescriptor = typedescriptor
    
    def visitDeclVar(self, node):
        name = node.name
        if self.table.declaredlocally(name):
            print('duplicate declaration of {}'.format(name))
        # 出错应该怎么处理的问题
        typedescriptor = node.typenode.typedescriptor
        attribute = VarAttribute(typedescriptor)
        self.table.enter(name, attribute)
        #return node 
    

    def visitDeclRecord(self, node):
        name = node.name
        if self.table.declaredlocally(name):
            print('duplicate record declaration of {}'.format(name))
        for field in node.fields:
            self.visit(field)
        typedescriptor = RecordTypeDescriptor({field.name:field.typedescriptor for field in node.fields})
        attribute = TypeAttribute(typedescriptor)
        self.table.enter(name, attribute)
    
    def visitRecordField(self, node):
        self.visit(node.typenode)

