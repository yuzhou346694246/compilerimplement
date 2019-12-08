from enum import Enum
class Token:
    def __init__(self, kind, pos, text, val=None, lineno=0):
        self.kind = kind
        self.pos = pos
        self.text = text
        self.val = val
        self.lineno = lineno

    def __str__(self):
        return 'tokenKind:{},pos:{},text:{},val:{}, lineno:{}'.format(self.kind, self.pos, self.text, self.val, self.lineno)
# class TokenType(Enum):

class Lexer:
    def __init__(self, content):
        self.content = content
    
    def lex(self):
        pos = 0
        line = self.content
        length = len(line)
        while pos < length:
            if line[pos].isdigit():
                begin = pos
                while True:
                    pos += 1
                    if pos >= length:
                        text = line[begin:pos]
                        val = int(text)
                        yield Token('num',begin,text,val)
                        yield Token('$',-1,'')
                        return
                    if not line[pos].isdigit():
                        text = line[begin:pos]
                        val = int(text)
                        yield Token('num',begin,text,val)
                        break
            if line[pos] == '+':
                yield Token('+',pos,'+')
                pos=pos+1
            if line[pos] == '-':
                yield Token('-',pos,'-')
                pos=pos+1
            if line[pos] == '*':
                yield Token('*',pos,'*')
                pos=pos+1
            if line[pos] == '/':
                yield '/'
                yield Token('/',pos,'/')
                pos=pos+1
            if pos >= length:
                yield Token('$',-1,'')
                return


