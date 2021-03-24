# -*- coding: utf-8 -*-

# ===================================
# file_name     : samples.py
# python_version: python 3.7.4
# file_author   : Johnathan.Strong
# create_time   : 2020/12/19 20:23
# ide_name      : PyCharm
# project_name  : 4U
# ===================================


class Person:
    def __init__(self, name, age):
        if self.is_name_valid(name):
            self.name = name
        else:
            raise Exception('invalid name')
        if self.is_age_valid(age):
            self.age = age
        else:
            raise Exception('invalid age')

    @staticmethod
    def is_name_valid(name: str) -> bool:
        if not isinstance(name, str):
            return False
        if name.isalpha():
            return True
        return False

    @staticmethod
    def is_age_valid(age: int) -> bool:
        if not isinstance(age, int):
            return False
        if 0 <= age <= 120:
            return True
        return False


aston = Person('aston-', 130)
