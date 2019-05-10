# coding=UTF-8

'''
Created on 2016年7月23日

@author: Administrator
'''

from tuoen.agile.apis.base import AuthorizedApi, NoAuthrizedApi
from tuoen.sys.core.api.request import RequestField
from tuoen.sys.core.api.response import ResponseField
from tuoen.sys.core.field.base import CharField, DictField, IntField, ListField


from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet
from tuoen.sys.core.api.utils import with_metaclass


class Test(NoAuthrizedApi):
    request = with_metaclass(RequestFieldSet)
    request.yrk = RequestField(CharField, desc = "hahahah110", choices = [('a',"account"), ('b',
                                                                                            'bass')])
    request.test = RequestField(CharField, desc = "hahahah110", choices = [('a',1), ('b', 2)])
    request.data = RequestField(DictField, desc = "hahahah110", conf = {
        'c1': CharField(desc="天天"),
        'c2': IntField(desc="数据"),
        'c3': DictField(desc="test", conf = {
            'test': IntField(desc="test")
         }),
    })
    request.data_list = RequestField(ListField, desc ='data_list110', fmt = IntField(desc = 'char list 2'))
    request.data_list_1 = RequestField(ListField, desc ='data_list110', fmt = DictField(desc = "hahahah110", conf = {
        'c1': CharField(desc="天天"),
        'c2': IntField(desc="数据")
    }))


    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc ='data_list110', fmt = IntField(desc = 'char list 2'))
    response.data2_list = ResponseField(ListField, desc ='data_list110', fmt = DictField(desc = "", conf ={
        'c1':IntField(desc = 'char list 2'),
        'c2':IntField(desc = 'char list 2')
    }))

    def execute(self, request):
        from tuoen.sys.log.base import logger
        logger.info(request.yrk)
        print(request.yrk)
        print(request.yrk___desc)
        print(request.data)
        print(request.data.c2)
        print(request.data_list)
        print(request.data_list_1)
        print(request.data_list_1[1].c2)
        data_list = ['1','2','3']
        data2_list = [
            {
                'c1':'123',
                'c2':'234',
            },
            {
                'c1':'51231',
                'c2':13412.12,
            }
        ]
        return data_list, data2_list

    def fill(self, response, data_list, data2_list):
        response.data_list = data_list
        response.data2_list = data2_list
        print(response.data_list)
        print(response.data2_list)
        print(response.data2_list[0].c1)
        return response


class Filter(NoAuthrizedApi):
    request = with_metaclass(RequestFieldSet)
    request.data = RequestField(DictField, desc = "hahahah110", conf = {
        'c1': CharField(desc="天天"),
        'c2': IntField(desc="数据"),
        'c3': CharField(desc="天天"),
    })

    response = with_metaclass(ResponseFieldSet)

    def execute(self, request):
        print(request.data)
        return "hahahah"

    def fill(self, response, flag):
        return response
