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
from collections import defaultdict
from datetime import datetime, timedelta

from django.forms import model_to_dict

from super_dong.frame.contri.manager import BaseManager
from super_dong.frame.core.exception import BusinessLogicError
from super_dong.frame.utils.query_tools import TearParts
from super_dong.model_store.models import MyShit


def is_last_day_exist(cur_day: str, mapping, max_offset=10) -> tuple:
    date_obj = datetime.strptime(cur_day, '%Y-%m-%d')

    days_offset = 1
    found = False
    last_date_obj = None
    while days_offset <= max_offset:
        last_date_obj = date_obj - timedelta(days=days_offset)
        if str(last_date_obj.date()) in mapping:
            found = True
            break
        days_offset += 1
    return last_date_obj, found


class MyShitManager(BaseManager):
    MODEL = MyShit
    InvestType_Choices = MODEL.InvestType.choices
    Status_Choices = MODEL.InvestStatus.choices
    App_Choices = MODEL.App.choices

    OffsetDays = 10

    @classmethod
    def create(cls, **data):
        if data['status'] == cls.MODEL.InvestStatus.SELL_OUT:
            data['amount'] = -(abs(data['amount']))
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
        query_date = None
        if yesterday_only:
            query_date = date + timedelta(days=-1)
            if query_date.date() != my_shit.create_time.date():
                raise BusinessLogicError(
                    f'the previous day:{query_date.date()}\' data is not exist.'
                )
        else:
            obj = cls.MODEL.search()[0]
            query_date = obj.create_time

        qs = cls.MODEL.search(
            create_time__gte=f"{str(query_date.date())} 00:00:00",
            create_time__lte=f"{str(query_date.date())} 23:59:59"
        ).exclude(status=cls.MODEL.InvestStatus.SELL_OUT)

        def process(shit):
            entry = model_to_dict(shit)
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
        date = date if date else datetime.today().date()

        start_ = f'{str(date)} 00:00:00'
        end_ = f'{str(date)} 23:59:59'
        qs = cls.MODEL.search(create_time__gte=start_, create_time__lte=end_)
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
            if item.status:
                total += item.amount
        return data, total

    @classmethod
    def delete(cls, id_: int):
        shit = cls.search(id=id_).first()
        if shit:
            shit.delete()

    @classmethod
    def update(cls, **update_info):
        id_ = update_info.pop('id_')
        shit = cls.search(id=id_).first()
        if not shit:
            raise BusinessLogicError(f'id_:{id_} is not existed.')
        status = update_info.get('status')
        if status == cls.MODEL.InvestStatus.SELL_OUT:
            amount = update_info.get('amount')
            amount = -(abs(amount)) if amount else -(abs(shit.amount))
            update_info['amount'] = amount
        shit.update(**update_info)

    @classmethod
    def calculate_net_worth(cls, date):
        date = date if date else datetime.today()
        yesterday = date - timedelta(days=1)

        yesterday_qs = cls.search_date(yesterday)
        yesterday_mapping = {item.name: item for item in yesterday_qs}

        cur_date_qs = cls.search_date(date)
        cur_date_mapping = {item.name: item for item in cur_date_qs}
        for name, cur_date in cur_date_mapping.items():
            if name not in yesterday_mapping:
                continue
            cur_date.net_worth = abs(cur_date.amount) - yesterday_mapping[
                name].amount

        cls.MODEL.objects.bulk_update(cur_date_qs, ['net_worth'])

    @classmethod
    def shit_profile(cls):
        qs = cls.search().exclude(status=cls.MODEL.InvestStatus.SELL_OUT)
        date_mapping = defaultdict(set)

        for item in qs:
            date = str(item.create_time.date())
            date_mapping[date].add(item)

        ret = {}
        for date, item_set in date_mapping.items():
            ret[date] = {
                "Total": float(sum([item.amount for item in item_set])),
                "Net_worth": 0
            }

        for date, data in ret.items():
            last_day_obj, found = is_last_day_exist(date, ret)

            if found:
                data['Net_worth'] = data['Total'] - \
                                    ret[str(last_day_obj.date())]['Total']
                data['Net_worth'] = float("%.2f" % data['Net_worth'])
        return ret

    @classmethod
    def sort_by_app(cls, req_data: dict):
        app_mapping = dict(cls.App_Choices)

        shit_qs = cls.MODEL.search().exclude(
            status=cls.MODEL.InvestStatus.SELL_OUT
        )

        day_app_mapping_amount = defaultdict(list)

        for item in shit_qs:
            key = str(item.create_time.date()) + '_' + str(item.app)
            day_app_mapping_amount[key].append(item.amount)

        ans = []
        day_mapping_app_amount = defaultdict(dict)
        for key, value in day_app_mapping_amount.items():
            day, app = key.rsplit('_', 1)
            ans.append({
                'app': app_mapping[int(app)],
                'amount': sum(value),
                'day': day,
                'net_worth': 0.00
            })
            day_mapping_app_amount[day][app_mapping[int(app)]] = sum(value)

        ret = {}

        for day, cur_details in day_mapping_app_amount.items():
            last_date_obj, found = is_last_day_exist(day,
                                                     day_mapping_app_amount)

            ret[day] = cur_details

            if found:
                last_details = day_mapping_app_amount[str(last_date_obj.date())]

                for key, value in last_details.items():
                    cur_day_amount = cur_details[key]
                    cur_details[key] = {
                        'total': float("%.2f" % cur_day_amount),
                        'net-worth': float("%.2f" % (cur_day_amount - value,))
                    }
            else:
                for key, value in cur_details.items():
                    cur_details[key] = {
                        'total': float("%.2f" % cur_details[key]),
                        'net-worth': 0.00
                    }
        return ret
