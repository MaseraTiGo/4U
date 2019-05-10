# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-07-02 15:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0013_auto_20180626_0228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='journal_type',
            field=models.CharField(choices=[('login', '登录'), ('other', '其它'), ('status reset', '导入数据状态重置'), ('delete', '删除'), ('look', '查詢'), ('edit', '編輯'), ('search', '搜索'), ('remove', '刪除'), ('update', '更新')], default='other', max_length=64, verbose_name='日志类型'),
        ),
    ]
