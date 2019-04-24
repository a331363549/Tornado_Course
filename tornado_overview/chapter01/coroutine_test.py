# 回调过深造成代码维护很难
# 栈撕裂造成异常无法向上抛出
# 协程可以被并切换到其他协程运行的函数

from tornado.gen import coroutine


async def yield_test():
    yield 1
    yield 2
    yield 3


async def yield_test2():
    yield 1
    yield 2
    yield 3


async def main():
    result = await yield_test()
    result = await yield_test2()


async def main2():
    await yield_test()
