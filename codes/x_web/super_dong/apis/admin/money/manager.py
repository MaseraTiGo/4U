# -*- coding: utf-8 -*-
# @File    : manager
# @Project : djangoProject
# @Time    : 2022/12/9 18:05
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
from datetime import datetime, timedelta

from django.forms import model_to_dict

from super_dong.frame.contri.manager import BaseManager
from super_dong.frame.core.exception import BusinessLogicError
from super_dong.model_store.models import MyShit


class MyShitManager(BaseManager):
    MODEL = MyShit
    InvestType_Choices = MODEL.InvestType.choices
    Status_Choices = MODEL.InvestStatus.choices
    App_Choices = MODEL.App.choices

    @classmethod
    def create(cls, **data):
        total = data['amount']

    @classmethod
    def quick_create(cls, **data):
        date = data.get('record_datetime')
        yesterday_only = data['yesterday_only']
        date = date if date else datetime.now()
        my_shit = cls.MODEL.search().first()
        if my_shit is None:
            raise BusinessLogicError(f'there\'s no data in db.')

        if my_shit.create_time.date() == date.date():
            raise BusinessLogicError(
                f'date:{date.date()}\'data is already exist.'
            )

        print(my_shit.create_time)
        if yesterday_only:
            last_day = date + timedelta(days=-1)
            if last_day.date() != my_shit.create_time.date():
                raise BusinessLogicError(
                    f'the previous day:{last_day.date()}\' data is not exist.'
                )
        qs = cls.MODEL.search(
            create_time__gte="2022-12-09 00:00:00",
            create_time__lte="2022-12-10 00:00:00"
        )

        def process(obj):
            entry = model_to_dict(obj)
            entry.pop('id')
            entry['create_time'] = date
            entry['update_time'] = date
            return entry

        if qs:
            new_data = [cls.MODEL(**process(item)) for item in qs]
            cls.MODEL.objects.bulk_create(new_data)
        else:
            raise BusinessLogicError(f'there is no data 2 copy')
