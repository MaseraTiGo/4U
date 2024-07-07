import builtins
import dis
from pprint import pprint

import inspect

y = 2


def print_frame_info():
    # 获取当前帧对象
    frame = inspect.currentframe()
    x = 1
    try:
        # 打印局部变量
        pprint(frame.f_locals)

        # 打印全局变量
        print("全局变量：", frame.f_globals)

        # 打印内置变量
        print("内置变量：", frame.f_builtins)

        # 打印值栈（假设值栈信息不可直接访问，这里模拟一个）
        print("值栈：", frame.f_locals.get('value_stack', '值栈信息不可用'))

        # 打印块栈（假设块栈信息不可直接访问，这里模拟一个）
        print("块栈：", frame.f_locals.get('block_stack', '块栈信息不可用'))
    finally:
        # 确保删除帧对象引用，以避免引用循环
        del frame


def example_function(x, y):
    value_stack = [10, 20, 30]  # 模拟值栈
    block_stack = ['loop', 'try-except']  # 模拟块栈

    z = x + y
    print_frame_info()  # 打印帧信息
    return z


result = example_function(5, 7)
print("结果：", result)

dis.dis(print_frame_info)
