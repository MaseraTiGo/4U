# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-06-25 16:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0010_auto_20180625_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='equipment_status',
            field=models.CharField(choices=[('normal', 'normal'), ('replace', 'replace'), ('patch', 'patch'), ('rgoods', 'rgoods')], default='normal', max_length=64, verbose_name='设备状态'),
        ),
    ]
