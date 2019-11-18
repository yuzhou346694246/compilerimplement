# 提取非终结符和终结符

productions = [
    ['Program','Block'],
    ['Block','{','Decls','Stmts','}'],
    ['Decls','Decls','Decl'],
    ['Decls'],
    ['Decl','Type','id'],
    ['Type','Type','[','num',']'],
    ['Type','int'],
    ['Type','string'],
    ['Type','float'],
    ['Stmts','Stmts','Stmt'],
    ['Stmts'],
    ['Stmt','Loc','=','Exp'],
    ['Stmt','if','(','Exp',')','Stmt'],
    ['Stmt','if','(','Exp',')','Stmt','else','Stmt'],
    ['Stmt','while','(','Exp',')','Stmt'],
    ['Stmt','do','Stmt','while','(','Exp',')'],
    ['Stmt','break'],
    ['Stmt','Block'],
    ['Loc','Loc','[','Exp',']'],
    ['Loc','id'],
    ['Exp','Exp','||','Exp'],
    ['Exp','Exp','&&','Exp'],
    ['Exp','Exp','==','Exp'],
    ['Exp','Exp','!=','Exp'],
    ['Exp','Exp','>=','Exp'],
    ['Exp','Exp','<=','Exp'],
    ['Exp','Exp','>','Exp'],
    ['Exp','Exp','<','Exp'],
    ['Exp','Exp','+','Exp'],
    ['Exp','Exp','-','Exp'],
    ['Exp','Exp','*','Exp'],
    ['Exp','Exp','/','Exp'],
    ['Exp','-','Exp'],
    ['Exp','!','Exp'],
    ['Exp','Loc'],
    ['Exp','num'],
    ['Exp','true'],
    ['Exp','false'],
    ['Exp','real']
]

terminal = [
    '{','}','[',']','id','int','string','float','num','=',
    '||','&&','==','!=','>=','<=','>','<','+','-','*','/',
    '!','true','false','real','do','else','while','break',
    'if','(',')'
]

nonterminal =[
    'Program','Block','Decls','Stmts','Stmt','Decl','Type',
    'Loc','Exp'
]

def p2TAndN():
    nont = []
    tt = []
    for p in productions:
        if p[0][0].isupper() :
            if p[0] not in nont:
                nont.append(p[0])
        
        for t in p[1:]:
            if t.islower():
                if t not in tt:
                    tt.append(t)

            if not t.isalnum():
                if t not in tt:
                    tt.append(t)
    return nont,tt

nn,tt = p2TAndN()
for n in nn:
    if n not in nonterminal:
        print(n)
for t in tt:
    if t not in terminal:
        print(t)

