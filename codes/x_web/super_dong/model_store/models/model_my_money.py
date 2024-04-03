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

import datetime

from django.db.models import CharField, JSONField, \
    SmallIntegerField, IntegerChoices, DecimalField, DateTimeField, Model, \
    ForeignKey, BooleanField, IntegerField, AutoField, DateField, TextField
from django.forms import model_to_dict
from django.utils import timezone

from super_dong.model_store import SuperDong


# from super_dong.model_store.base import BaseModel


class BaseModel(Model):
    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        abstract = True
        ordering = ("-create_time",)
        get_latest_by = "create_time"

    @classmethod
    def create(cls, **kwargs):
        valid_keys = set(field.name for field in cls._meta.fields)
        default = {attr: val for attr, val in kwargs.items() if
                   attr in valid_keys}
        try:
            return cls.objects.create(**default)
        except Exception as e:
            raise e

    @classmethod
    def get_by_id(cls, _id):
        try:
            relations = [field.name for field in cls.get_relationship_fields()]
            return cls.objects.select_related(*relations).get(id=_id)
        except Exception as e:
            raise e
            # return None

    @classmethod
    def get_relationship_fields(cls):
        return [field for field in cls._meta.fields if
                isinstance(field, ForeignKey)]

    @classmethod
    def get_valid_field_name(cls):
        return {field.name: field for field in cls._meta.fields}

    @classmethod
    def query(cls, **search_info):
        relations = [field.name for field in cls.get_relationship_fields()]
        valid_mapping = cls.get_valid_field_name()
        qs = cls.objects.select_related(*relations).filter()

        for key, val in search_info.items():
            if key in valid_mapping:
                field = valid_mapping[key]
                if val or isinstance(field, BooleanField) or \
                        isinstance(field, IntegerField):
                    temp = {}
                    if isinstance(field, AutoField):
                        temp.update({field.name: int(val)})
                    elif isinstance(field, CharField):
                        temp.update({'{}__contains'.format(field.name): val})
                    elif isinstance(field, IntegerField):
                        temp.update({field.name: int(val)})
                    elif isinstance(field, BooleanField):
                        temp.update({field.name: bool(val)})
                    elif isinstance(field, TextField):
                        temp.update({'{}__contains'.format(field.name): val})
                    elif isinstance(field, DateTimeField):
                        # fsy
                        temp.update({field.name: val})
                    elif isinstance(field, DateField):
                        # fsy
                        temp.update({field.name: datetime.date(val.year,
                                                               val.month,
                                                               val.day)})
                    elif isinstance(field, ForeignKey):
                        temp.update({field.name: val})
                    qs = qs.filter(**temp)

        return qs

    def update(self, **kwargs):
        valid_files = []
        valid_keys = self.__class__.get_valid_field_name().keys()
        for attr, val in kwargs.items():
            if attr in valid_keys:
                setattr(self, attr, val)
                valid_files.append(attr)

        try:
            if valid_files:
                self.save()
                for attr in valid_files:
                    kwargs.pop(attr)
            return self
        except Exception as e:
            raise e

    @classmethod
    def search(cls, **kwargs):
        res_qs = cls.objects.filter(**kwargs)
        return res_qs

    @classmethod
    def search_ex(cls, *res_cols, **kwargs):
        res_mapping = cls.search(**kwargs).values(*res_cols)
        return res_mapping

    @classmethod
    def single_col_list(cls, col, flat=True):
        return cls.objects.values_list(col, flat=flat)

    @classmethod
    def search_enhance(cls, *q_funcs):
        return cls.objects.filter(*q_funcs)

    def as_dict(self):
        return model_to_dict(self)

    @classmethod
    def get_field_verbose_name(cls):
        field_dict = {}
        for field in cls._meta.fields:
            field_dict[field.name] = field.verbose_name
        for field in cls._meta.many_to_many:
            field_dict[field.name] = field.verbose_name

        return field_dict

    class Meta:
        abstract = True
        ordering = ("-create_time",)
        get_latest_by = "create_time"


class MyShit(BaseModel):
    class InvestStatus(IntegerChoices):
        SELL_OUT = 0, 'sell out'
        BUY_IN = 1, 'buy in'
        HOLD = 2, 'hold'
        ON_THE_WAY = 3, 'on the way'

    class InvestType(IntegerChoices):
        SAVING = 0, "saving"
        CURRENT_DEPOSIT = 1, "current_deposit"
        FIXED_DEPOSIT = 2, "fixed_deposit"
        STEADY = 3, "steady"
        MONETARY_FUND = 4, "monetary fund"
        BOND_FUND = 5, "bond fund"
        MIXED_FUND = 6, "mixed fund"
        EQUITY_FUND = 7, "equity fund"
        STOCKS = 8, "stocks"

    class App(IntegerChoices):
        ALIPAY = 0, 'alipay'
        WECHAT = 1, 'wechat'
        INVEST_BANK = 2, 'invest bank'

    name = CharField(verbose_name="where the money is", max_length=64)
    amount = DecimalField(verbose_name="how many here is", default=0,
                          max_digits=11, decimal_places=2)
    invest_type = SmallIntegerField(verbose_name="invest type",
                                    default=InvestType.SAVING,
                                    choices=InvestType.choices)
    net_worth = DecimalField(verbose_name="net_worth", default=0, max_digits=11,
                             decimal_places=2)
    status = SmallIntegerField(verbose_name="status", default=InvestStatus.HOLD,
                               choices=InvestStatus.choices)
    app = SmallIntegerField(verbose_name="money app", default=App.INVEST_BANK,
                            choices=App.choices)
    delta = DecimalField(verbose_name='delta', default=0, max_digits=11,
                         decimal_places=2)
    share = DecimalField(verbose_name='shares', default=0, max_digits=11,
                         decimal_places=2)
    ex_info = JSONField(verbose_name="ex_info", default=dict)
    remark = CharField(verbose_name="remark", max_length=128)
    priority = IntegerField(verbose_name="priority", default=0)

    class Meta:
        ordering = ("-create_time",)
        db_table = f"{SuperDong}my_shit"


class DollarRate(BaseModel):
    sell_out = DecimalField(verbose_name="sell out price", default=0,
                            decimal_places=2, max_digits=13)
    buy_in = DecimalField(verbose_name="buy in price", default=0,
                          decimal_places=2, max_digits=13)

    class Meta:
        ordering = ("-create_time",)
        db_table = f"{SuperDong}my_fucking_dollar"


class Schedule(BaseModel):
    code = IntegerField(verbose_name="code", null=False)
    cycle = SmallIntegerField(verbose_name="cycle", default=0)
    day = IntegerField(verbose_name="day", default=0)
    today_trade = BooleanField(verbose_name="today trade", default=True)
