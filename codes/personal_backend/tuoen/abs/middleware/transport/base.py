# coding=UTF-8

from tuoen.sys.utils.common.dictwrapper import DictWrapper


class BaseTransport(object):

    def pack(self, **kwargs):
        return DictWrapper(kwargs)

    def parse(self, result):
        return DictWrapper(result)

    def send(self, request):
        raise NotImplementedError('Please imporlement this interface in subclass')

    def connect(self, request, try_count = 3):
        error = None
        for index in range(try_count):
            try:
                return self.send(request)
            except Exception as e:
                error = e
                print("try to connect, {} times".format(index + 1))

        raise Exception("connect error, e = {}".format(error))

    def run(self, *args, **kwargs):
        request = self.pack(*args, **kwargs)
        result = self.connect(request)
        response = self.parse(result)
        return response


class HttpTransport(BaseTransport):
    pass
