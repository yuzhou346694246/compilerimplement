# 提取非终结符和终结符

# productions = [
#     ['Program','Block'],
#     ['Block','{','Decls','Stmts','}'],
#     ['Decls','Decls','Decl'],
#     ['Decls'],
#     ['Decl','Type','id'],
#     ['Type','Type','[','num',']'],
#     ['Type','int'],
#     ['Type','string'],
#     ['Type','float'],
#     ['Stmts','Stmts','Stmt'],
#     ['Stmts'],
#     ['Stmt','Loc','=','Exp'],
#     ['Stmt','if','(','Exp',')','Stmt'],
#     ['Stmt','if','(','Exp',')','Stmt','else','Stmt'],
#     ['Stmt','while','(','Exp',')','Stmt'],
#     ['Stmt','do','Stmt','while','(','Exp',')'],
#     ['Stmt','break'],
#     ['Stmt','Block'],
#     ['Loc','Loc','[','Exp',']'],
#     ['Loc','id'],
#     ['Exp','Exp','||','Exp'],
#     ['Exp','Exp','&&','Exp'],
#     ['Exp','Exp','==','Exp'],
#     ['Exp','Exp','!=','Exp'],
#     ['Exp','Exp','>=','Exp'],
#     ['Exp','Exp','<=','Exp'],
#     ['Exp','Exp','>','Exp'],
#     ['Exp','Exp','<','Exp'],
#     ['Exp','Exp','+','Exp'],
#     ['Exp','Exp','-','Exp'],
#     ['Exp','Exp','*','Exp'],
#     ['Exp','Exp','/','Exp'],
#     ['Exp','-','Exp'],
#     ['Exp','!','Exp'],
#     ['Exp','Loc'],
#     ['Exp','num'],
#     ['Exp','true'],
#     ['Exp','false'],
#     ['Exp','real']
# ]
# productions = [
#     ['Program','program','id',';','Block'],
#     ['Block','VarDeclPart','ProcDeclPart','StatPart'],
#     ['VarDeclPart'],
#     ['VarDeclPart','VarDeclPart','VarDecl'],
#     ['VarDecl','var','Decl'],
#     ['Decl','Ids',':','Type'],
#     ['Ids','Ids',',','id'],
#     ['Ids','id'],
#     ['Type','SimpleType'],
#     ['Type','ArrayType'],
#     ['SimpleType','int'],
#     ['ArrayType','array','[','IndexRange',']'],
#     ['IndexRange','num','..','num'],# num 整数
#     ['ProcDeclPart'],
#     ['ProcDeclPart','ProcDecl'],
#     ['ProcDecl','procedure','id',';','Block'],
#     ['StatPart','CompState'],
#     ['CompState','begin','Stats','end'],
#     ['Stats','Stats',';','Stat'],
#     ['Stats','Stat'],
#     ['Stat','SimpleStat'],
#     ['Stat','StructStat'],
#     ['SimpleStat','AssignStat'],
#     ['SimpleStat','ProcStat'],
#     ['SimpleStat','ReadStat'],
#     ['SimpleStat','WriteStat'],
#     ['AssignStat','id',':=','Exp'],
#     ['ProcStat','ProcId'],
#     ['ProcId','id'],
#     ['ReadStat','read','(','Ids',')'],
#     ['WriteStat','write','(','OutputValues',')'],
#     ['OutputValues','Exp'],
#     ['OutputValues','OutputValues',',','Exp'],
#     ['StructStat','CompStat'],
#     ['StructStat','IfStat'],
#     ['StructStat','WhileStat'],
#     ['IfStat','if','Exp','then','Stat'],
#     ['IfStat','if','Exp','then','Stat','else','Stat'],
#     ['WhileStat','while','Exp','do','Stat'],
#     ['Exp','SimpleExp'],
#     ['Exp','SimpleExp','ReOp','SimpleExp'],
#     ['SimpleExp','Sign','Term'],
#     ['SimpleExp','Sign','Term','AddOp','SimpleExp'],
#     ['Term','Factor'],
#     ['Term','Factor','MulOp','Term'],
#     ['Factor','Variable'],
#     ['Factor','Const'],
#     ['Factor','(','Exp',')'],
#     ['Factor','not','Factor'],
#     ['ReOp','='],
#     ['ReOp','<>'],
#     ['ReOp','>'],
#     ['ReOp','>='],
#     ['ReOp','<'],
#     ['ReOp','<='],
#     ['Sign'],
#     ['Sign','+'],
#     ['Sign','-'],
#     ['AddOp','+'],
#     ['AddOp','-'],
#     ['AddOp','or'],
#     ['MulOp','*'],
#     ['MulOp','/'],
#     ['MulOp','and'],
#     ['Variable','id'],
#     ['Variable','IndexVar'],
#     ['IndexVar','id','[','Exp',']'],
#     ['Const','intconst'],
#     ['Const','charconst'],
#     ['Const','ConstId'],
#     ['ConstId','id']
# ]
productions = [
    ['Program','MainClass','ClassDeclarations'],
    ['ClassDeclarations'],
    ['ClassDeclarations','ClassDeclarations','ClassDeclaration'],
    ['ClassDeclarations','ClassDeclaration'],
    ['MainClass','class','id','{','public','static','void','main','(','String','[',']','id',')','{','Statement','}','}'],
    ['ClassDeclaration','class','id','Extend','{','VarDeclarations','MethodDeclarations','}'],
    ['VarDeclarations'],
    ['VarDeclarations','VarDeclarations','VarDeclaration'],
    ['VarDeclarations','VarDeclaration'],
    ['VarDeclaration','Type','id',';'],
    ['Extend'],
    ['Extend','extends','id'],
    ['MethodDeclarations'],
    ['MethodDeclarations','MethodDeclarations','MethodDeclaration'],
    ['MethodDeclarations','MethodDeclaration'],
    ['MethodDeclaration','public','Type','id','(','ParamsDefinition',')','{','VarDeclarations','Statement','}'],
    ['ParamsDefinition','ParamDefinition'],
    ['ParamsDefinition'],
    ['ParamsDefinitions','ParamsDefinitions','ParamDefinition'],
    ['ParamDefinition','Type','id'],
    ['Type','int','[',']'],
    ['Type','boolean'],
    ['Type','int'],
    ['Type','id'],
    ['Statement','{','Statements','}'],
    ['Statement','if','(','Expression',')','Statement','else','Statement'],
    ['Statement','while','(','Expression',')','Statement'],
    ['Statement','System.out.println','(','Expression',')'],
    ['Statement','id','=','Expression',';'],
    ['Statement','id','[','Expression',']','=','Expression',';'],
    ['Statements'],
    ['Statements','Statements','Statement'],
    ['Statements','Statement'],
    # ['Expression','Expression','&&','Expression'],
    # ['Expression','Expression','||','Expression'],
    # ['Expression','Expression','<','Expression'],
    # ['Expression','Expression','>','Expression'],
    # ['Expression','Expression','<=','Expression'],
    # ['Expression','Expression','>=','Expression'],
    # ['Expression','Expression','==','Expression'],
    # ['Expression','Expression','!=','Expression'],
    # ['Expression','Expression','[','Expression',']'],
    # ['Expression','Expression','+','Expression'],
    # ['Expression','Expression','-','Expression'],
    # ['Expression','Expression','*','Expression'],
    # ['Expression','Expression','/','Expression'],
    # ['Expression','Expression','.','length'],
    # ['Expression','Expression','.','id','(','Params',')'],
    # ['Params'],
    # ['Params','Params',',','Expression'],
    # ['Params','Expression'],
    ['Expression','num'],
    # ['Expression','true'],
    # ['Expression','false'],
    # ['Expression','id'],
    # ['Expression','this'],
    # ['Expression','new','int','[','Expression',']'],
    # ['Expression','new','id','(',')'],
    # ['Expression','!','Expression'],
    # ['Expression','-','Expression'],
    # ['Expression','(','Expression',')']
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
print(nn)
print(tt)
# for n in nn:
#     if n not in nonterminal:
#         print(n)
# for t in tt:
#     if t not in terminal:
#         print(t)

