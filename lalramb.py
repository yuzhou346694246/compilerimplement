## 让LALR支持带二义性的语法
## E->E+E|E*E|(E)|id
## 这种语法就是带二义性的，可以将其改写为非二义性的语法
## 但是这种改写方法会增加编写语法的复杂性
## stmt-> if expr then stmt | if expr the stmt else stmt
## 同样这个语法也是二义性的

# 基于优先级和结合律的方法
# 对于 E->E+E. +  E->E.+E + 这种情况 此处要考虑结合律
# 对于 E->E+E. *  E->E.*E 此处要考虑优先级的问题
# 方法如下，如果发生冲突，reduce产生式最近的一个终结符（第一个例子是+）
# 与我们要reduce的终结符进行匹配，如果优先级相同，按照结合律进行
# 如果优先级不同，优先级高的执行
# 但是这里有个问题，有些终结符有多种含义，那其优先级就不确定（两种优先级）
# -1+1 那么第一个负号优先级肯定高于第二个+号


## LR(1) 存在的优点
## 功能非常强大，只要不是二义性语法都是识别
## 但是缺点也是非常明显
## 就拿例子中的语法，使用slr只有11个状态
## 使用lr有22个状态，显然这个状态有点多，这还只是只有几个语法的情况下
## 所以这里提出LALR的改进型方法
# 16
# F->( E ) . $
# ---------------------------------
# 21
# F->( E ) . )
# ---------------------------------
## 我们观察lr中的状态，有些状态是可以合并的，比如16和21
## 这两个状态都只有一个项，同样也是reduce操作，完全可以合并在一起
## 同样20和14也是这种情况，也可以合并在一起
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

# productions = [
#     ['E','E','+','T'],
#     ['E','T'],
#     ['T','T','*','F'],
#     ['T','F'],
#     ['F','(','E',')'],
#     ['F','id']
# ]
# terminal = ['+','*','(',')','id']
# nonterminal = ['E','T','F']
# productions = [
#     ['S','C','C'],
#     ['C','c','C'],
#     ['C','d']
# ]
# terminal = ['c','d']
# nonterminal = ['S','C']

productions = [
    ['E','E','+','E'],
    ['E','E','*','E'],
    ['E','(','E',')'],
    ['E','id']
]
terminal = ['(','id','+','*',')']
nonterminal = ['E']

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

def getNT(A):
    return [item for item in items if item[0]==A and item[1] == '.']


FIRST= {}
FOLLOW = {}

# def first(A):
#     if A in FIRST:
#         return FIRST[A]
#     if A in terminal:
#         FIRST[A] = set([A])
#         return [A]
#     if A in nonterminal:
#         ps = [p for p in productions if p[0] == A]
#         ret = set()
#         for p in ps:
#             if len(p) == 1: #A-> null [A]
#                 ret.add('')
#                 continue
#             for t in p[1:]:
#                 f = first(t)
#                 if '' not in f:#null 不在里面就不需要后面的token的first了
#                     ret.update(f)
#                     break
#                 f.remove('')#把null 移除然后加入
#                 ret.update(f)
#         FIRST[A] = ret
#         return ret
#     return []

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
                    f = first(t)# 这里依然有可能会出现死循环的问题,如果语法中出现循环
                    # 如 A->SB
                    #    S->A
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
# def closure(I, visited=[]):
#     ret = []
#     for item in I:#item = ['E','E','.','+','T',$]
#         if item[-2] == '.':#item = ['E','E','+','T','.',$]
#             ret.append(item)
#             continue
#         pos = item.index('.')
#         t = item[pos+1]
#         ret.append(item)
#         if t in nonterminal and t not in visited:
#             visited.append(t)
#             nt = getNT(t)
#             f = []
#             if item[pos+2] == item[-1]:# beta == epsion empty
#                 f.append(item[-1])
#             else:
#                 ff = first(item[pos+2])
#                 if len(ff) == 0:
#                     f.append(item[-1])
#                 else:
#                     f = ff
#             newitems = []
#             for p in nt:
#                 newitems.extend([p+ [ff] for ff in f])
            
