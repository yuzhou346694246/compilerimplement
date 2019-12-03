import re

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

nt = escape(terminal)
nt.append('\s+')
nt.append('.*?')
nt = '|'.join(['('+t+ ')' for t in nt])

print(nt)

pattern = re.compile(nt)

iters = pattern.finditer('if a>b else a=1')
length = len(terminal)
for i in iters:
    index = i.lastindex
    text = i.group()
    if index == length+1:
        continue
    if index > length+2:
        print('error')
    print(text)

    