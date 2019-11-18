## 第一步定义产生式

# (1) E -> E + T 
# (2) E -> T 
# (3) T -> T * F  
# (4) T -> F
# (5) F -> (E)
# (6) F -> id
# productions = {
#     'E':[['E','+','T'],['T'],
#     'T':[['T','*','F'],['F']],
#     'F':[['(','E',')'],['id']]
# }

## SLR存在的问题
## S-> L=R
## S-> R
## L-> *R
## L-> id
## R-> L

## 项目集
## R-> L.
## S-> L.=R
## 显然这里就存在问题，到底是shift，还是reduce
## 这个问题怎么解决，使用最长序列进行匹配（初步想法）
## 这里还有个reduce reduce冲突
## S-> aCe | aDb
## C-> c
## D-> c
## 这个文法其实是没有二义性的
## 当出现项目集
## C-> c.
## D-> c.
## SLR无法确定应该用哪个产生式进行归约
from collections import deque
productions = [
    ['E','E','+','T'],
    ['E','T'],
    ['T','T','*','F'],
    ['T','F'],
    ['F','(','E',')'],
    ['F','id']
]
terminal = ['id','*','+','(',')']
nonterminal = ['E','T','F']

# productions = [
#     ['E','E','+','E'],
#     ['E','id']
# ]
# terminal = ['id','+']
# nonterminal = ['E']

# productions = [
#     ['S','C','C'],
#     ['C','c','C'],
#     ['C','d']
# ]
# terminal = ['c','d']
# nonterminal = ['S','C']

# productions = [
#     ['E','E','+','E'],
#     ['E','E','*','E'],
#     ['E','(','E',')'],
#     ['E','id']
# ]
# terminal = ['(','id','+','*',')']
# nonterminal = ['E']

# productions = [
#     ['E','E','+','E'],
#     ['E','id']
# ]
# terminal = ['id','+']
# nonterminal = ['E']

## I0 = ['START','.','E',$]
## CLOUSE
## ['E','.','E','+','T']

def prehandle():
    p = ['START',productions[0][0]]
    productions.insert(0,p)
prehandle()

# print(productions)

def productions2items():
    ret = []
    for p in productions:
        
        #print([t.insert(i+1,'.') for i in range(len(p))])
        for i in range(len(p)):
            t = p.copy()
            t.insert(i+1,'.')
            ret.append(t)
    return ret
items = productions2items()


FIRST= {}
FOLLOW = {}


def first(A):
    if A in FIRST:
        return FIRST[A]
    if A in terminal:
        FIRST[A] = set([A])
        return [A]
    if A in nonterminal:
        ps = [p for p in productions if p[0] == A]
        ret = set()
        for p in ps:
            if len(p) == 1: #A-> null [A]
                ret.add('')
                continue
            i = 0
            if p[0] == p[1]:# 第一种左递归 A->Ab|c
                continue
            # 第二种递归非直接递归
            if p[1] in nonterminal:
                i = 0
                for t in p[1:]:
                    f = first(t)# 这里依然会出现死循环的问题
                    if '' not in f:
                        ret.update(f)
                        break
                    f.remove('')
                    ret.update(f)
                    i = i+1
                if i == len(p[1:]):
                    ret.add('')
                continue
            ret.add(p[1]) # 终结符
            # for t in p[1:]:
                
            #     f = first(t) # 如果出现左递归就会出现循环
                
                
            #     if '' not in f:#null 不在里面就不需要后面的token的first了
            #         ret.update(f)
            #         break
            #     f.remove('')#把null 移除然后加入
            #     ret.update(f)
            #     i = i+1
            # if i == len(p[1:]):
            #     ret.add('')
        FIRST[A] = ret
        return ret
    return []

def firsts(AS):
    ret = set()
    empty = False
    ff = [first(A) for A in AS]
    i = 0
    for f in ff:
        ret.update(f)
        if '' not in f:
            break
        i = i + 1
    if i < len(ff):#不是所有的集合都包含空
        if '' in ret:
            ret.remove('')
    # 这里没有添加空，是因为我们采用update方法并且没有删除前面集合的空
    return ret


def getNT(A):
    return [item for item in items if item[0]==A and item[1] == '.']



def closure(I):
    ret = []
    unvisited = []
    unvisited.extend(I)
    while len(unvisited) > 0:
        item = unvisited.pop()
        ret.append(item)
        if item[-2] == '.':
            continue
        pos = item.index('.')
        t = item[pos+1]
        if t in nonterminal:
            nt = getNT(t)
            ff = []# first set
            if item[pos+2] == item[-1]:#beta = empty
                ff.append(item[-1])
            else:
                ff = firsts(item[pos+2:-1])
                if '' in ff:# ff长度不可能为0
                    ff.append(item[-1])
            newitems = []
            for p in nt:
                newitems.extend([p+ [f] for f in ff])
            for ni in newitems:
                if ni in ret:
                    continue
                if ni in unvisited:
                    continue
                unvisited.append(ni)
    return ret     

    # for item in I:#item = ['E','E','.','+','T',$]
    #     if item[-2] == '.':#item = ['E','E','+','T','.',$]
    #         ret.append(item)
    #         continue
    #     pos = item.index('.')
    #     t = item[pos+1]
    #     ret.append(item)
    #     if t in nonterminal and t not in visited:
    #         visited.append(t)
    #         nt = getNT(t)
    #         f = []
    #         if item[pos+2] == item[-1]:# beta == epsion empty
    #             f.append(item[-1])
    #         else:
    #             ff = first(item[pos+2])
    #             if len(ff) == 0:
    #                 f.append(item[-1])
    #             else:
    #                 f = ff
    #         newitems = []
    #         for p in nt:
    #             newitems.extend([p+ [ff] for ff in f])
            
    #         newitems = closure(newitems,visited)
    #         ret.extend(newitems)
    # visited.clear()
    # return ret

