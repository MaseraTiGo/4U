# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-06-23 11:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0002_auto_20180621_1943'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportReturns',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('init', '初始化'), ('excutting', '执行中'), ('finish', '已完成'), ('failed', '失败')], default='init', max_length=24, verbose_name='执行状态')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('error_text', models.TextField(default='', null=True, verbose_name='转化失败描述')),
                ('code', models.CharField(default='', max_length=64, verbose_name='设备SN码')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderReturns',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='', max_length=128, verbose_name='设备编码')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='model.Order')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='equipment',
            name='product_status',
            field=models.CharField(default='正常', max_length=64, verbose_name='设备状态'),
        ),
    ]
