# coding=UTF-8

'''
Created on 2016年7月23日

@author: Administrator
'''
import datetime

from django.db.models import *
from django.utils import timezone


class BaseModel(Model):
    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        abstract = True

    @classmethod
    def create(cls, **kwargs):
        valid_keys = set(field.name for field in cls._meta.fields)
        default = {attr: val for attr, val in kwargs.items() if attr in valid_keys}
        try:
            return cls.objects.create(**default)
        except Exception as e:
            raise e

    @classmethod
    def get_byid(cls, id):
        try:
            relations = [field.name for field in cls.get_relateionship_fields()]
            return cls.objects.select_related(*relations).get(id=id)
        except:
            return None

    @classmethod
    def get_relateionship_fields(cls):
        return [field for field in cls._meta.fields if isinstance(field, ForeignKey)]

    @classmethod
    def get_valid_fieldname(cls):
        return {field.name: field for field in cls._meta.fields}

    @classmethod
    def query(cls, **search_info):
        relations = [field.name for field in cls.get_relateionship_fields()]
        valid_mapping = cls.get_valid_fieldname()
        qs = cls.objects.select_related(*relations).filter()

        for key, val in search_info.items():
            if key in valid_mapping:
                field = valid_mapping[key]
                if val or isinstance(field, BooleanField) or isinstance(field, IntegerField):
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
                        temp.update({field.name: datetime.date(val.year, val.month, val.day)})
                    elif isinstance(field, ForeignKey):
                        temp.update({field.name: val})
                    qs = qs.filter(**temp)

        return qs

    def update(self, **kwargs):
        valid_files = []
        valid_keys = self.__class__.get_valid_fieldname().keys()

        for attr, val in kwargs.items():
            if attr in valid_keys:
                setattr(self, attr, val)
                valid_files.append(attr)

        try:
            if valid_files:
                self.save()
                for attr in valid_files:
                    kwargs.pop(attr)
            return True
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
