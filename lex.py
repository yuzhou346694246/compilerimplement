## 词法分析

def lex(line):
    pos = 0
    length = len(line)
    while pos < length:
        if line[pos].isdigit():
            begin = pos
            while True:
                pos += 1
                if pos >= length:
                    yield line[begin:pos]
                    return
                if not line[pos].isdigit():
                    yield line[begin:pos]
                    break
        if line[pos] == '+':
            pos=pos+1
            yield '+'
        if line[pos] == '-':
            pos=pos+1
            yield '-'
        if line[pos] == '*':
            pos=pos+1
            yield '*'
        if line[pos] == '/':
            pos=pos+1
            yield '/'

print(list(lex('1+1')))