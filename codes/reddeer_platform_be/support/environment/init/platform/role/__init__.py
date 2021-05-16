# coding=UTF-8

from support.common.maker import BaseLoader


class RoleLoader(BaseLoader):

    def generate(self):
        return [
            {
                'name': '超级管理员',
                'describe': "超级管理员",
            }
        ]
