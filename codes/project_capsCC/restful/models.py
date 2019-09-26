from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=16, default='123456')

class Token(models.Model):
    tuser = models.OneToOneField(to='User', on_delete=models.CASCADE)
    token = models.CharField(max_length=32)


# -*- coding: utf-8 -*-
# file_func  :
# file_author: 'Johnathan.Wick'
# file_date  : '7/26/2019 3:30 PM'

from random import randint

from django.db.models import CharField, TextField, DateTimeField, BooleanField, IntegerField, FloatField, \
    ImageField, FilePathField
from django.utils import timezone

# from project_x.model_store.base_model import BaseModel


class Plugins(models.Model):
    """
    plugins store
    """
    uuid = CharField(verbose_name='Universally Unique Identifier', max_length=64)
    name = CharField(verbose_name='plugin\'s name', max_length=256)
    type = CharField(verbose_name='classify', max_length=64, default='UNKNOWN')
    version = CharField(verbose_name='current version num', max_length=32, default='-')
    size = CharField(verbose_name='plugins\'s size', max_length=16)
    score = FloatField(verbose_name='user rating', default=3.0)
    download = IntegerField(verbose_name='statistics of downloads', default=randint(100, 1000))
    my_download = IntegerField(verbose_name='statistics of my site downloads', default=randint(100, 1000))
    download_url = CharField(verbose_name='download url', max_length=256, default='oops, the url is missing!')
    download_code = CharField(verbose_name='download code', max_length=8, default='john')
    pics = ImageField(verbose_name='pics about this plugin', upload_to='plugins', null=True)
    thumbnail = FilePathField(verbose_name='thumbnail path', path='plugins/thumbnail', null=True)
    brief = TextField(verbose_name='brief about plugin', default='very useful plugin')
    overview = TextField(verbose_name='details about plugin', default='sorry, no details! it\'s coming soon!')
    url = CharField(verbose_name='plugin\'s url', max_length=256, default='-')
    isvalid = BooleanField(verbose_name='valid or not', default=True)
    create_time = DateTimeField(verbose_name='create time', default=timezone.now)

    @classmethod
    def search(cls, **kwargs):
        return cls.query().filter(**kwargs)

    class Meta:
        db_table = 'PluginsAlpha'

