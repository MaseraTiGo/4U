# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-06-23 16:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0003_auto_20180623_1113'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderreturns',
            name='remark',
            field=models.CharField(default='', max_length=128, verbose_name='備註'),
        ),
    ]
