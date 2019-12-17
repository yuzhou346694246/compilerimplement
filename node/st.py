# symbol table
class Symbol:
    def __init__(self, name, attribute, var=None, level=None, depth=None):
        self.name = name # 标识符名字
        self.attribute = attribute # 关联的信息，类型或者其它
        self.var = var # 同名标识符的上一层次符号
        self.level = level # 
        self.depth = depth
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name

class Scope:
    def __init__(self, up):
        self.up = up
        self._scope = []

    def add(self, sym):
        self._scope.append(sym)
    
    def __iter__(self):
        yield from self._scope

class Attribute:
    def __init__(self, kind, typedescriptor):
        self.kind = kind
        self.typedescriptor = typedescriptor

class VarAttribute(Attribute):
    def __init__(self, typedescriptor):
        self.kind = 'VAR'
        self.typedescriptor = typedescriptor
    
class TypeAttribute(Attribute):
    def __init__(self, typedescriptor):
        self.kind = 'Type'
        self.typedescriptor = typedescriptor

class TypeDescriptor:
    pass

class IntegerTypeDescriptor(TypeDescriptor):
    def __init__(self):
        self.typekind = 'Integer'

class RecordTypeDescriptor(TypeDescriptor):
    def __init__(self, fields):
        self.typekind = 'Record'
        self.fields = fields

class BooleanTypeDescriptor(TypeDescriptor):
    def __init__(self):
        self.typekind = 'Boolean'

class SymbolTable:
    def __init__(self):
        self.tb = {}
        self.scope = Scope(None)
        self.depth = 1

    def openscope(self):
        self.depth = self.depth+1
        self.scope = Scope(self.scope)# 新的作用域要与上个作用域联系起来
    
    def closescope(self):
        self.depth = self.depth - 1
        for sym in self.scope:
            prevsym = sym.var
            self.remove(sym)
            if prevsym is not None:
                self.add(prevsym) # 让被覆盖的符号变得可见
        self.scope = self.scope.up # 切换到上面一个作用域 
    
    def add(self,sym):
        self.tb[sym.name] = sym
    
    def remove(self, sym):
        del self.tb[sym.name]
    
    def get(self, name):
        return self.tb.get(name,None)

    '''
    检测变量是否已经在当前作用域声明
    '''
    def declaredlocally(self, name):
        sym = self.get(name)
        if sym is None or sym.depth != self.depth:
            return False
        return True

    def enter(self,name,attribute):
        oldsym = self.get(name)
        # 不能在当前作用域重复声明一个符号
        if oldsym is not None and oldsym.depth == self.depth:
            # if oldsym.depth == self.depth:
            print('Error:duplicated declaration of {}'.format(name)) 
            return
        newsym = Symbol(name, attribute,level=self.scope, depth=self.depth)
        self.scope.add(newsym)
        if oldsym is not None:
            newsym.var = oldsym
            self.tb[name] = newsym # 替代 remove(oldsym) add(newsym)
        else:
            self.add(newsym)



