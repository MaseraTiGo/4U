# -*- coding: utf-8 -*-

# ===================================
# file_name     : __init__.py
# python_version: python 3.7.4
# file_author   : Johnathan.Strong
# create_time   : 2020/12/19 19:50
# ide_name      : PyCharm
# project_name  : 4U
# ===================================


import logging

logging.basicConfig(level=logging.INFO)


class LoggedAccess:

    def __set_name__(self, owner, name):
        logging.info(f'dong --------------> I am being accessed: {owner}:{name}')
        self.public_name = name
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        value = getattr(obj, self.private_name)
        logging.info('Accessing %r giving %r', self.public_name, value)
        return value

    def __set__(self, obj, value):
        logging.info('Updating %r to %r', self.public_name, value)
        setattr(obj, self.private_name, value)


class Person:
    name = LoggedAccess()  # First descriptor instance
    age = LoggedAccess()  # Second descriptor instance

    def __init__(self, name, age):
        self.name = name  # Calls the first descriptor
        self.age = age  # Calls the second descriptor

    def birthday(self):
        self.age += 1


john = Person('john', 29)
print(john.name)
