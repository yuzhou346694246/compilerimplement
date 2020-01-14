
from collections import deque
import json
import pickle
import sys
from os import path
sys.path.append(path.join(path.dirname(__file__), '..'))
from analysis import timer
class Parser:
    FIRST = {}
    FOLLOW = {}

    def __init__(self, productions, terminal, nonterminal,precs={}, precedence={}, assosiation={}):
        self.productions = productions
        self.precs = precs
        self.terminal = terminal
        self.nonterminal = nonterminal
        self.precedence = precedence
        self.assosiation = assosiation
        self._cacheNT = {}
    
    def addstart(self):
        p = ['START', self.productions[0][0]]
        self.productions.insert(0,p)
        tt = self.terminal + self.nonterminal + ['$']
        self.FIRST = {t:self.first(t) for t in tt}
        self.productions2items()
        self._getNT = {t:self.getNT(t) for t in self.nonterminal}
        self._goto = {}
        self._closure = {}
    
    def productions2items(self):
        ret = []
        for p in self.productions:
            for i in range(len(p)):
                t = p.copy()
                t.insert(i+1,'.')
                ret.append(t)
        self.items = ret

    @timer
    def getNT(self,A):
        if A in self._cacheNT:
            return self._cacheNT[A]
        ret =  [item for item in self.items if item[0]==A and item[1] == '.']
        self._cacheNT[A] = ret
        return ret
    
    @timer
    def first(self, A):
        if A in self.FIRST:
            return self.FIRST[A]
        if A in self.terminal:
            self.FIRST[A] = [A]
            return [A]
        if A in self.nonterminal:
            ps = [p for p in self.productions if p[0] == A]
            ret = set()
            for p in ps:
                if len(p) == 1: #A-> null [A]
                    ret.add('')
                    continue
                i = 0
                if p[0] == p[1]:# 第一种左递归 A->Ab|c
                    continue
                # 第二种递归非直接递归
                if p[1] in self.nonterminal:
                    i = 0
                    for t in p[1:]:
                        f = self.first(t)# 这里依然有可能会出现死循环的问题,如果语法中出现循环
                        if '' not in f:# 如 A->SB S->A    
                            ret.update(f)
                            break
                        f.remove('')
                        ret.update(f)
                        i = i+1
                    if i == len(p[1:]):
                        ret.add('')
                    continue
                ret.add(p[1]) # 终结符
            self.FIRST[A] = list(ret)
            return ret
        return []

    @timer
    def firsts(self, AS):
        ret = set()
        empty = False
        # ff = [self.first(A) for A in AS]
        ff = [self.FIRST[A] for A in AS]
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
        return list(ret)

    @timer
    def closure(self, I):
        # print('-----------------------')
        # Parser.printitems(I)
        # print('-----------------------')
        key = Parser.i2s(I)
        if key in self._closure:
            return self._closure[key]
        ret = []
        unvisited = []
        unvisited.extend(I)
        visited_nonterminal = []
        while len(unvisited) > 0:
            item = unvisited.pop()
            ret.append(item)
            if item[-2] == '.':
                continue
            pos = item.index('.')
            t = item[pos+1]
            if t in self.nonterminal:
                # if t in visited_nonterminal:
                #     continue
                # visited_nonterminal.append(t)
                # nt = self.getNT(t)
                nt = self._getNT[t]
                ff = []# first set
                if item[pos+2] == item[-1]:#beta = empty
                    ff.append(item[-1])
                else:
                    ff = self.firsts(item[pos+2:-1])
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
        self._closure[key] = ret
        return ret 
    
    @staticmethod
    def i2s(I):
        s = sorted([''.join(i) for i in I])
        return ''.join(s)

    @timer
    def goto(self, I,X):
        key = Parser.i2s(I)
        trans = {}
        if key in self._goto:
            trans = self._goto[key]
            if X in trans:
                return trans[X]
        else:
            self._goto[key] = trans
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
        if ret == []:
            return []
        ret = self.closure(ret)
        trans[X] = ret
        return ret

    @staticmethod
    def printitems(I,printno=False):
        for i,item in enumerate(I):
            s = ' '.join(item[1:])
            n = '({}) '.format(i)
            s = '{}->{}'.format(item[0],s)
            if printno:
                print(n+s)
            else:
                print(s)

    @timer
    def listItems(self):
        ret = []
        # C = closure([items[0]])
        C = self.closure([self.items[0]+['$']])
        #print(C)
        q = deque()
        q.append(C)
        while True:
            if len(q) <= 0 :
                break
            C = q.popleft()
            ret.append(C)
            for X in self.nonterminal+self.terminal:
                g = self.goto(C, X) # 此处应该可以优化
                if len(g) == 0:
                    continue
                if g in ret:
                    continue
                q.append(g)
        return ret
    
    @timer
    def lalrgen(self,C):
        actions = {}
        gotos = {}
        for state,itemlist in enumerate(C):
            action = {}
            for a in self.terminal+['$']:
                Ij = self.goto(itemlist, a)
                if len(Ij) == 0:
                    '''
                    # 如果没有集合为空，这里要考虑a是不是在itemlist向前看的符号中
                    # 如果不是就直接跳到下一个
                    # 如果是，那么这就会出现收敛
                    '''
                    ps = [item for item in itemlist if item[-2] == '.']
                    if len(ps) == 0:# 如果没有reduce的项目，那肯定直接返回
                        continue
                    lf = [item[-1] for item in ps]
                    if a in lf:
                        # ps = [item[:-2] for item in itemlist if item[-1] == a]
                        ps = [p[:-2] for p in ps if p[-1] == a]
                        indexs = [str(self.productions.index(p)) for p in ps]
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
                    indexs = [str(self.productions.index(p)) for p in ps]
                    r = ''
                    # 这里之所以认为发生了冲突，是因为在我们的items发现了在当前终结符下可以进行规约
                    # 比如 (1)E-> E+E. + (2) E->E.+E x
                    # 或者 (1)if E Stmt . else (2) if E Stmt .else Stmt x
                    # 上面的x代表规约字符
                    # 针对第一种情况，我们采用优先级的方法来处理
                    # 针对第二种情况，我们采用最长匹配原则
                    if len(indexs) > 0:# 发生了reduce/shift conflict
                        r = '||r'+'|'.join(indexs)
                        # 针对 else 这种情况，那么要reduce的产生式，就是shift产生式的开头一部分
                        # 这里假设ps只有一个元素
                        # 第一种 情况处理
                        lps = [p for p in self.productions if len(p) > len(ps[0])]
                        test = [ps[0] == p[:len(ps[0])] for p in lps]
                        # 选择最长匹配
                        if True in test:
                            action[a] = 's'+str(i)
                            continue
                        p = ps[0]
                        p = p[::-1] ## ？
                        prec = 0
                        # 上面谈到了else的shift-reduce冲突问题，采取最长匹配原则
                        # 但是当面对 1+1.+1 这种情况我们是应该规约E->E+E呢，还是
                        # 继续输入后面的token
                        # 这里采用的原则是，如果接下来的操作符优先级大于当前优先级，那么就shift
                        # 否则规约
                        # 例如 1+1.*2 当面对这种*的优先级大于+，所以要shift
                        # 但是这里还有别的情况，比如负数-E
                        # - 在这个地方不是减法的意思，而是负号
                        for t in p:
                            if t in self.terminal:
                                for k,v in self.precs.items():# 如果语法中，对于某条语法定义了一个优先级，那么要先提取这个优先级
                                    if v == p:
                                        t = k
                                prec = self.precedence.get(t,0)
                        cprec = self.precedence.get(a,0)
                        if prec > cprec:
                            action[a] = 'r'+indexs[0]
                            continue
                        if prec == cprec:
                            asso = self.assosiation.get(prec,'L')
                            if asso == 'L':
                                action[a] = 'r'+indexs[0]
                                continue
                    action[a] = 's'+str(i)
            actions[state] = action
            ## 非终结符的情况
            trans = {}
            for A in self.nonterminal:
                Ij = self.goto(itemlist, A)# 这里的goto也是lr的goto
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

    @timer
    def lr2lalr(self, C):
        slr = []
        # for itemlist in C:
        #     slr.append([item[:-1] for item in itemlist])
        for itemlist in C:
            tt = [item[:-1] for item in itemlist]
            ntt = []
            for t in tt:
                if t not in ntt:
                    ntt.append(t)
            slr.append(ntt)
        self.slr = slr
        numslr = []
        for ss in slr:
            vals = sorted([''.join(s) for s in ss])
            numslr.append(vals)
            
        # indexs = {i:slr.index(s) for i,s in enumerate(slr)}
        indexs = {i:numslr.index(s) for i,s in enumerate(numslr)}
        # for i,s in enumerate(slr):

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
    
    def lr2larlrN(self, C):
        slr = []
        for itemlist in C:
            tt = [item[:-1] for item in itemlist]
            ntt = []
            for t in tt:
                if t not in ntt:
                    ntt.append(t)
            slr.append(ntt)
        for ss in slr:
            t = sorted([hash(s) for s in ss])

    '''
    这个版本的分析器能接受语法动作
    '''
    @timer
    def slrparse(self, actions, gotos, tokens, sdmap):
        pos = 0
        states = [0]
        symbol = []
        # tokens.append('$')
        sdmap = {self.productions.index(p):[params,f] for p,params,f in sdmap}
        while True:
            print(states)
            print(symbol)
            if pos == len(tokens):
                break
            print(tokens[pos])
            print('******************')
            current = states[-1]
            token = tokens[pos]
            t = token.kind
            if t in actions[current]:
                action = actions[current][t]
                if action.startswith('s'):#shift
                    s = int(action[1:])
                    symbol.append(token)
                    states.append(s)
                    pos += 1
                elif action.startswith('r'):#reduce
                    l = int(action[1:])
                    pindexs, f = sdmap.get(l)
                    p = self.productions[l]
                    pindexs = [i-1 for i in pindexs]
                    if len(p) >= 1:
                        tp = -len(p)+1
                        params = symbol[tp:]
                        params = [params[i] for i in pindexs]
                        for i in range(len(p)-1):
                            states.pop()
                            symbol.pop()
                        top = states[-1]
                        s = gotos[top][p[0]]
                        states.append(s)
                        symbol.append(f(*params))
                    else:
                        s = gotos[current][p[0]]
                        states.append(s)
                elif action.startswith('acc'):
                    pos += 1
                    print('Accept!')
                    return symbol[-1]
                    break
            else:
                print('ERROR')
                break

    def checkerror(self):
        for state,action in self.actions.items():
            for k,v in action.items():
                if v == 'r':
                    print('Reduce undefined:State:{},Token:{}'.format(state,k))

    @timer
    def generate(self,printInfo=False):
        self.addstart()#这里是LR扩展文法
        # self.productions2items()
        lrC = self.listItems()
        lalrC = self.lr2lalr(lrC)
        C = lalrC#listlalritems()
        self.lalritems = C
        self.C = C
        if printInfo:
            print('---------------------------------')
            for i,c in enumerate(C):
                print(i)
                Parser.printitems(c)
                print('---------------------------------')
            print('*********************************')
            Parser.printitems(self.productions,printno=True)
            print('*********************************')
        
        actions, gotos = self.lalrgen(C)
        self.actions = actions
        self.gotos = gotos
        n = 8
        if printInfo:
            header = ''.join(['{:8}'.format(s) for s in ['state']+self.terminal+['$']+self.nonterminal])
            print(header)
            for (k,v),(k1,v1) in zip(self.actions.items(), self.gotos.items()):
                s = '{:8}'.format(str(k))
                t = ''.join(['{:8}'.format(str(v.get(i,''))) for i in self.terminal+['$']])
                n = ''.join(['{:8}'.format(str(v1.get(i,''))) for i in self.nonterminal])
                p = s+t+n
                sp = ''.join(['-' for i in range(len(p))])
                print(sp)
                print(p)
    
    @staticmethod
    def htmlitems(I):
        ret = []
        pp = '<p>{}</p>'
        aname = '<a name="p{0}">({0})</a>'
        for i,item in enumerate(I):
            s = ' '.join(item[1:])
            # n = '({}) '.format(i)
            n = aname.format(i)
            s = '{}->{}'.format(item[0],s)
            s = s+'<br>'    
            ret.append(n+s)
        return pp.format(''.join(ret))

    def htmlparse(self,filename='temp.html'):
        shtml = []
        pformat = '<p>{}</p>'
        aname = '<a name="{0}">{0}</a><br>'
        for i,c in enumerate(self.C):
            # i = str(i)+'<br>'
            i = aname.format(i)
            h = Parser.htmlitems(c)
            shtml.append(i+h)
        shtml = pformat.format(''.join(shtml))

        phtml = Parser.htmlitems(self.productions)

        def convert(ac):
            shref = '<a href="#{0}">s{0}</a>'
            rhref = '<a href="#p{0}">r{0}</a>'
            ghref = '<a href="#{0}">{0}</a>'
            ac = str(ac)
            if ac == "":
                return ""
            if ac[0] == 's':
                s = ac[1:]
                return shref.format(s)
            elif ac[0] == 'r':
                r = ac[1:]
                return rhref.format(r)
            return ghref.format(ac)

        header = ['state']+self.terminal+['$']+self.nonterminal
        body = []
        formatstr = '<td>{}</td>'
        ahref = '<a href="#{0}">{0}</a>'
        header = ''.join([formatstr.format(i) for i in header])
        for (k,v),(k1,v1) in zip(self.actions.items(), self.gotos.items()):
                # s = [str(k)]
                s = [ahref.format(k)]
                # t = [str(v.get(i,'')) for i in self.terminal+['$']]
                t = [convert(v.get(i,'')) for i in self.terminal+['$']]
                # n = [str(v1.get(i,'')) for i in self.nonterminal]
                n = [convert(v1.get(i,'')) for i in self.nonterminal]
                p = s+t+n
                body.append(''.join([formatstr.format(i) for i in p]))
        formatline = '<tr>{}</tr>'
        formattable = '<table>{}</table>'
        body = ''.join([formatline.format(i) for i in body])
        header = formatline.format(header)
        table = header + body
        table = formattable.format(table)
        content = phtml+shtml+table
        with open(filename,'w') as f:
            f.write(content)
    
    def dumpjson(self, filename='actions.json'):
        with open(filename,'w') as f:
            json.dump([self.actions,self.gotos, self.C, self.productions],f)
    
    def loadjson(self, filename='actions.json'):
        with open(filename,'r') as f:
            self.actions,self.gotos, self.C, self.productions = json.load(f)
        self.actions = {int(k):v for k,v in self.actions.items()}
        self.gotos = {int(k):v for k,v in self.gotos.items()}

    def parse(self, tokens, sdmap):
        return self.slrparse(self.actions, self.gotos, tokens, sdmap)


