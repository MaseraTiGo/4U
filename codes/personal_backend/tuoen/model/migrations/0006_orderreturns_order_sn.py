# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-06-23 20:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0005_auto_20180623_1957'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderreturns',
            name='order_sn',
            field=models.CharField(default='', max_length=128, verbose_name='訂單號'),
        ),
    ]
