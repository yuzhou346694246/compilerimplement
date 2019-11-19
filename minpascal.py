from lalrparse import Parser

productions = [
    ['Program','program','id',';','Block'],
    ['Block','VarDeclPart','ProcDeclPart','StatPart'],
    ['VarDeclPart'],
    ['VarDeclPart','VarDeclPart','VarDecl'],
    ['VarDecl','var','Decl'],
    ['Decl','Ids',':','Type'],
    ['Ids','Ids',',','id'],
    ['Ids','id'],
    ['Type','SimpleType'],
    ['Type','ArrayType'],
    ['SimpleType','int'],
    ['ArrayType','array','[','IndexRange',']'],
    ['IndexRange','num','..','num'],# num 整数
    ['ProcDeclPart'],
    ['ProcDeclPart','ProcDecl'],
    ['ProcDecl','procedure','id',';','Block'],
    ['StatPart','CompState'],
    ['CompState','begin','Stats','end'],
    ['Stats','Stats',';','Stat'],
    ['Stats','Stat'],
    ['Stat','SimpleStat'],
    ['Stat','StructStat'],
    ['SimpleStat','AssignStat'],
    ['SimpleStat','ProcStat'],
    ['SimpleStat','ReadStat'],
    ['SimpleStat','WriteStat'],
    ['AssignStat','id',':=','Exp'],
    ['ProcStat','ProcId'],
    ['ProcId','id'],
    ['ReadStat','read','(','Ids',')'],
    ['WriteStat','write','(','OutputValues',')'],
    ['OutputValues','Exp'],
    ['OutputValues','OutputValues',',','Exp'],
    ['StructStat','CompStat'],
    ['StructStat','IfStat'],
    ['StructStat','WhileStat'],
    ['IfStat','if','Exp','then','Stat'],
    ['IfStat','if','Exp','then','Stat','else','Stat'],
    ['WhileStat','while','Exp','do','Stat'],
    ['Exp','SimpleExp'],
    ['Exp','SimpleExp','ReOp','SimpleExp'],
    ['SimpleExp','Sign','Term'],
    ['SimpleExp','Sign','Term','AddOp','SimpleExp'],
    ['Term','Factor'],
    ['Term','Factor','MulOp','Term'],
    ['Factor','Variable'],
    ['Factor','Const'],
    ['Factor','(','Exp',')'],
    ['Factor','not','Factor'],
    ['ReOp','='],
    ['ReOp','<>'],
    ['ReOp','>'],
    ['ReOp','>='],
    ['ReOp','<'],
    ['ReOp','<='],
    ['Sign'],
    ['Sign','+'],
    ['Sign','-'],
    ['AddOp','+'],
    ['AddOp','-'],
    ['AddOp','or'],
    ['MulOp','*'],
    ['MulOp','/'],
    ['MulOp','and'],
    ['Variable','id'],
    ['Variable','IndexVar'],
    ['IndexVar','id','[','Exp',']'],
    ['Const','intconst'],
    ['Const','charconst'],
    ['Const','ConstId'],
    ['ConstId','id']
]

precs = {
    # 'UMINUS':['E','-','E']
}

terminal = ['program', 'id', ';', 'var', ':', ',', 'int', 'array', '[', ']', 'num', 
    '..', 'procedure', 'begin', 'end', ':=', 'read', '(', ')', 'write', 'if', 'then', 
    'else', 'while', 'do', 'not', '=', '<>', '>', '>=', '<', '<=', '+', '-', 'or', '*', 
    '/', 'and', 'intconst', 'charconst']

nonterminal = ['Program', 'Block', 'VarDeclPart', 'VarDecl', 'Decl', 'Ids', 'Type', 
    'SimpleType', 'ArrayType', 'IndexRange', 'ProcDeclPart', 'ProcDecl', 'StatPart', 
    'CompState', 'Stats', 'Stat', 'SimpleStat', 'AssignStat', 'ProcStat', 'ProcId', 
    'ReadStat', 'WriteStat', 'OutputValues', 'StructStat', 'IfStat', 'WhileStat', 
    'Exp', 'SimpleExp', 'Term', 'Factor', 'ReOp', 'Sign', 'AddOp', 'MulOp', 'Variable', 
    'IndexVar', 'Const', 'ConstId']
precedence = {# 优先级 
    # '||':7,
    # '&&':7,
    # '!':8,
    # '>=':9,
    # '>':9,
    # '<':9,
    # '<=':9,
    # '==':9,
    # '!=':9,
    # '+':10,
    # '-':10,
    # '*':11,
    # '/':11,
    # 'UMINUS':15
}

assosiation = {# 结合律
    # '+':'L',
    # '-':'L',
    # '*':'L',
    # '/':'L',
    # 'UMINUS':'R'
}


parser = Parser(productions, precs, terminal, nonterminal, precedence, assosiation)
parser.generate(printInfo=True)