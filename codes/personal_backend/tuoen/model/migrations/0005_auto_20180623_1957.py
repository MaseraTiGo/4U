# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-06-23 19:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0004_orderreturns_remark'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderreturns',
            name='channel_name',
            field=models.CharField(default='', max_length=128, verbose_name='渠道名称'),
        ),
        migrations.AddField(
            model_name='orderreturns',
            name='cus_phone',
            field=models.CharField(default='', max_length=128, verbose_name='客戶手機'),
        ),
        migrations.AddField(
            model_name='orderreturns',
            name='customer',
            field=models.CharField(default='', max_length=128, verbose_name='客戶名稱'),
        ),
        migrations.AddField(
            model_name='orderreturns',
            name='goods_name',
            field=models.CharField(default='', max_length=128, verbose_name='商品名稱'),
        ),
        migrations.AddField(
            model_name='orderreturns',
            name='quantity',
            field=models.IntegerField(default=0, verbose_name='商品数量'),
        ),
        migrations.AddField(
            model_name='orderreturns',
            name='servicer',
            field=models.CharField(default='', max_length=128, verbose_name='客服名稱'),
        ),
        migrations.AddField(
            model_name='orderreturns',
            name='shop_name',
            field=models.CharField(default='', max_length=128, verbose_name='店铺名称'),
        ),
        migrations.AddField(
            model_name='orderreturns',
            name='total_price',
            field=models.IntegerField(default=0, verbose_name='订单金额'),
        ),
    ]
