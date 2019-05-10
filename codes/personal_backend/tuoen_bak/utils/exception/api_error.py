# coding=UTF-8

'''
Created on 2016-7-4

@author: YRK
'''

import itertools

from tuoen.utils.common.single import Single
from tuoen.utils.exception.base import BaseError
from tuoen.utils.exception.error_code import SYS_ERROR_CODES, SERVER_ERROR_CODES

class APIBaseError(BaseError):

    def __str__(self):
        return "【{code}】{desc}".format(code = self.code, desc = self.desc)

    def __call__(self):
        return {"code":self.code, "msg":self.desc % self.args}
#         return {"error_respose":{"code":self.code, "msg":self.desc % self.args}}


def bind_error(**config):

    class APIError(APIBaseError):
        code = config.get('code', 0)
        desc = config.get('desc', "")

        def __init__(self, *args):
            self.args = args

    return APIError

class ApiErrorManager(Single):

    def __init__(self):
        self._error = {}
        self._loads()

    def _loads(self):
        for code , desc  in itertools.chain(SYS_ERROR_CODES, SERVER_ERROR_CODES):
            api_error = bind_error(code = code, desc = desc)
            self.regiter(api_error)

    def regiter(self, api_error):
        assert issubclass(api_error, APIBaseError)

        if api_error.code in self._error:
            raise Exception("api_error {code} code have registed, error obj = {error}"\
                            .format(code = api_error.code, error = api_error))

        self._error[api_error.code] = api_error

    def get_error(self, code):
        return self._error[code]

error_manager = ApiErrorManager()

if __name__ == "__main__":
    for api_error in error_manager._error.values():
        print(api_error)