#             newitems = closure(newitems,visited)
#             ret.extend(newitems)
#     visited.clear()
#     return ret

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
from collections import deque


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
## LR集合与LALR集合
## 对于每个由LR closure函数产生的集合，剔去LR（1）中的1之后，形成的集合一定在SLR中
## 举个例子
# {['START','.','E','$'],
# ['E','.',E','+','E','$'],
# ['E','.','id','$'],
# ['E','.','E','+','E','+']
# ['E','.','id','+']
# }
# => SLR集合
# {
#   ['START','.','E'],
#   ['E','.','E','+','E'],
#   ['E','.','id']
# }
def listlalritems():
    ret = []
    lr0 = []
    lalritems = []
    # C = closure([items[0]])
    C = closure([items[0]+['$']])
    # lr0.append([item[:-1] for item in C])
    ### 此处用来生成LALR 项目
    tt = []
    for item in C:#删除最后一个1
        if item[:-1] in tt:
            continue
        tt.append(item[:-1])
    lr0.append(tt)
    lalritems.append(C)
    ####
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
            ### 此部分用来生成LALR 项目
            ## 这个过程很简单lr0 用来表示slr的项目集
            ## 既然LALR与SLR项目集数量是一样的
            ## 当产生一个新的LR(1)项目集合时，我们求出其SLR，如果这个SLR在lr0中
            ## 这时候只需要判定每个item是否在集合中，不在就添加进去
            tt = []
            for item in g:
                if item[:-1] in tt:
                    continue
                tt.append(item[:-1])
            judge1 = False
            for l in lr0:
                test = [t in l for t in tt]
                if False not in test:
                    judge1 = True
                    break
            judge2 = False
            if tt in lr0:
                judge2 = True
                pos = lr0.index(tt)
                arr = lalritems[pos]
                for item in g:
                    if item not in arr:
                        arr.append(item)
                continue
            else:
                lalritems.append(g)
                lr0.append(tt)
            ### 
            if judge1 == True and judge2 == False:
                print('Warning!')
            q.append(g)
    return lalritems



def lalrgen(C):
    actions = {}
    gotos = {}
    for state,itemlist in enumerate(C):
        action = {}
        for a in terminal+['$']:
            Ij = goto(itemlist, a)
            if len(Ij) == 0:
                # 如果没有集合为空，这里要考虑a是不是在itemlist向前看的符号中
                # 如果不是就直接跳到下一个
                # 如果是，那么这就会出现收敛
                ps = [item for item in itemlist if item[-2] == '.']
                if len(ps) == 0:# 如果没有reduce的项目，那肯定直接返回
                    continue
                lf = [item[-1] for item in itemlist]
                if a in lf:
                    # ps = [item[:-2] for item in itemlist if item[-1] == a]
                    ps = [p[:-2] for p in ps if p[-1] == a]
                    indexs = [str(productions.index(p)) for p in ps]
                    r = '|'.join(indexs) # 如果indexs存在多个值，那么说明语法发生了reduce/reduce冲突
                    action[a] = 'r'+r
                    if a == '$' and '0' in indexs:#START production in positon 0
                        action['$'] = 'acc'
                else:
                    continue
            else:
                # i = C.index(Ij)
                if state == 2:
                    test1 =   1
                i = -1
                for ii, cc in enumerate(C):
                    test = [j in cc for j in Ij]
                    if False in test:
                        continue
                    else:
                        i = ii
                ps = [item[:-2] for item in itemlist if item[-2]=='.' and item[-1]==a]
                indexs = [str(productions.index(p)) for p in ps]
                r = ''
                if len(indexs) > 0:# 发生了reduce/shift conflict
                    r = '||r'+'|'.join(indexs)
                action[a] = 's'+str(i)+r
        actions[state] = action
        ## 非终结符的情况
        trans = {}
        for A in nonterminal:
            Ij = goto(itemlist, A)# 这里的goto也是lr的goto
            if len(Ij) == 0:
                continue
            for i,cc in enumerate(C):
                test = [j in cc for j in Ij]
                if False in test:
                    continue
                else:
                    trans[A] = i
                    break
        gotos[state] = trans
    return actions, gotos

# 把lr items 转换为 lalr items 
def lr2lalr(C):
    slr = []
    for itemlist in C:
        slr.append([item[:-1] for item in itemlist])
    indexs = {i:slr.index(s) for i,s in enumerate(slr)}
    ret = {}
    for k,v in indexs.items():
        if v in ret:
            for i in C[k]:
                if i not in ret[v]:
                    t = ret[v]
                    t.append(i)
                    ret[v] = t
        else:
            ret[v] = C[k]
    return list(ret.values())

def lalrgen1(C):# C = lalritems
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
                s = -1
                ##
                ##
                if t in terminal:
                    Ij = goto(itemlist, t)# 这里的goto依然是lr的goto，其生成的集合一定是lalr项目集合一个子集合的子集
                    for i,cc in enumerate(C):
                        test = [j in cc for j in Ij]
                        if False in test:
                            continue
                        else:
                            s = i
                            break
                    action[t] = "s"+str(s)
        actions[state] = action
        trans = {}
        for A in nonterminal:
            Ij = goto(itemlist, A)# 这里的goto也是lr的goto
            if len(Ij) == 0:
                continue
            for i,cc in enumerate(C):
                test = [j in cc for j in Ij]
                if False in test:
                    continue
                else:
                    trans[A] = i
                    break
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
lrC = listItems()
lalrC = lr2lalr(lrC)
# for i,c in enumerate(lalrC):
#     print(i)
#     printitems(c)
#     print('---------------------------------')

C = lalrC#listlalritems()
print('---------------------------------')
for i,c in enumerate(C):
    print(i)
    printitems(c)
    print('---------------------------------')
print('*********************************')
printitems(productions,printno=True)
print('*********************************')
actions, gotos = lalrgen(C)
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