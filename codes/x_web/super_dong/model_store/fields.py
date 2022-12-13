# -*- coding: UTF-8 -*-    
# Author: Dongjd
# FileName: fields
# DateTime: 2021/06/7 18:50
# Project: ifw_dong
# Do Not Touch Me!

from django.db.models import ForeignKey, ManyToManyField


class VirtualForeignKey(ForeignKey):
    def __init__(self, *args, **kwargs):
        if 'db_constraint' not in kwargs:
            kwargs.update({'db_constraint': False, 'null': True})
        super(VirtualForeignKey, self).__init__(*args, **kwargs)


class VirtualManyToManyField(ManyToManyField):
    def __init__(self, *args, **kwargs):
        if 'db_constraint' not in kwargs:
            kwargs.update({'db_constraint': False})
        super(VirtualManyToManyField, self).__init__(*args, **kwargs)
