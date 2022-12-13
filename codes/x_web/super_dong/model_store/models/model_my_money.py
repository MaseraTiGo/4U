# -*- coding: utf-8 -*-
# @File    : model_my_money
# @Project : Apollo_Shit
# @Time    : 2022/12/9 13:56
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""

__all__ = ("MyShit",)

from django.db.models import CharField, IntegerField, JSONField, \
    SmallIntegerField, IntegerChoices, DecimalField

from super_dong.model_store import SuperDong
from super_dong.model_store.base import BaseModel


class MyShit(BaseModel):
    class InvestStatus(IntegerChoices):
        SELL_OUT = 0, 'sell out'
        BUY_IN = 1, 'buy in'
        HOLD = 2, 'hold'

    class InvestType(IntegerChoices):
        SAVING = 0, "saving"
        CURRENT_DEPOSIT = 1, "current_deposit"
        FIXED_DEPOSIT = 2, "fixed_deposit"
        STEADY = 3, "steady"
        FOUND = 4, "found"
        STOCKS = 5, "stocks"

    class App(IntegerChoices):
        ALIPAY = 0, 'alipay'
        WECHAT = 1, 'wechat'
        INVEST_BANK = 2, 'invest bank'

    name = CharField(verbose_name="where the money is", max_length=32)
    amount = DecimalField(verbose_name="how many here is", default=0, max_digits=11, decimal_places=2)
    invest_type = SmallIntegerField(verbose_name="invest type",
                                    default=InvestType.SAVING, choices=InvestType.choices)
    net_worth = DecimalField(verbose_name="net_worth", default=0, max_digits=11, decimal_places=2)
    status = SmallIntegerField(verbose_name="status", default=InvestStatus.HOLD, choices=InvestStatus.choices)
    app = SmallIntegerField(verbose_name="money app", default=App.INVEST_BANK, choices=App.choices)

    ex_info = JSONField(verbose_name="ex_info", default=dict)
    remark = CharField(verbose_name="remark", max_length=128)

    class Meta:
        ordering = ("-create_time",)
        db_table = f"{SuperDong}my_shit"
