# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-07-12 16:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0023_auto_20180712_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipmentregister',
            name='status',
            field=models.CharField(choices=[('normal', '正常'), ('abnormal', '异常'), ('agent', '代理商')], default='normal', max_length=32, verbose_name='状态'),
        ),
    ]