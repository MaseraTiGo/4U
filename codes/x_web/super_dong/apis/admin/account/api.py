# -*- coding: utf-8 -*-
# @File    : api
# @Project : djangoProject
# @Time    : 2022/10/12 11:09
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""

from super_dong.frame.core.api import AuthApi
from super_dong.frame.core.data_field import CharField, IntField, ListField, \
    DictField, DateTimeField, AlmightyField
from super_dong.frame.core.data_field.data_type import RequestData, \
    access_control, \
    ResponseData


@access_control(access_method=['POST'])
class Login(AuthApi):
    @access_control(access_method=['GET'])
    class Login(RequestData):
        name = CharField(verbose='fucking name', max_length=-1,
                         choices=[('apple', 'apple a'), ('banana', 'banana a')])
        age = IntField(verbose='fucking age', max_value=11)
        hobbits = ListField(verbose='bob',
                            item=CharField(verbose='items', max_length=-1))
        crypto = DictField(verbose='crypto', strict=False, members={
            'name': CharField(verbose='name', max_length=-1),
            'ai': ListField(verbose='ai',
                            item=CharField(verbose='ai', max_length=-1))
        }
                           )
        mix = DictField(verbose='mixing',
                        members={
                            'fuck': ListField(verbose='fuck',
                                              item=DictField(verbose='item',
                                                             members={
                                                                 'you': CharField(
                                                                     verbose='you',
                                                                     max_length=1)
                                                             }
                                                             )
                                              )
                        }
                        )

    class InfoDante(RequestData):
        goods = ListField(verbose='goods',
                          item=CharField(verbose='item', max_length=-1))
        sale_date = DateTimeField(verbose='datetime')

    class Almighty(RequestData):
        almighty = AlmightyField(verbose='almighty test')

    class Result(ResponseData):
        objects = CharField(verbose='objects', max_length=-1)
        score = IntField(verbose='score')
        # create_time = DateTimeField(verbose='create time')

    @classmethod
    def get_desc(cls):
        pass

    @classmethod
    def get_author(cls):
        pass

    @classmethod
    def get_history(cls):
        pass

    @classmethod
    def get_unique_num(cls):
        pass

    def execute(self):
        return {
            'objects': 'math',
            'score': 99
        }

    def tidy(self, rets):
        return {
            'Result': rets
        }
