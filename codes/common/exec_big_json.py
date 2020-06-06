# -*- coding: utf-8 -*-
# file_name       : exec_big_json.py
# file_func       :
# file_author     : 'Johnathan.Wick'
# file_create_date: 2020/6/5 20:35

import json

import ijson
from memory_profiler import profile

src_data = {
    "data_key0": {
        "file_name": "fuck_you",
        "s3_key": 'I do not know',
        "valid_lines": [1, 2, 3, 4, 5]
    },
    "ct-20200606": [1, 2, 3, 4, 5, 6, 7, 8],
    "data_key1": {
        "file_name": "fuck_you",
        "s3_key": 'I do not know',
        "valid_lines": [1, 2, 3, 4, 5]
    },
}
origin_path = r"E:\temp\src_data.json"


def write_json():
    with open(origin_path, 'w') as f:
        json.dump(src_data, f)


class Middleware(object):
    __slots__ = ('_src_obj', '_src_len')

    def __init__(self, src_obj, src_len):
        self._src_obj = src_obj
        self._src_len = src_len

    def get(self, value):
        self._src_obj.get(value)

    def __len__(self):
        return self._src_len

    def __iter__(self):
        return self._src_obj


class ReadJson(object):
    def __init__(self, fp, prefix=''):
        self._fp = fp
        self._prefix = prefix
        self._len = 0

    def get(self, key):
        if 'data_key' in key and not self._prefix:
            return ReadJson(self._fp, key)
        if self._prefix:
            if key not in ['valid_lines']:
                res = ijson.items(open(self._fp, encoding='utf-8', mode='r'), '%s.%s' % (self._prefix, key))
                for item in res:
                    return item
            else:
                res = ijson.items(open(self._fp, encoding='utf-8', mode='r'), '%s.%s.item' % (self._prefix, key))
                for _ in res:
                    self._len += 1
                res = ijson.items(open(self._fp, encoding='utf-8', mode='r'), '%s.%s.item' % (self._prefix, key))
                return Middleware(res, self._len)
        if not self._prefix and 'data_key' not in key:
            res = ijson.items(open(self._fp, encoding='utf-8', mode='r'), '%s.item' % key)
            for _ in res:
                self._len += 1
            res = ijson.items(open(self._fp, encoding='utf-8', mode='r'), '%s.item' % key)
            return Middleware(res, self._len)


def read_json(fp):
    return ReadJson(fp)


@profile
def do_some():
    write_json()
    result = read_json(origin_path)
    log = result.get('data_key1')
    file_name = log.get('file_name')
    s3_key = log.get('s3_key')
    var_lines = log.get('valid_lines')
    print(len(var_lines))
    for item in var_lines:
        print(item)
    print(file_name)
    print(s3_key)
    lines = result.get('ct-20200606')
    print(len(lines))
    for item in lines:
        print(item)


do_some()
