import sys
from os import path
sys.path.append(path.join(path.dirname(__file__), '..'))
from lalrparse import Parser

#http://www.cs.tufts.edu/~sguyer/classes/comp181-2006/minijava.html
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
    ['Expression','Expression','&&','Expression'],
    ['Expression','Expression','||','Expression'],
    ['Expression','Expression','<','Expression'],
    ['Expression','Expression','>','Expression'],
    ['Expression','Expression','<=','Expression'],
    ['Expression','Expression','>=','Expression'],
    ['Expression','Expression','==','Expression'],
    ['Expression','Expression','!=','Expression'],
    ['Expression','Expression','[','Expression',']'],
    ['Expression','Expression','+','Expression'],
    ['Expression','Expression','-','Expression'],
    ['Expression','Expression','*','Expression'],
    ['Expression','Expression','/','Expression'],
    ['Expression','Expression','.','length'],
    ['Expression','Expression','.','id','(','Params',')'],
    ['Params'],
    ['Params','Params',',','Expression'],
    ['Params','Expression'],
    ['Expression','num'],
    ['Expression','true'],
    ['Expression','false'],
    ['Expression','id'],
    ['Expression','this'],
    ['Expression','new','int','[','Expression',']'],
    ['Expression','new','id','(',')'],
    ['Expression','!','Expression'],
    ['Expression','-','Expression'],
    ['Expression','(','Expression',')']
]
terminal = ['class', 'id', '{', 'public', 'static', 'void', 'main', '(', '[', ']', ')', '}', ';', 
            'extends', 'int', 'boolean', 'if', 'else', 'while', '=', 'num','System.out.println']
nonterminal = ['Program', 'ClassDeclarations', 'MainClass', 'ClassDeclaration', 
                'VarDeclarations', 'VarDeclaration', 'Extend', 'MethodDeclarations', 
                'MethodDeclaration', 'ParamsDefinition', 'ParamsDefinitions', 
                'ParamDefinition', 'Type', 'Statement', 'Statements', 'Expression', 'Params']

precedence = {# 优先级 
    '||':7,
    '&&':7,
    '!':8,
    '>=':9,
    '>':9,
    '<':9,
    '<=':9,
    '==':9,
    '!=':9,
    '+':10,
    '-':10,
    '*':11,
    '/':11,
    'UMINUS':15
}

assosiation = {# 结合律
    '+':'L',
    '-':'L',
    '*':'L',
    '/':'L',
    'UMINUS':'R',
    '!':'R'
}
precs = {
    'UMINUS':['Expression','-','Expression'],
}

parser = Parser(productions,  terminal, nonterminal,precs, precedence, assosiation)
parser.generate()
# parser.generate(printInfo=False)
tokens = ['id','>','id']
parser.checkerror()
# parser.parse(tokens)
'''
function hello()
    if 
'''
parser.htmlparse()