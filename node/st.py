# symbol table
class Symbol:
    def __init__(self, name, info, var=None, level=None, depth=None):
        self.name = name # 标识符名字
        self.info = info # 关联的信息，类型或者其它
        self.var = var # 同名标识符的上一层次符号
        self.level = level # 
        self.depth = depth
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name

class SymbolTable:
    def __init__(self):
        self.tb = {}

    def openscope(self):
        self.depth = self.depth+1
        self.scope = []
    
    def closescope(self):
        self.depth = self.depth - 1
        for sym in self.scope:
            prevsym = sym.var
            self.remove(sym)
            if prevsym is not None:
                self.add(prevsym)
    
    def add(self,sym):
        self.tb[sym.name] = sym
    
    def remove(self, sym):
        del self.tb[sym.name]
    
    def get(self, name):
        self.tb.get(name,None)
    
    def enter(self,name,info):
        oldsym = self.get(name)
        if oldsym is not None and oldsym.depth == self.depth:
            # if oldsym.depth == self.depth:
            print('Error:duplicated declaration of {}'.format(name)) 
            return
        newsym = Symbol(name, info,level=self.scope, depth=self.depth)
        self.scope.append(newsym)
        if oldsym is not None:
            newsym.var = oldsym
            self.tb[name] = newsym # 替代 remove(oldsym) add(newsym)
        else:
            self.add(newsym)



