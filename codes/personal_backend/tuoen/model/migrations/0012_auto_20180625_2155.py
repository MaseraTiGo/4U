# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-06-25 21:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0011_auto_20180625_1637'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderreturns',
            name='channel_name',
        ),
        migrations.RemoveField(
            model_name='orderreturns',
            name='cus_phone',
        ),
        migrations.RemoveField(
            model_name='orderreturns',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='orderreturns',
            name='goods_name',
        ),
        migrations.RemoveField(
            model_name='orderreturns',
            name='order_sn',
        ),
        migrations.RemoveField(
            model_name='orderreturns',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='orderreturns',
            name='servicer',
        ),
        migrations.RemoveField(
            model_name='orderreturns',
            name='shop_name',
        ),
        migrations.RemoveField(
            model_name='orderreturns',
            name='total_price',
        ),
        migrations.AlterField(
            model_name='orderreturns',
            name='remark',
            field=models.CharField(default='', max_length=128, verbose_name='退货说明'),
        ),
    ]
