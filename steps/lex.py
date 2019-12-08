import re
class Token:
    def __init__(self, kind, pos, text, val=None, lineno=0):
        self.kind = kind
        self.pos = pos
        self.text = text
        self.val = val
        self.lineno = lineno

    def __str__(self):
        return 'tokenKind:{},pos:{},text:{},val:{}, lineno:{}'.format(self.kind, self.pos, self.text, self.val, self.lineno)
    
    def __repr__(self):
        return 'tokenKind:{},pos:{},text:{},val:{}, lineno:{}'.format(self.kind, self.pos, self.text, self.val, self.lineno)

class Lexer:
    def __init__(self, filename, terminal, patterns):
        self.terminal = terminal
        self.patterns = patterns
        self.filename = filename
        self.lineno = 0
    
    def escape(self):
        reserve = '{}[]()|*+^?.'
        ret = []
        for tt in self.terminal:
            if tt in self.patterns:
                ret.append(t2re[tt])
            else:
                ret.append(''.join(['\\'+t if t in reserve else t for t in tt]))
        ret.append('\s+') # 空白符号
        ret.append('.+?') # 其它任意字符，加入? 改变其模式（不贪婪）
        ret = '|'.join(['('+t+ ')' for t in ret])
        self.reexp = ret
        self.pattern = re.compile(ret)
    
    def lex(self):
        self.escape()
        length = len(self.terminal)
        with open(self.filename) as f:
            for line in f.readlines():
                iters = self.pattern.finditer(line)
                self.lineno = self.lineno + 1
                for i in iters:
                    index = i.lastindex
                    text = i.group()
                    if index == length+1:
                        continue
                    if index >= length+2:
                        # continue
                        print('error')
                        raise Exception('Unexpected word')
                    print(Token(self.terminal[index-1],i.pos,text,lineno=self.lineno))
    


terminal = ['{','}','=',';','int','if','else','while','do','break',
            '||','&&','==','!=','<','<=','>','>=','+','-','*','/','!',
            '(',')','[',']','num','false','true','real','id']
t2re = {'id':'[a-zA-Z_]\w*','num':'\d+','real':'\d*\.\d+'}

# 匹配越宽的表达式放在最后面 比如id的表达式是可以匹配true的
reserve = '{}[]()|*+^?.'

def escape(terminal):
    ret = []
    for tt in terminal:
        if tt in t2re:
            ret.append(t2re[tt])
        else:
            ret.append(''.join(['\\'+t if t in reserve else t for t in tt]))
    return ret

# nt = escape(terminal)
# nt.append('\s+')
# nt.append('.*?')
# nt = '|'.join(['('+t+ ')' for t in nt])

# print(nt)

# pattern = re.compile(nt)

# iters = pattern.finditer('if a>b else a=1')
# length = len(terminal)
# for i in iters:
#     index = i.lastindex
#     text = i.group()
#     if index == length+1:
#         continue
#     if index > length+2:
#         print('error')
#     print('----------')
#     print('{}:{}'.format(index,text))

lexer = Lexer('steps/test.lex',terminal,t2re) #使用调试器运行代码，当前目录下文件访问存在问题
# 此时当前目录是compiler 而不是二级目录steps

# print(list(lexer.lex()))
lexer.lex()

# with open('steps/test.lex','r') as f:
#     print(f.readlines())

    