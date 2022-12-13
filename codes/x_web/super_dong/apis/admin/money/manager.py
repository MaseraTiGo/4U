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
from super_dong.frame.utils.query_tools import TearParts
from super_dong.model_store.models import MyShit


class MyShitManager(BaseManager):
    MODEL = MyShit
    InvestType_Choices = MODEL.InvestType.choices
    Status_Choices = MODEL.InvestStatus.choices
    App_Choices = MODEL.App.choices

    @classmethod
    def create(cls, **data):
        cls.MODEL.create(**data)

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

    @classmethod
    def details(cls, search_info, page_info):
        date = search_info.get('date')
        qs = cls.search()

        if date:
            start_ = f'{str(date)} 00:00:00'
            end_ = f'{str(date)} 23:59:59'
            qs.filter(create_time__gte=start_, create_time__lte=end_)
        qs = TearParts(qs, page_info['page_num'], page_info['page_size'])
        total = 0
        data = []
        for item in qs.data:
            item: MyShit
            data.append({
                "id": item.id,
                "name": item.name,
                "amount": item.amount,
                "invest_type": item.get_invest_type_display(),
                "net_worth": item.net_worth,
                "status": item.get_status_display(),
                "app": item.get_app_display(),
                "ex_info": item.ex_info,
                "remark": item.remark,
                "create_time": item.create_time

            })
            total += item.amount
        return data, total