def goto(I,X):
    ret = []
    for item in I:
        if item[-2] == '.':
            continue
        pos = item.index('.')
        if item[pos+1] == X:
            t = item.copy()
            t[pos] = X
            t[pos+1] = '.'
            ret.append(t)

    return closure(ret)

def printitems(I,printno=False):
    for i,item in enumerate(I):
        s = ' '.join(item[1:])
        n = '({}) '.format(i)
        s = '{}->{}'.format(item[0],s)
        if printno:
            print(n+s)
        else:
            print(s)

I = closure([items[0]+['$']])
# printitems(I)

# def goto(I,X):
#     ret = []
#     for item in I:
#         if item[-1] == '.':
#             continue
#         pos = item.index('.')
#         if item[pos+1] == X:
#             t = item.copy()
#             t[pos] = X
#             t[pos+1] = '.'
#             ret.append(t)

#     return closure(ret)

def I2N(I):
    for i in I:
        for index, v in enumerate(items):
            if i == v:
                print(index)

# printitems(I)
# I2N(I)



def listItems():
    ret = []
    # C = closure([items[0]])
    C = closure([items[0]+['$']])
    #print(C)
    q = deque()
    q.append(C)
    while True:
        if len(q) <= 0 :
            break
        C = q.popleft()
        ret.append(C)
        for X in nonterminal+terminal:
            g = goto(C, X)
            if len(g) == 0:
                continue
            if g in ret:
                continue
            q.append(g)
    return ret




def follow(A):
    if A in FOLLOW:
        return FOLLOW[A]
    #return [ p[p[:1].index(A)+2] for p in productions if A in p[1:] and p[-1]!=A]
    ret = set()
    if A == 'START':
        ret.add('$')
    ps = [p for p in productions if A in p[1:]]
    for p in ps:
        if p[-1] == A:
            f = follow(p[0])
            ret.update(f)
        else:
            pos = p[1:].index(A)
            f = first(p[pos+2])#前面切片从1开始
            if '' in f:
                f.remove('')
                ret.update(f)
                if pos+2 == len(p):# pos+2是最后一个
                    ff = follow(p[0])
                    ret.update(ff)
            else:
                ret.update(f)
    FOLLOW[A] = ret
    return ret

def slrgen(C):
    actions = {}
    gotos = {}
    for state,itemlist in enumerate(C):
        action = {}
        for item in itemlist:
            if item[-2] == '.':# reduce
                # t = item[:-2]
                pos = productions.index(item[:-2])
                # ff = follow(item[0])
                r = 'r'+str(pos)
                # trans = {f:r for f in ff}
                trans = {}
                if item[0] == 'START':
                    trans['$'] = 'acc'
                else:
                    trans[item[-1]] = r
                action.update(trans)
            else:
                pos = item.index('.')
                t = item[pos+1]
                if t in terminal:
                    Ij = goto(itemlist, t)
                    s = C.index(Ij)
                    action[t] = "s"+str(s)
        actions[state] = action
        trans = {}
        for A in nonterminal:
            Ij = goto(itemlist, A)
            if Ij in C:
                trans[A] = C.index(Ij)
        gotos[state] = trans
    return actions, gotos


def slrparse(actions,gotos,tokens):
    pos = 0
    states = [0]
    symbol = []
    tokens.append('$')
    while True:
        if pos == len(tokens):
            break
        current = states[-1]
        t = tokens[pos]
        if t in actions[current]:
            action = actions[current][t]
            if action.startswith('s'):#shift
                s = int(action[1:])
                symbol.append(t)
                states.append(s)
                pos += 1
            elif action.startswith('r'):#reduce
                l = int(action[1:])
                p = productions[l]
                if len(p) >= 1:
                    for i in range(len(p)-1):
                        states.pop()
                        symbol.pop()
                    top = states[-1]
                    s = gotos[top][p[0]]
                    states.append(s)
                    symbol.append(p[0])
                else:
                    s = gotos[current][p[0]]
                    states.append(s)
            elif action.startswith('acc'):
                pos += 1
                print('Accept!')
                break
        else:
            print('ERROR')

C = listItems()

print('---------------------------------')
for i,c in enumerate(C):
    print(i)
    printitems(c)
    print('---------------------------------')
print('*********************************')
printitems(productions,printno=True)

print('*********************************')
actions, gotos = slrgen(C)
header = ''.join(['{:10}'.format(s) for s in ['state']+terminal+['$']+nonterminal])
print(header)
for (k,v),(k1,v1) in zip(actions.items(), gotos.items()):
    s = '{:10}'.format(str(k))
    t = ''.join(['{:10}'.format(str(v.get(i,''))) for i in terminal+['$']])
    n = ''.join(['{:10}'.format(str(v1.get(i,''))) for i in nonterminal])
    p = s+t+n
    sp = ''.join(['-' for i in range(len(p))])
    print(sp)
    print(p)

# ####
# print('---------------------parse---------------------------')
# slrparse(actions, gotos, ['id','+','id'])

## SLR存在的问题
## S-> L=R
## S-> R
## L-> *R
## L-> id
## R-> L

## 项目集
## R-> L.
## S-> L.=R
## 显然这里就存在问题，到底是shift，还是reduce
## 这个问题怎么解决，使用最长序列进行匹配（初步想法）
## 这里还有个reduce reduce冲突
## S-> aCe | aDb
## C-> c
## D-> c
## 这个文法其实是没有二义性的
## 当出现项目集
## C-> c.
## D-> c.
## SLR无法确定应该用哪个产生式进行归约