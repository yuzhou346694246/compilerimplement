from functools import wraps
from datetime import datetime
calls = {}
'''
这个代码实现了对函数调用次数和运行时间的统计
'''
def timer(func):
    @wraps(func)
    def decorator(*args,**kwargs):
        name = func.__name__
        if name not in calls:
            calls[name] = {'callno':0,'total_time':0}
        start = datetime.now()
        ret = func(*args,**kwargs)
        end = datetime.now()
        delta = end - start
        # print(delta.total_seconds())
        calls[name]['callno'] += 1
        calls[name]['total_time'] += delta.total_seconds()
        return ret
    return decorator

@timer
def test():
    for i in range(100000000):
        a = 1

# test()
# class TestClass:
#     def __init__(self):
#         pass
#     @timer
#     def calc(self):
#         for i in range(10000000):
#             a = 1

# tc = TestClass()
# tc.calc()
# print(calls)