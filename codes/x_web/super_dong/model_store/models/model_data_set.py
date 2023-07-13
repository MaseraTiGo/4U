# -*- coding: utf-8 -*-
# @File    : model_data_set
# @Project : x_web
# @Time    : 2023/7/11 16:01
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
from django.db.models import IntegerField, CharField

from super_dong.model_store.base import BaseModel


class WhitePig(BaseModel):
    db_name = CharField(verbose_name='name of db', max_length=32)
    pig_id = IntegerField(verbose_name='pig_id')
    remark = CharField(verbose_name='remark', max_length=32)
