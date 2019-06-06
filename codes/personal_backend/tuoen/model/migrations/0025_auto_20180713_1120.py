# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-07-13 11:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0024_auto_20180712_1632'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipmentout',
            name='is_agent',
        ),
        migrations.RemoveField(
            model_name='importequipmentout',
            name='is_agent',
        ),
        migrations.AddField(
            model_name='equipmentout',
            name='type',
            field=models.CharField(choices=[('self', '自营平台'), ('first', '一级代理'), ('second', '二级代理')], default='self', max_length=24, verbose_name='出库类型'),
        ),
        migrations.AddField(
            model_name='importequipmentout',
            name='type',
            field=models.CharField(default='', max_length=32, verbose_name='出库类型'),
        ),
    ]