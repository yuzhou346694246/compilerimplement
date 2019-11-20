from functools import wraps

def syntaxmap(grammar, params):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwds):
            return f(*args, **kwds)
        return wrapper
    return 

@syntaxmap(['E','+','E'],[0,1,2])
def binaryoperator(left,op,right):
    pass