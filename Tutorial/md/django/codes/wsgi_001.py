import re
from wsgiref.simple_server import make_server


# application
def application(environ, start_response):
    start_response('200 ok', [('Content-Type', 'text/html')])
    # if 'location' in environ.get('PATH_INFO', ''):
    #     return [b'I am in china']
    # if 'say' in environ.get('PATH_INFO', ''):
    #     return [b'hello world']
    # else:
    #     return [b'welcome to my index page']
    [print(k, ':', v) for k, v in environ.items()]
    return [b'test']


# WSGI server
# with make_server('', 8080, application) as httpd:
#     sa = httpd.socket.getsockname()
#     print("Serving HTTP on", sa[0], "port", sa[1], "...")
#     import webbrowser
#
#     webbrowser.open('http://localhost:8080')
#     httpd.serve_forever()
# httpd.handle_request()  # serve one request, then exit


# httpd = make_server('', 8000, application)
# print('Now, server is running on port 8000')
# httpd.serve_forever()
from django.utils.deprecation import MiddlewareMixin
from django.db.models.signals import pre_save


def test():
    def _decorator(func):
        print('inner')
        # func()
        return func

    print('outter')
    return _decorator


def time_cost(func):
    def _wrapper_time_cost(*args, **kwargs):
        print('no execute')
        func(*args, **kwargs)
        return 3

    return _wrapper_time_cost


@test()
def fuck():
    print('fuck')


# fuck()

print('-' * 100)

import weakref


class Container:
    def __init__(self):
        self.dict = {}

    def add(self, obj):
        # 维护弱引用, 实现gc回调
        self.dict[weakref.ref(obj, self.gc)] = id(obj)

    def gc(self, ref_obj):
        obj_id = self.dict[ref_obj]
        print("移除object id:", obj_id, "weakref对象:", ref_obj, "指向的对象:", ref_obj())
        del self.dict[ref_obj]


class SomeCls:
    pass


# 容器
# container = Container()
# # 任意对象
# obj1 = SomeCls()
# obj2 = SomeCls()
# # 加入容器
# container.add(obj1)
# container.add(obj2)
# # 释放对象
# del obj2


from django.dispatch.dispatcher import receiver
from signal001 import shut_down_alarm

# shut_down_alarm = Signal(providing_args=('shutting down', 'shut_down_alarm'))

print('test--------------->')


@receiver(shut_down_alarm, sender='fucker')
def call_back(sender, *args, **kwargs):
    print('shutting ===========>')
    print(args)
    print(kwargs)
