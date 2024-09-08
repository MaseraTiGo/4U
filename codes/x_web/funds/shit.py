# -*- coding: utf-8 -*-
# @File    : shit
# @Project : x_web
# @Time    : 2024/8/31 8:43
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
import datetime
import os

import requests


class Founds:
    BaseUrl = 'http://192.168.203.53:3000/fundMNHisNetList?FCODE={fcode}&pageIndex=1&pagesize=1'

    @classmethod
    def get_funds(cls, fund_code):
        try:
            ret = requests.get(cls.BaseUrl.format(fcode=fund_code)).json()
            networth = float(ret['Datas'][0]['DWJZ'])
        except Exception as e:
            networth = 0.0
            print(f"dong ---------------> get found: {fund_code} error: {e}")
        else:
            print(
                f"dong ---------------> get found: {fund_code} success, networth is: {networth}")
        return networth


class TodaysShit:
    @classmethod
    def calculate_shit_4_today(cls) -> None:
        today = datetime.datetime.today()
        from super_dong.models import MyShit
        my_shits = MyShit.objects.filter(create_time__date=today)
        # founds_code_mapping = {
        #     item.remark['fcode']: item
        #     for item in my_shits if item.remark.get('fcode')
        # }

        update_objs = []
        for shit in my_shits:
            fcode = shit.remark.get('fcode')
            if not fcode:
                continue
            regular_invest = shit.ex_info.get('regular_invest')
            if regular_invest:
                # cls.schedule_invest(fcode, shit)
                pass
            else:
                cls.process_normal_founds(fcode, shit)
                update_objs.append(shit)
        MyShit.objects.bulk_update(update_objs, ['amount'])

    @classmethod
    def process_normal_founds(cls, fcode, shit):
        newest_networth = Founds.get_funds(fcode)
        if not newest_networth:
            return
        shit.amount = float(
            '%.2f' % (
                    float(
                        '%.2f' % shit.share
                    ) * newest_networth - shit.ex_info.get('fix_tax', 0.0)))
        print(f"schedule invest: {shit.name}, {shit.amount}, {shit.share}")

    @classmethod
    def schedule_invest(cls, fcode, shit):
        newest_networth = Founds.get_funds(fcode)
        if not newest_networth:
            return
        fix_tax = shit.ex_info.get('fix_tax')
        regular_invest = shit.ex_info['regular_invest']
        front_end_load = shit.ex_info.get('front-end-load')
        if fix_tax:
            regular_invest -= fix_tax
        if front_end_load:
            regular_invest -= regular_invest * front_end_load

        increase_share = Decimal(regular_invest / newest_networth)
        shit.share += increase_share
        shit.amount = shit.share * Decimal(newest_networth)
        print(f"schedule invest: {shit.name}, {shit.amount}, {shit.share}")


if __name__ == '__main__':
    from decimal import Decimal
    from django import setup

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')
    setup()
    TodaysShit.calculate_shit_4_today()
